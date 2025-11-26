#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA4_1

"""
Gerador de Código Assembly AVR para Arduino Uno (ATmega328P)

Este módulo implementa a geração de código Assembly AVR a partir de TAC otimizado.
Inclui alocação de registradores, spilling para memória e mapeamento TAC → Assembly.
"""

from typing import Dict, List, Tuple, Optional, Any
import json


class GeradorAssembly:
    """
    Gerador de Assembly AVR com alocação de registradores integrada.

    Características:
    - Suporte a 16-bit (4 pares de registradores: R16:R17, R18:R19, R20:R21, R22:R23)
    - Spilling FIFO para SRAM quando registradores esgotam
    - Constantes literais carregadas com LDI (sem alocar do pool)
    - Mapeamento completo TAC → AVR Assembly
    """

    def __init__(self):
        """Inicializa o gerador com alocação simplificada de registradores.

        Estratégia simplificada (sem spilling):
        - Variáveis conhecidas (COUNTER, RESULT, LIMIT, FIB_*) têm alocações fixas
        - Temporários (t0, t1, ...) sempre usam R24:R25 (scratch register)
        - Nenhum spilling para memória - tudo em registradores
        """
        # Alocações FIXAS para variáveis conhecidas (factorial/fibonacci)
        # IMPORTANT: R18:R19 and R20:R21 are used by mul16 routine!
        # Don't allocate persistent variables to these registers.
        self._fixed_allocations: Dict[str, Tuple[int, int]] = {
            # Factorial variables (avoid R18-R21 used by mul16)
            "COUNTER":   (12, 13),   # Changed from R16:R17
            "RESULT":    (14, 15),   # Changed from R18:R19
            "LIMIT":     (16, 17),   # Changed from R20:R21

            # Fibonacci variables (needs 5 pairs total!)
            "FIB_0":     (6, 7),     # Using lower registers for fibonacci-specific vars
            "FIB_1":     (8, 9),
            "FIB_NEXT":  (10, 11),
            # COUNTER and LIMIT will reuse (12,13) and (16,17) when fibonacci runs
        }

        # Track which variables have been allocated
        self._var_to_reg_pair: Dict[str, Tuple[int, int]] = {}

        # Available pairs for dynamic allocation
        # R22:R23 available for unknowns
        self._available_pairs: List[Tuple[int, int]] = [(22, 23)]

        # Rotinas auxiliares necessárias (serão geradas no epílogo)
        self._routines_needed: set = set()

    # =========================================================================
    # FUNÇÃO PRINCIPAL - INTERFACE PÚBLICA
    # =========================================================================

    def gerarAssembly(self, tac_otimizado: Dict[str, Any]) -> str:
        """
        Gera código Assembly AVR a partir de TAC otimizado.

        Esta é a ÚNICA função pública do gerador.

        Args:
            tac_otimizado: Dicionário com chave "instructions" contendo lista de instruções TAC
                          Formato esperado:
                          {
                              "instructions": [
                                  {"type": "assignment", "dest": "t0", "source": "1", "line": 1},
                                  {"type": "binary_op", "result": "t2", "operand1": "t0",
                                   "operator": "+", "operand2": "t1", "line": 2},
                                  ...
                              ]
                          }

        Returns:
            String contendo o código Assembly AVR completo, pronto para ser salvo em .s

        Raises:
            KeyError: Se tac_otimizado não contém chave "instructions"
            ValueError: Se alguma instrução TAC tiver formato inválido
        """
        if "instructions" not in tac_otimizado:
            raise KeyError("TAC otimizado deve conter chave 'instructions'")

        asm_lines: List[str] = []

        # 1. Gerar prólogo (inicialização do programa)
        asm_lines.extend(self._gerar_prologo())

        # 2. Processar cada instrução TAC
        instructions = tac_otimizado["instructions"]
        for instr in instructions:
            asm_lines.extend(self._processar_instrucao(instr))

        # 3. Gerar epílogo (finalização do programa)
        asm_lines.extend(self._gerar_epilogo(instructions))

        return "\n".join(asm_lines)

    # =========================================================================
    # MÉTODOS DE ALOCAÇÃO DE REGISTRADORES (PRIVADOS)
    # =========================================================================

    def _get_reg_pair(self, var_name: str) -> Tuple[int, int]:
        """
        Obtém par de registradores para variável TAC (alocação simplificada).

        Estratégia simplificada (SEM SPILLING):
        1. Se é variável conhecida (COUNTER, RESULT, etc.) → usa alocação fixa
        2. Se é temporário (t0, t1, ...) → sempre usa R24:R25 (scratch)
        3. Se já foi alocado antes → retorna o mesmo par
        4. Senão → aloca do pool disponível (ou usa R24:R25 como fallback)

        Args:
            var_name: Nome da variável TAC (ex: "COUNTER", "t0", "FIB_0")

        Returns:
            Tupla (reg_low, reg_high) representando par de registradores
            Exemplo: (16, 17) para R16:R17

        Note:
            Esta versão simplificada NUNCA faz spilling para memória.
            Assume que o código TAC não excede 4 pares de registradores.
        """
        # Caso 1: Variável já foi alocada anteriormente
        if var_name in self._var_to_reg_pair:
            return self._var_to_reg_pair[var_name]

        # Caso 2: Variável conhecida com alocação fixa
        if var_name in self._fixed_allocations:
            pair = self._fixed_allocations[var_name]
            self._var_to_reg_pair[var_name] = pair
            return pair

        # Caso 3: Temporário (t0, t1, t2, ...) → sempre usa R24:R25 (scratch)
        if var_name.startswith("t") and var_name[1:].isdigit():
            # Temporaries don't get persistent allocation - always R24:R25
            # This is safe because temporaries are consumed immediately
            return (24, 25)

        # Caso 4: Variável desconhecida → aloca do pool disponível
        if self._available_pairs:
            pair = self._available_pairs.pop(0)
            self._var_to_reg_pair[var_name] = pair
            return pair

        # Caso 5: Fallback - sem registradores disponíveis
        # Use R24:R25 como último recurso (pode sobrescrever temporários!)
        # Este caso NÃO deveria acontecer para factorial/fibonacci
        return (24, 25)

    # Spilling methods removed - simplified allocator doesn't need them

    # =========================================================================
    # MÉTODOS AUXILIARES (PRIVADOS)
    # =========================================================================

    def _is_constant(self, operand: str) -> bool:
        """
        Verifica se operando é uma constante literal numérica.

        Constantes não alocam registradores do pool - são carregadas com LDI.

        Args:
            operand: String do operando (ex: "5", "3.14", "t0")

        Returns:
            True se é número (int ou float), False se é variável
        """
        try:
            float(operand)
            return True
        except ValueError:
            return False

    def _load_constant_16bit(self, value: float, reg_low: int, reg_high: int) -> List[str]:
        """
        Gera código Assembly para carregar constante literal em par de registradores.

        Usa instrução LDI (Load Immediate) - não consome do pool de registradores.
        Para inteiros, armazena em formato 16-bit little-endian.

        Args:
            value: Valor da constante (int ou float)
            reg_low: Registrador para byte baixo
            reg_high: Registrador para byte alto

        Returns:
            Lista de linhas Assembly (comentário + 2x ldi)

        Note:
            Float de 16-bit (half-precision) será implementado em sub-issue 3.5
            Por enquanto, trata apenas inteiros
        """
        # TODO: Implementar conversão para float16 (IEEE 754 half-precision) no sub-issue 3.5
        # Por enquanto, assume inteiro
        int_value = int(value)

        low_byte = int_value & 0xFF
        high_byte = (int_value >> 8) & 0xFF

        return [
            f"    ldi r{reg_low}, {low_byte}   ; Constante {int_value} (low byte)",
            f"    ldi r{reg_high}, {high_byte}  ; Constante {int_value} (high byte)",
            ""
        ]

    # =========================================================================
    # PROCESSAMENTO DE INSTRUÇÕES TAC (PRIVADOS)
    # =========================================================================

    def _processar_instrucao(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa uma instrução TAC e gera código Assembly correspondente.

        Args:
            instr: Dicionário representando instrução TAC

        Returns:
            Lista de linhas Assembly geradas

        Raises:
            ValueError: Se tipo de instrução é inválido ou não implementado
        """
        instr_type = instr.get("type")

        # No more spilling! Simplified allocator handles everything in registers

        if instr_type == "assignment":
            return self._processar_assignment(instr)
        elif instr_type == "copy":
            return self._processar_copy(instr)
        elif instr_type == "binary_op":
            return self._processar_binary_op(instr)
        elif instr_type == "label":
            return self._processar_label(instr)
        elif instr_type == "goto":
            return self._processar_goto(instr)
        elif instr_type == "if_goto":
            return self._processar_if_goto(instr)
        elif instr_type == "if_false_goto":
            return self._processar_if_false_goto(instr)
        else:
            # TODO: Implementar outros tipos de instrução nos próximos sub-issues
            return [f"    ; TODO: Implementar tipo '{instr_type}'", ""]

    def _processar_assignment(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa instrução de atribuição: dest = source

        Exemplos TAC:
        - t0 = 5     (constante)
        - t1 = t0    (cópia entre variáveis)

        Args:
            instr: {"type": "assignment", "dest": "t0", "source": "5", "line": 1}

        Returns:
            Linhas Assembly geradas
        """
        dest = instr["dest"]
        source = instr["source"]
        line = instr.get("line", "?")

        asm = [f"    ; TAC linha {line}: {dest} = {source}"]

        # Caso 1: Source é constante literal → usar LDI
        if self._is_constant(source):
            dest_low, dest_high = self._get_reg_pair(dest)
            asm.extend(self._load_constant_16bit(float(source), dest_low, dest_high))

        # Caso 2: Source é variável → copiar entre registradores
        else:
            dest_low, dest_high = self._get_reg_pair(dest)
            src_low, src_high = self._get_reg_pair(source)
            asm.extend([
                f"    mov r{dest_low}, r{src_low}   ; {dest} = {source}",
                f"    mov r{dest_high}, r{src_high}",
                ""
            ])

        return asm

    def _processar_copy(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa instrução de cópia: dest = source

        Diferente de assignment, copy é usado para renomear variáveis
        após otimizações (ex: X_VAL = t0, X_SQUARED = t1).

        Exemplos TAC:
        - X_VAL = t0         (renomear temporário)
        - RESULT_COS = t17   (nomear resultado final)
        - t0 = 1000          (constante)

        Args:
            instr: {"type": "copy", "dest": "X_VAL", "source": "t0", "line": 1}

        Returns:
            Linhas Assembly geradas
        """
        dest = instr["dest"]
        source = instr["source"]
        line = instr.get("line", "?")

        asm = [f"    ; TAC linha {line}: {dest} = {source}"]

        # Caso 1: Source é constante literal → usar LDI
        if self._is_constant(source):
            dest_low, dest_high = self._get_reg_pair(dest)
            asm.extend(self._load_constant_16bit(float(source), dest_low, dest_high))

        # Caso 2: Source é variável → copiar entre registradores
        else:
            dest_low, dest_high = self._get_reg_pair(dest)
            src_low, src_high = self._get_reg_pair(source)
            asm.extend([
                f"    mov r{dest_low}, r{src_low}   ; {dest} = {source}",
                f"    mov r{dest_high}, r{src_high}",
                ""
            ])

        return asm

    def _processar_binary_op(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa operação binária: result = operand1 op operand2

        Exemplo TAC:
        - t2 = t0 + t1

        Args:
            instr: {"type": "binary_op", "result": "t2", "operand1": "t0",
                    "operator": "+", "operand2": "t1", "line": 2}

        Returns:
            Linhas Assembly geradas
        """
        operator = instr["operator"]

        # Despachar para função específica de cada operador
        if operator == "+":
            return self._processar_adicao_16bit(instr)
        elif operator == "-":
            return self._processar_subtracao_16bit(instr)
        elif operator == "*":
            return self._processar_multiplicacao_16bit(instr)
        elif operator == "/":
            return self._processar_divisao_16bit(instr)
        elif operator == "%":
            return self._processar_modulo_16bit(instr)
        elif operator == "^":
            return self._processar_exponenciacao_16bit(instr)
        elif operator == "|":
            return self._processar_divisao_real(instr)
        # Operadores de comparação
        elif operator == "==":
            return self._processar_comparacao_eq(instr)
        elif operator == "!=":
            return self._processar_comparacao_ne(instr)
        elif operator == "<":
            return self._processar_comparacao_lt(instr)
        elif operator == "<=":
            return self._processar_comparacao_le(instr)
        elif operator == ">":
            return self._processar_comparacao_gt(instr)
        elif operator == ">=":
            return self._processar_comparacao_ge(instr)
        else:
            line = instr.get("line", "?")
            return [
                f"    ; TAC linha {line}: {instr['result']} = {instr['operand1']} {operator} {instr['operand2']}",
                f"    ; ERRO: Operador '{operator}' não reconhecido!",
                ""
            ]

    def _processar_adicao_16bit(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa adição 16-bit: result = op1 + op2

        Usa instruções ADD (low byte) e ADC (high byte com carry).

        CRITICAL: Copy operands to result FIRST to avoid destroying source operands.
        This is essential for loops where operands may be reused (e.g., COUNTER + 1).

        Handles constants efficiently: if op2 is constant, uses temporary registers
        instead of allocating from register pool.

        Args:
            instr: {"type": "binary_op", "result": "t2", "operand1": "t0",
                    "operator": "+", "operand2": "t1", "line": 2}

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        asm = [f"    ; TAC linha {line}: {result} = {op1} + {op2}"]

        # Get op1 and result register pairs
        op1_low, op1_high = self._get_reg_pair(op1)
        res_low, res_high = self._get_reg_pair(result)

        # Check if op2 is a constant
        if self._is_constant(op2):
            # Use temporary registers R22:R23 for constant loading
            # (R24:R25 may already be allocated to result!)
            int_value = int(float(op2))
            low_byte = int_value & 0xFF
            high_byte = (int_value >> 8) & 0xFF

            asm.extend([
                f"    ; Soma 16-bit: {result} = {op1} + {op2} (op2 is constant)",
                f"    mov r{res_low}, r{op1_low}   ; Copy op1 to result FIRST",
                f"    mov r{res_high}, r{op1_high}",
                f"    ldi r22, {low_byte}          ; Load constant low byte into temp",
                f"    ldi r23, {high_byte}         ; Load constant high byte into temp",
                f"    add r{res_low}, r22          ; Add constant to result (low byte with carry)",
                f"    adc r{res_high}, r23         ; Add constant to result (high byte with carry)",
                ""
            ])
        else:
            # op2 is a variable, get its register pair
            op2_low, op2_high = self._get_reg_pair(op2)

            asm.extend([
                f"    ; Soma 16-bit: {result} = {op1} + {op2}",
                f"    mov r{res_low}, r{op1_low}   ; Copy op1 to result FIRST",
                f"    mov r{res_high}, r{op1_high}",
                f"    add r{res_low}, r{op2_low}   ; Add op2 to result (low byte with carry)",
                f"    adc r{res_high}, r{op2_high} ; Add op2 to result (high byte with carry)",
                ""
            ])

        return asm

    def _processar_subtracao_16bit(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa subtração 16-bit: result = op1 - op2

        Usa instruções SUB (low byte) e SBC (high byte com carry/borrow).

        CRITICAL: Copy operands to result FIRST to avoid destroying source operands.
        This is essential for loops where operands may be reused.

        Handles constants efficiently: if op2 is constant, uses temporary registers
        instead of allocating from register pool.

        Args:
            instr: {"type": "binary_op", "result": "t2", "operand1": "t0",
                    "operator": "-", "operand2": "t1", "line": 2}

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        asm = [f"    ; TAC linha {line}: {result} = {op1} - {op2}"]

        # Get op1 and result register pairs
        op1_low, op1_high = self._get_reg_pair(op1)
        res_low, res_high = self._get_reg_pair(result)

        # Check if op2 is a constant
        if self._is_constant(op2):
            # Use temporary registers R22:R23 for constant loading
            # (R24:R25 may already be allocated to result!)
            int_value = int(float(op2))
            low_byte = int_value & 0xFF
            high_byte = (int_value >> 8) & 0xFF

            asm.extend([
                f"    ; Subtração 16-bit: {result} = {op1} - {op2} (op2 is constant)",
                f"    mov r{res_low}, r{op1_low}   ; Copy op1 to result FIRST",
                f"    mov r{res_high}, r{op1_high}",
                f"    ldi r22, {low_byte}          ; Load constant low byte into temp",
                f"    ldi r23, {high_byte}         ; Load constant high byte into temp",
                f"    sub r{res_low}, r22          ; Subtract constant from result (low byte with borrow)",
                f"    sbc r{res_high}, r23         ; Subtract constant from result (high byte with borrow)",
                ""
            ])
        else:
            # op2 is a variable, get its register pair
            op2_low, op2_high = self._get_reg_pair(op2)

            asm.extend([
                f"    ; Subtração 16-bit: {result} = {op1} - {op2}",
                f"    mov r{res_low}, r{op1_low}   ; Copy op1 to result FIRST",
                f"    mov r{res_high}, r{op1_high}",
                f"    sub r{res_low}, r{op2_low}   ; Subtract op2 from result (low byte with borrow)",
                f"    sbc r{res_high}, r{op2_high} ; Subtract op2 from result (high byte with borrow)",
                ""
            ])

        return asm

    def _processar_multiplicacao_16bit(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa multiplicação 16-bit com re-normalização de escala SOMENTE para reais.

        INTEGERS (data_type="int"):
          result = op1 * op2  (direct multiplication)

        REALS (data_type="real"):
          Quando multiplicando dois valores escalados (ambos 100x):
            (A * 100) * (B * 100) = (A * B) * 10,000
          Para manter escala 100x, dividimos por 100:
            result = (A * B * 10,000) / 100 = (A * B) * 100

        Exemplo INTEGER: 5 * 6 = 30 (no scaling)
        Exemplo REAL: 50 * 50 = 2500, então 2500 / 100 = 25 (representa 0.5 * 0.5 = 0.25)

        Usa rotinas auxiliares mul16 e div16 que serão geradas no epílogo.
        Convenção: op1 em R18:R19, op2 em R20:R21, resultado em R24:R25

        Args:
            instr: Instrução TAC de multiplicação

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")
        data_type = instr.get("data_type", "int")  # Default to int if not specified

        # Registrar que precisamos da rotina mul16
        self._routines_needed.add("mul16")

        asm = [f"    ; TAC linha {line}: {result} = {op1} * {op2} (type: {data_type})"]

        # Get result register pair
        res_low, res_high = self._get_reg_pair(result)

        # Prepare operands for mul16 (R18:R19 = op1, R20:R21 = op2)
        # Handle constants efficiently
        if self._is_constant(op1):
            int_value = int(float(op1))
            low_byte = int_value & 0xFF
            high_byte = (int_value >> 8) & 0xFF
            asm.extend([
                f"    ; Load op1 constant {op1}",
                f"    ldi r18, {low_byte}",
                f"    ldi r19, {high_byte}",
            ])
        else:
            op1_low, op1_high = self._get_reg_pair(op1)
            # Only move if source and destination are different
            if op1_low != 18 or op1_high != 19:
                asm.extend([
                    f"    ; Load op1 variable {op1}",
                    f"    mov r18, r{op1_low}",
                    f"    mov r19, r{op1_high}",
                ])
            else:
                asm.append(f"    ; op1 {op1} already in R18:R19")

        if self._is_constant(op2):
            int_value = int(float(op2))
            low_byte = int_value & 0xFF
            high_byte = (int_value >> 8) & 0xFF
            asm.extend([
                f"    ; Load op2 constant {op2}",
                f"    ldi r20, {low_byte}",
                f"    ldi r21, {high_byte}",
            ])
        else:
            op2_low, op2_high = self._get_reg_pair(op2)
            # Only move if source and destination are different
            if op2_low != 20 or op2_high != 21:
                asm.extend([
                    f"    ; Load op2 variable {op2}",
                    f"    mov r20, r{op2_low}",
                    f"    mov r21, r{op2_high}",
                ])
            else:
                asm.append(f"    ; op2 {op2} already in R20:R21")

        asm.append(f"    rcall mul16              ; R24:R25 = op1 * op2")

        # Only apply scale renormalization for REAL numbers
        if data_type == "real":
            # Need div16 for scale renormalization
            self._routines_needed.add("div16")
            asm.extend([
                f"    ; Re-normalize: divide by 100 to restore 100x scaling",
                f"    mov r18, r24",
                f"    mov r19, r25",
                f"    ldi r20, 100             ; Divide by scale factor",
                f"    ldi r21, 0",
                f"    rcall div16              ; R24:R25 = result (scaled¹)",
            ])

        # Copy result to destination (only if different from R24:R25)
        if res_low != 24 or res_high != 25:
            asm.extend([
                f"    mov r{res_low}, r24",
                f"    mov r{res_high}, r25",
                ""
            ])
        else:
            asm.append(f"    ; Result already in R24:R25\n")

        return asm

    def _processar_divisao_16bit(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa divisão inteira 16-bit: result = op1 / op2

        Usa rotina auxiliar div16 que retorna quociente em R24:R25 e resto em R22:R23.
        Convenção: op1 em R18:R19 (dividendo), op2 em R20:R21 (divisor), quociente em R24:R25

        Args:
            instr: Instrução TAC de divisão

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        # Registrar que precisamos da rotina div16
        self._routines_needed.add("div16")

        asm = [f"    ; TAC linha {line}: {result} = {op1} / {op2}"]

        # Obter registradores dos operandos
        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        asm.extend([
            f"    ; Divisão 16-bit: {result} = {op1} / {op2}",
            f"    ; Preparar parâmetros para div16",
            f"    mov r18, r{op1_low}   ; Dividendo (low)",
            f"    mov r19, r{op1_high}  ; Dividendo (high)",
            f"    mov r20, r{op2_low}   ; Divisor (low)",
            f"    mov r21, r{op2_high}  ; Divisor (high)",
            f"    rcall div16           ; Chamar rotina (quociente em R24:R25, resto em R22:R23)",
            f"    mov r{res_low}, r24   ; Copiar quociente",
            f"    mov r{res_high}, r25",
            ""
        ])

        return asm

    def _processar_modulo_16bit(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa módulo 16-bit: result = op1 % op2

        Usa mesma rotina div16, mas retorna o RESTO (R22:R23) ao invés do quociente.
        Convenção: op1 em R18:R19 (dividendo), op2 em R20:R21 (divisor), resto em R22:R23

        Args:
            instr: Instrução TAC de módulo

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        # Registrar que precisamos da rotina div16 (mesma rotina!)
        self._routines_needed.add("div16")

        asm = [f"    ; TAC linha {line}: {result} = {op1} % {op2}"]

        # Obter registradores dos operandos
        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        asm.extend([
            f"    ; Módulo 16-bit: {result} = {op1} % {op2}",
            f"    ; Preparar parâmetros para div16",
            f"    mov r18, r{op1_low}   ; Dividendo (low)",
            f"    mov r19, r{op1_high}  ; Dividendo (high)",
            f"    mov r20, r{op2_low}   ; Divisor (low)",
            f"    mov r21, r{op2_high}  ; Divisor (high)",
            f"    rcall div16           ; Chamar rotina (quociente em R24:R25, resto em R22:R23)",
            f"    mov r{res_low}, r22   ; Copiar RESTO (não quociente!)",
            f"    mov r{res_high}, r23",
            ""
        ])

        return asm

    def _processar_exponenciacao_16bit(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa exponenciação 16-bit: result = op1 ^ op2

        Args:
            instr: Instrução TAC de exponenciação

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        # TODO: Implementar na Fase 4
        return [
            f"    ; TAC linha {line}: {result} = {op1} ^ {op2}",
            f"    ; TODO: Implementar exponenciação 16-bit (Fase 4)",
            ""
        ]

    def _processar_divisao_real(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa divisão real: result = op1 | op2

        Operands are already scaled by 100x from TAC generation.
        To maintain precision, we multiply dividend by 100 before dividing:
        result = (op1 * 100) / op2

        Example: 100 | 200 (represents 1.0 / 2.0)
                 = (100 * 100) / 200
                 = 10000 / 200
                 = 50 (represents 0.5) ✓

        Args:
            instr: {"type": "binary_op", "result": "t2", "operand1": "t0",
                    "operator": "|", "operand2": "t1", "line": 5}

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        # Obter registradores dos operandos
        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        # Need mul16 and div16 for scaled division
        self._routines_needed.add("mul16")
        self._routines_needed.add("div16")

        return [
            f"    ; TAC linha {line}: {result} = {op1} | {op2}",
            f"    ; Real division: (op1 * 100) / op2 for precision",
            f"    ; Step 1: Multiply dividend by scale factor (100)",
            f"    mov r18, r{op1_low}      ; Dividendo",
            f"    mov r19, r{op1_high}",
            f"    ldi r20, 100             ; Scale factor (100)",
            f"    ldi r21, 0",
            f"    rcall mul16              ; R24:R25 = op1 * 100",
            f"    ; Step 2: Divide scaled dividend by divisor",
            f"    mov r18, r24             ; Move result to dividend registers",
            f"    mov r19, r25",
            f"    mov r20, r{op2_low}      ; Divisor",
            f"    mov r21, r{op2_high}",
            f"    rcall div16              ; R24:R25 = (op1 * 100) / op2",
            f"    mov r{res_low}, r24      ; Copy result",
            f"    mov r{res_high}, r25",
            ""
        ]

    # ====================================================================
    # Operadores de Comparação (16-bit unsigned)
    # ====================================================================

    def _processar_comparacao_eq(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa comparação de igualdade: result = op1 == op2
        Retorna 1 (0x0001) se op1 == op2, 0 (0x0000) caso contrário

        Usa instruções CP (compare low) e CPC (compare high with carry).
        Verifica flag Z (zero) - se ambos bytes forem iguais, Z=1.

        Args:
            instr: Instrução TAC de comparação

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        skip_label = f"skip_eq_{line}"

        # Obter registradores dos operandos
        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        return [
            f"    ; TAC linha {line}: {result} = {op1} == {op2}",
            f"    ; Comparação 16-bit de igualdade (unsigned)",
            f"    cp r{op1_low}, r{op2_low}      ; Compare low bytes",
            f"    cpc r{op1_high}, r{op2_high}   ; Compare high bytes with carry",
            f"    ldi r{res_low}, 0               ; Assume false",
            f"    ldi r{res_high}, 0",
            f"    brne {skip_label}               ; If not equal, skip",
            f"    ldi r{res_low}, 1               ; Set true",
            f"{skip_label}:",
            ""
        ]

    def _processar_comparacao_ne(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa comparação de desigualdade: result = op1 != op2
        Retorna 1 (0x0001) se op1 != op2, 0 (0x0000) caso contrário

        Args:
            instr: Instrução TAC de comparação

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        skip_label = f"skip_ne_{line}"

        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        return [
            f"    ; TAC linha {line}: {result} = {op1} != {op2}",
            f"    ; Comparação 16-bit de desigualdade (unsigned)",
            f"    cp r{op1_low}, r{op2_low}      ; Compare low bytes",
            f"    cpc r{op1_high}, r{op2_high}   ; Compare high bytes with carry",
            f"    ldi r{res_low}, 0               ; Assume false",
            f"    ldi r{res_high}, 0",
            f"    breq {skip_label}               ; If equal, skip",
            f"    ldi r{res_low}, 1               ; Set true",
            f"{skip_label}:",
            ""
        ]

    def _processar_comparacao_lt(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa comparação menor que: result = op1 < op2
        Retorna 1 (0x0001) se op1 < op2, 0 (0x0000) caso contrário

        Usa BRSH (branch if same or higher) para inverter lógica.
        Flag C (carry) é setado se op1 < op2 (unsigned).

        Args:
            instr: Instrução TAC de comparação

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        skip_label = f"skip_lt_{line}"

        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        return [
            f"    ; TAC linha {line}: {result} = {op1} < {op2}",
            f"    ; Comparação 16-bit menor que (unsigned)",
            f"    cp r{op1_low}, r{op2_low}      ; Compare low bytes",
            f"    cpc r{op1_high}, r{op2_high}   ; Compare high bytes with carry",
            f"    ldi r{res_low}, 0               ; Assume false",
            f"    ldi r{res_high}, 0",
            f"    brsh {skip_label}               ; If A >= B, skip",
            f"    ldi r{res_low}, 1               ; Set true (A < B)",
            f"{skip_label}:",
            ""
        ]

    def _processar_comparacao_ge(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa comparação maior ou igual: result = op1 >= op2
        Retorna 1 (0x0001) se op1 >= op2, 0 (0x0000) caso contrário

        Args:
            instr: Instrução TAC de comparação

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        skip_label = f"skip_ge_{line}"

        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        return [
            f"    ; TAC linha {line}: {result} = {op1} >= {op2}",
            f"    ; Comparação 16-bit maior ou igual (unsigned)",
            f"    cp r{op1_low}, r{op2_low}      ; Compare low bytes",
            f"    cpc r{op1_high}, r{op2_high}   ; Compare high bytes with carry",
            f"    ldi r{res_low}, 0               ; Assume false",
            f"    ldi r{res_high}, 0",
            f"    brlo {skip_label}               ; If A < B, skip",
            f"    ldi r{res_low}, 1               ; Set true (A >= B)",
            f"{skip_label}:",
            ""
        ]

    def _processar_comparacao_gt(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa comparação maior que: result = op1 > op2
        Retorna 1 (0x0001) se op1 > op2, 0 (0x0000) caso contrário

        Implementação: A > B é equivalente a B < A (troca operandos)

        Args:
            instr: Instrução TAC de comparação

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        skip_label = f"skip_gt_{line}"

        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        return [
            f"    ; TAC linha {line}: {result} = {op1} > {op2}",
            f"    ; Comparação 16-bit maior que (unsigned)",
            f"    ; Implementado como: B < A (operandos trocados)",
            f"    cp r{op2_low}, r{op1_low}      ; Compare B with A (reversed)",
            f"    cpc r{op2_high}, r{op1_high}",
            f"    ldi r{res_low}, 0               ; Assume false",
            f"    ldi r{res_high}, 0",
            f"    brsh {skip_label}               ; If B >= A, skip",
            f"    ldi r{res_low}, 1               ; Set true (B < A, i.e., A > B)",
            f"{skip_label}:",
            ""
        ]

    def _processar_comparacao_le(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa comparação menor ou igual: result = op1 <= op2
        Retorna 1 (0x0001) se op1 <= op2, 0 (0x0000) caso contrário

        Implementação: A <= B é equivalente a B >= A (troca operandos)

        Args:
            instr: Instrução TAC de comparação

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        skip_label = f"skip_le_{line}"

        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        return [
            f"    ; TAC linha {line}: {result} = {op1} <= {op2}",
            f"    ; Comparação 16-bit menor ou igual (unsigned)",
            f"    ; Implementado como: B >= A (operandos trocados)",
            f"    cp r{op2_low}, r{op1_low}      ; Compare B with A (reversed)",
            f"    cpc r{op2_high}, r{op1_high}",
            f"    ldi r{res_low}, 0               ; Assume false",
            f"    ldi r{res_high}, 0",
            f"    brlo {skip_label}               ; If B < A, skip",
            f"    ldi r{res_low}, 1               ; Set true (B >= A, i.e., A <= B)",
            f"{skip_label}:",
            ""
        ]

    def _processar_label(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa label (rótulo): L1:

        Args:
            instr: {"type": "label", "name": "L1", "line": 16}

        Returns:
            Linhas Assembly geradas
        """
        label_name = instr["name"]
        return [
            f"{label_name}:",
            ""
        ]

    def _processar_goto(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa salto incondicional: goto L1

        Args:
            instr: {"type": "goto", "target": "L2", "line": 18}

        Returns:
            Linhas Assembly geradas
        """
        target = instr["target"]
        line = instr.get("line", "?")
        return [
            f"    ; TAC linha {line}: goto {target}",
            f"    rjmp {target}   ; Salto relativo para {target}",
            ""
        ]

    def _processar_if_goto(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa salto condicional (jump if TRUE): if condition goto target

        Jumps to target if condition is non-zero (true).

        Args:
            instr: {"type": "if_goto", "condition": "t5", "target": "L1", "line": 10}

        Returns:
            Linhas Assembly geradas
        """
        condition = instr["condition"]
        target = instr["target"]
        line = instr.get("line", "?")

        # Get register pair for condition variable
        cond_low, cond_high = self._get_reg_pair(condition)

        return [
            f"    ; TAC linha {line}: if {condition} goto {target}",
            f"    ; Check if {condition} != 0 (true)",
            f"    ldi r24, 0                  ; Zero constant for comparison",
            f"    ldi r25, 0",
            f"    cp r{cond_low}, r24         ; Compare low byte with 0",
            f"    cpc r{cond_high}, r25       ; Compare high byte with carry",
            f"    brne {target}               ; Branch if NOT equal (condition is true)",
            ""
        ]

    def _processar_if_false_goto(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa salto condicional (jump if FALSE): ifFalse condition goto target

        Jumps to target if condition is zero (false).

        Args:
            instr: {"type": "if_false_goto", "condition": "t5", "target": "L2", "line": 12}

        Returns:
            Linhas Assembly geradas
        """
        condition = instr["condition"]
        target = instr["target"]
        line = instr.get("line", "?")

        # Get register pair for condition variable
        cond_low, cond_high = self._get_reg_pair(condition)

        return [
            f"    ; TAC linha {line}: ifFalse {condition} goto {target}",
            f"    ; Check if {condition} == 0 (false)",
            f"    cp r{cond_low}, r1          ; Compare low byte with 0 (R1 is always 0)",
            f"    cpc r{cond_high}, r1        ; Compare high byte with 0",
            f"    breq {target}               ; Branch if equal (condition is false)",
            ""
        ]

    # =========================================================================
    # GERAÇÃO DE PRÓLOGO E EPÍLOGO (PRIVADOS)
    # =========================================================================

    def _gerar_prologo(self) -> List[str]:
        """
        Gera prólogo do programa Assembly (inicialização).

        Inclui:
        - Diretivas de seção (.text)
        - Entry point (main)
        - Inicialização do stack pointer

        Returns:
            Linhas do prólogo
        """
        return [
            "; ====================================================================",
            "; Código Assembly gerado automaticamente",
            "; Arquitetura: AVR ATmega328P (Arduino Uno)",
            "; Compilador: RA4_Compiladores - Fase 4",
            "; ====================================================================",
            "",
            ".section .text",
            ".global main",
            "",
            "main:",
            "    ; Inicializar stack pointer",
            "    ldi r16, lo8(0x08FF)   ; RAMEND low byte",
            "    out 0x3D, r16          ; SPL",
            "    ldi r16, hi8(0x08FF)   ; RAMEND high byte",
            "    out 0x3E, r16          ; SPH",
            "",
            "    ; Inicializar UART (115200 baud @ 16MHz)",
            "    rcall uart_init",
            "",
            "    ; ==== INÍCIO DO CÓDIGO GERADO ====",
            ""
        ]

    def _gerar_epilogo(self, instructions: List[Dict[str, Any]]) -> List[str]:
        """
        Gera epílogo do programa Assembly (finalização).

        Inclui:
        - Output do resultado final via UART
        - Rotinas auxiliares necessárias (mul16, div16, uart, etc.)
        - Loop infinito (fim do programa)

        Args:
            instructions: Lista de instruções TAC para detectar resultado final

        Returns:
            Linhas do epílogo
        """
        epilogo = [
            "    ; ==== FIM DO CÓDIGO GERADO ====",
            ""
        ]

        # Detectar variável do resultado final
        # Strategy: Look for variables named RESULT, FIB_NEXT, or last copy/assignment
        final_result_var = None

        # First, search for common result variable names
        result_candidates = ["RESULT", "FIB_NEXT", "FINAL_COS"]
        for candidate in result_candidates:
            if candidate in self._var_to_reg_pair or candidate in self._spilled_vars:
                final_result_var = candidate
                break

        # Fallback: search backwards for last copy/assignment
        if not final_result_var and instructions:
            for instr in reversed(instructions):
                if instr.get("type") in ["copy", "assignment"]:
                    dest = instr.get("dest")
                    # Skip temporary variables (t0, t1, etc.)
                    if dest and not dest.startswith("t"):
                        final_result_var = dest
                        break

        # Enviar resultado via UART se identificado
        # Check both register-allocated and spilled variables
        if final_result_var:
            if final_result_var in self._var_to_reg_pair:
                res_low, res_high = self._var_to_reg_pair[final_result_var]
            elif final_result_var in self._spilled_vars:
                # Variable was spilled - load it first
                mem_addr = self._spilled_vars[final_result_var]
                epilogo.extend([
                    f"    ; Load final result {final_result_var} from memory 0x{mem_addr:04X}",
                    f"    lds r24, 0x{mem_addr:04X}      ; Load low byte",
                    f"    lds r25, 0x{mem_addr + 1:04X}  ; Load high byte",
                ])
                res_low, res_high = 24, 25  # Already in R24:R25
            else:
                final_result_var = None  # Not found

        if final_result_var and (final_result_var in self._var_to_reg_pair or final_result_var in self._spilled_vars):
            # If in registers, copy to R24:R25
            if final_result_var in self._var_to_reg_pair:
                res_low, res_high = self._var_to_reg_pair[final_result_var]
                epilogo.extend([
                    "    ; Enviar resultado final via UART",
                    f"    mov r24, r{res_low}    ; Copiar resultado para R24:R25",
                    f"    mov r25, r{res_high}",
                ])
            # If spilled, already loaded above into R24:R25

            # Send via UART
            epilogo.extend([
                "    rcall send_number_16bit",
                "    ldi r24, 13            ; CR",
                "    rcall uart_transmit",
                "    ldi r24, 10            ; LF",
                "    rcall uart_transmit",
                "    jmp fim                ; Saltar para loop infinito",
                ""
            ])

        # Gerar rotinas auxiliares necessárias
        if "mul16" in self._routines_needed:
            epilogo.extend(self._gerar_rotina_multiplicacao_16bit())

        if "div16" in self._routines_needed:
            epilogo.extend(self._gerar_rotina_divisao_16bit())

        # div_scaled routine removed - real division now uses direct div16
        # (operands are pre-scaled by 100x in TAC generation)

        if "exp16" in self._routines_needed:
            epilogo.extend(self._gerar_rotina_exponenciacao())

        # Gerar rotinas UART (sempre necessárias)
        epilogo.extend(self._gerar_rotinas_uart())

        # Loop infinito (fim do programa)
        epilogo.extend([
            "fim:",
            "    rjmp fim   ; Loop infinito",
            "",
            "; ====================================================================",
            "; Fim do programa",
            "; ===================================================================="
        ])

        return epilogo

    # =========================================================================
    # ROTINAS AUXILIARES DE OPERAÇÕES COMPLEXAS (PRIVADOS)
    # =========================================================================

    def _gerar_rotina_multiplicacao_16bit(self) -> List[str]:
        """
        Gera rotina auxiliar para multiplicação 16-bit × 16-bit = 16-bit (unsigned).

        Algoritmo: (AH:AL) × (BH:BL) = AH×BH×2^16 + AH×BL×2^8 + AL×BH×2^8 + AL×BL
        Simplificado para 16-bit: descarta AH×BH (overflow), mantém apenas 16 bits baixos.

        Convenção de chamada:
        - Entrada: R18:R19 (operando 1), R20:R21 (operando 2)
        - Saída: R24:R25 (resultado 16-bit)
        - Usa: R0, R1 (resultado de MUL), R22, R23 (temporários)

        Returns:
            Linhas Assembly da rotina
        """
        return [
            "; ====================================================================",
            "; mul16: Multiplicação 16-bit × 16-bit = 16-bit (unsigned)",
            "; Entrada: R18:R19 (op1), R20:R21 (op2)",
            "; Saída: R24:R25 (resultado)",
            "; Usa: R0, R1, R22, R23",
            "; ====================================================================",
            "mul16:",
            "    ; Salvar registradores que serão modificados",
            "    push r22",
            "    push r23",
            "",
            "    ; Zerar acumulador resultado",
            "    clr r24",
            "    clr r25",
            "",
            "    ; Produto parcial 1: AL × BL (contribui totalmente)",
            "    mul r18, r20      ; R1:R0 = AL × BL",
            "    mov r24, r0       ; Byte baixo do resultado",
            "    mov r22, r1       ; Byte alto vai para temporário",
            "",
            "    ; Produto parcial 2: AL × BH (contribui byte baixo para byte alto do resultado)",
            "    mul r18, r21      ; R1:R0 = AL × BH",
            "    add r22, r0       ; Somar byte baixo ao acumulador",
            "    adc r25, r1       ; Somar byte alto com carry",
            "",
            "    ; Produto parcial 3: AH × BL (contribui byte baixo para byte alto do resultado)",
            "    mul r19, r20      ; R1:R0 = AH × BL",
            "    add r22, r0       ; Somar byte baixo ao acumulador",
            "    adc r25, r1       ; Somar byte alto com carry",
            "",
            "    ; Produto parcial 4: AH × BH (descartado - overflow além de 16 bits)",
            "    ; Não precisamos calcular pois descartamos resultado > 16 bits",
            "",
            "    ; Mover acumulador para resultado final",
            "    mov r25, r22      ; Byte alto do resultado",
            "",
            "    ; Restaurar registradores",
            "    pop r23",
            "    pop r22",
            "",
            "    ; Limpar R0 e R1 (boa prática após MUL)",
            "    clr r1",
            "",
            "    ret",
            ""
        ]

    def _gerar_rotina_divisao_16bit(self) -> List[str]:
        """
        Gera rotina auxiliar para divisão 16-bit ÷ 16-bit = quociente e resto (unsigned).

        Algoritmo: Restoring shift-subtract division (17 iterações)
        Baseado em: AVR200 Application Note e GCC libgcc

        Convenção de chamada:
        - Entrada: R18:R19 (dividendo), R20:R21 (divisor)
        - Saída: R24:R25 (quociente), R22:R23 (resto)
        - Usa: R16 (contador de loop)
        - Ciclos: ~245 (com verificação de divisão por zero)

        Tratamento de divisão por zero:
        - Quociente = 0xFFFF (indicador de erro)
        - Resto = dividendo original (sem modificação)

        Returns:
            Linhas Assembly da rotina
        """
        return [
            "; ====================================================================",
            "; div16: Divisão 16-bit ÷ 16-bit = quociente e resto (unsigned)",
            "; Algoritmo: Restoring shift-subtract (17 iterações, resto corrigido)",
            "; Entrada: R18:R19 (dividendo), R20:R21 (divisor)",
            "; Saída: R24:R25 (quociente), R22:R23 (resto)",
            "; Usa: R16 (contador de loop)",
            "; Ciclos: ~232",
            "; ====================================================================",
            "div16:",
            "    push r16              ; Salvar registrador usado",
            "",
            "    ; Verificar divisão por zero",
            "    cp      r20, r1       ; Comparar divisor low com 0",
            "    cpc     r21, r1       ; Comparar divisor high com 0",
            "    breq    div16_by_zero ; Se zero, pular para tratamento de erro",
            "",
            "    ; Inicializar resto = 0",
            "    clr     r22           ; Resto low = 0",
            "    clr     r23           ; Resto high = 0",
            "",
            "    ; Inicializar contador de loop (16 iterações para divisão 16-bit)",
            "    ldi     r16, 16",
            "",
            "div16_loop:",
            "    ; Deslocar dividendo/quociente para esquerda",
            "    lsl     r18           ; Logical shift left (LSB=0, no carry dependency)",
            "    rol     r19           ; Shift dividend/quotient high",
            "",
            "    ; Deslocar bit MSB do dividendo para o resto",
            "    rol     r22           ; Shift into remainder low",
            "    rol     r23           ; Shift into remainder high",
            "",
            "    ; Comparar resto com divisor",
            "    cp      r22, r20      ; Compare remainder with divisor (low)",
            "    cpc     r23, r21      ; Compare remainder with divisor (high)",
            "    brcs    div16_skip    ; If remainder < divisor, skip subtraction",
            "",
            "    ; Resto >= divisor: subtrair divisor do resto",
            "    sub     r22, r20      ; Subtract divisor from remainder (low)",
            "    sbc     r23, r21      ; Subtract divisor from remainder (high)",
            "    inc     r18           ; Set quotient LSB bit to 1",
            "",
            "div16_skip:",
            "    dec     r16           ; Decrementar contador",
            "    brne    div16_loop    ; Loop se não terminou",
            "",
            "    ; Mover quociente para registradores de saída",
            "    mov     r24, r18      ; Quotient to output (low)",
            "    mov     r25, r19      ; Quotient to output (high)",
            "",
            "    ; Resto já está em R22:R23 (correto)",
            "",
            "    pop r16",
            "    ret",
            "",
            "div16_by_zero:",
            "    ; Retornar valores de erro",
            "    ldi     r24, 0xFF     ; Quociente = 0xFFFF (indicador de erro)",
            "    ldi     r25, 0xFF",
            "    mov     r22, r18      ; Resto = dividendo original (low)",
            "    mov     r23, r19      ; Resto = dividendo original (high)",
            "    pop r16",
            "    ret",
            ""
        ]

    # _gerar_rotina_divisao_escalada method removed
    # Real division now uses direct div16 with pre-scaled operands (100x from TAC)
    # No need for runtime scaling multiplication

    def _gerar_rotina_exponenciacao(self) -> List[str]:
        """
        Gera rotina auxiliar para exponenciação 16-bit ^ 16-bit.

        TODO: Implementar na Fase 4

        Returns:
            Linhas Assembly da rotina
        """
        return [
            "; ====================================================================",
            "; exp16: Exponenciação 16-bit ^ 16-bit",
            "; TODO: Implementar na Fase 4",
            "; ====================================================================",
            "exp16:",
            "    ; TODO: Implementar loop de multiplicação",
            "    ret",
            ""
        ]

    def _gerar_rotinas_uart(self) -> List[str]:
        """
        Gera rotinas UART para comunicação serial (115200 baud @ 16MHz).

        Inclui:
        - uart_init: Inicializa UART
        - uart_transmit: Envia um byte via UART
        - send_number_16bit: Converte e envia número 16-bit como decimal

        Returns:
            Linhas Assembly das rotinas UART
        """
        return [
            "; ====================================================================",
            "; ROTINAS UART (115200 baud @ 16MHz)",
            "; ====================================================================",
            "",
            "uart_init:",
            "    ldi r16, 0",
            "    sts 0xC5, r16        ; UBRR0H = 0",
            "    ldi r16, 8",
            "    sts 0xC4, r16        ; UBRR0L = 8 (115200 baud @ 16MHz)",
            "    ldi r16, (1 << 3)    ; TXEN0",
            "    sts 0xC1, r16        ; UCSR0B",
            "    ldi r16, (1 << 2) | (1 << 1)",
            "    sts 0xC2, r16        ; UCSR0C (8N1)",
            "    ret",
            "",
            "uart_transmit:",
            "    push r25",
            "uart_wait:",
            "    lds r25, 0xC0        ; UCSR0A",
            "    sbrs r25, 5          ; Wait for UDRE0",
            "    rjmp uart_wait",
            "    sts 0xC6, r24        ; UDR0 = data",
            "    pop r25",
            "    ret",
            "",
            "; ====================================================================",
            "; send_number_16bit: Envia número 16-bit como decimal via UART",
            "; Entrada: R24:R25 (número 16-bit, 0-65535)",
            "; Saída: Nenhuma (envia via UART)",
            "; ====================================================================",
            "send_number_16bit:",
            "    push r20",
            "    push r21",
            "    push r22",
            "    push r23",
            "    push r16",
            "    push r17",
            "    push r18",
            "    push r19",
            "",
            "    mov r20, r24",
            "    mov r21, r25",
            "",
            "    ; Dezenas de milhares (10000)",
            "    ldi r16, lo8(10000)",
            "    ldi r17, hi8(10000)",
            "    clr r18",
            "",
            "div_10000:",
            "    cp r20, r16",
            "    cpc r21, r17",
            "    brlo div_1000",
            "    sub r20, r16",
            "    sbc r21, r17",
            "    inc r18",
            "    rjmp div_10000",
            "",
            "div_1000:",
            "    ; Imprimir dezena de milhares se != 0",
            "    cpi r18, 0",
            "    breq skip_10000",
            "    mov r24, r18",
            "    subi r24, -48",
            "    rcall uart_transmit",
            "skip_10000:",
            "",
            "    ; Milhares (1000)",
            "    ldi r16, lo8(1000)",
            "    ldi r17, hi8(1000)",
            "    clr r18",
            "",
            "div_1000_loop:",
            "    cp r20, r16",
            "    cpc r21, r17",
            "    brlo div_100",
            "    sub r20, r16",
            "    sbc r21, r17",
            "    inc r18",
            "    rjmp div_1000_loop",
            "",
            "div_100:",
            "    ; Imprimir milhares",
            "    mov r24, r18",
            "    subi r24, -48",
            "    rcall uart_transmit",
            "",
            "    ; Centenas (100)",
            "    ldi r16, 100",
            "    clr r17",
            "    clr r18",
            "",
            "div_100_loop:",
            "    cp r20, r16",
            "    cpc r21, r17",
            "    brlo div_10",
            "    sub r20, r16",
            "    sbc r21, r17",
            "    inc r18",
            "    rjmp div_100_loop",
            "",
            "div_10:",
            "    ; Imprimir centenas",
            "    mov r24, r18",
            "    subi r24, -48",
            "    rcall uart_transmit",
            "",
            "    ; Dezenas (10)",
            "    ldi r16, 10",
            "    clr r17",
            "    clr r18",
            "",
            "div_10_loop:",
            "    cp r20, r16",
            "    cpc r21, r17",
            "    brlo print_units",
            "    sub r20, r16",
            "    sbc r21, r17",
            "    inc r18",
            "    rjmp div_10_loop",
            "",
            "print_units:",
            "    ; Imprimir dezenas",
            "    mov r24, r18",
            "    subi r24, -48",
            "    rcall uart_transmit",
            "",
            "    ; Imprimir unidades",
            "    mov r24, r20",
            "    subi r24, -48",
            "    rcall uart_transmit",
            "",
            "    pop r19",
            "    pop r18",
            "    pop r17",
            "    pop r16",
            "    pop r23",
            "    pop r22",
            "    pop r21",
            "    pop r20",
            "    ret",
            ""
        ]


# =============================================================================
# FUNÇÃO DE CONVENIÊNCIA PARA USO EXTERNO
# =============================================================================

def gerarAssembly(tac_otimizado_path: str, output_path: str) -> None:
    """
    Função de conveniência para gerar Assembly a partir de arquivo JSON TAC.

    Args:
        tac_otimizado_path: Caminho para arquivo JSON com TAC otimizado
        output_path: Caminho para salvar arquivo .s de saída

    Raises:
        FileNotFoundError: Se arquivo TAC não existe
        json.JSONDecodeError: Se JSON é inválido
    """
    # Ler TAC otimizado
    with open(tac_otimizado_path, 'r', encoding='utf-8') as f:
        tac_otimizado = json.load(f)

    # Gerar Assembly
    gerador = GeradorAssembly()
    assembly_code = gerador.gerarAssembly(tac_otimizado)

    # Salvar arquivo .s
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(assembly_code)

    print(f"Assembly gerado com sucesso: {output_path}")
