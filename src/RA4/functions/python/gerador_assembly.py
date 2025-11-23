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
        """Inicializa o gerador com estruturas de alocação de registradores."""
        # Mapeamento: variável TAC → par de registradores (low, high)
        # Exemplo: {"t0": (16, 17), "t1": (18, 19)}
        self._var_to_reg_pair: Dict[str, Tuple[int, int]] = {}

        # Pares de registradores 16-bit disponíveis para temporários
        # R16:R17, R18:R19, R20:R21, R22:R23
        self._available_pairs: List[Tuple[int, int]] = [
            (16, 17),
            (18, 19),
            (20, 21),
            (22, 23)
        ]

        # Variáveis spilladas para memória: variável → endereço SRAM
        self._spilled_vars: Dict[str, int] = {}

        # Próximo endereço disponível para spill (inicia em RAMSTART = 0x0100)
        self._next_spill_addr: int = 0x0100

        # Acumulador de linhas Assembly geradas durante spill
        self._pending_spill_code: List[str] = []

        # Rotinas auxiliares necessárias (serão geradas no epílogo)
        # Ex: {"mul16", "div16", "exp16"}
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
        for instr in tac_otimizado["instructions"]:
            asm_lines.extend(self._processar_instrucao(instr))

        # 3. Gerar epílogo (finalização do programa)
        asm_lines.extend(self._gerar_epilogo())

        return "\n".join(asm_lines)

    # =========================================================================
    # MÉTODOS DE ALOCAÇÃO DE REGISTRADORES (PRIVADOS)
    # =========================================================================

    def _get_reg_pair(self, var_name: str) -> Tuple[int, int]:
        """
        Obtém par de registradores para variável TAC (alocação lazy on-demand).

        Estratégia:
        1. Se variável já tem registrador alocado → retorna o existente
        2. Se variável está spillada na memória → aloca novo par e carrega
        3. Se há par disponível → aloca
        4. Se não há pares disponíveis → faz spill FIFO e tenta novamente

        Args:
            var_name: Nome da variável TAC (ex: "t0", "t1", "MEM")

        Returns:
            Tupla (reg_low, reg_high) representando par de registradores
            Exemplo: (16, 17) para R16:R17
        """
        # Caso 1: Variável já tem registrador alocado
        if var_name in self._var_to_reg_pair:
            return self._var_to_reg_pair[var_name]

        # Caso 2: Variável está spillada, precisa carregar de volta
        if var_name in self._spilled_vars:
            # Aloca novo par primeiro
            if self._available_pairs:
                pair = self._available_pairs.pop(0)
            else:
                # Precisa fazer spill para liberar par
                spill_code = self._spill_oldest_variable()
                self._pending_spill_code.extend(spill_code)
                pair = self._available_pairs.pop(0)

            # Gera código de load e atualiza mapeamento
            load_code = self._load_from_spill(var_name, pair)
            self._pending_spill_code.extend(load_code)
            return pair

        # Caso 3: Alocar novo par (primeira vez que variável é usada)
        if self._available_pairs:
            pair = self._available_pairs.pop(0)
            self._var_to_reg_pair[var_name] = pair
            return pair

        # Caso 4: Sem registradores disponíveis - fazer spill FIFO
        spill_code = self._spill_oldest_variable()
        self._pending_spill_code.extend(spill_code)
        return self._get_reg_pair(var_name)  # Retry após liberar

    def _spill_oldest_variable(self) -> List[str]:
        """
        Spilla a variável mais antiga (FIFO) da memória para liberar um par de registradores.

        Estratégia FIFO: Remove a primeira variável alocada (mais antiga).
        Gera código Assembly para salvar o conteúdo atual do registrador na SRAM.

        Returns:
            Lista de linhas Assembly para o spill (comentários + instruções sts)

        Raises:
            RuntimeError: Se não há variáveis para spillar (não deveria acontecer)
        """
        if not self._var_to_reg_pair:
            raise RuntimeError("Tentativa de spill sem variáveis alocadas!")

        # Seleciona primeira variável alocada (FIFO - First In First Out)
        victim_var = list(self._var_to_reg_pair.keys())[0]
        reg_low, reg_high = self._var_to_reg_pair[victim_var]

        # Alocar endereço de memória SRAM (2 bytes para 16-bit)
        mem_addr = self._next_spill_addr
        self._next_spill_addr += 2  # Incrementa para próxima variável

        # Gerar código Assembly para spill
        asm_lines = [
            f"    ; Spill {victim_var} (r{reg_low}:r{reg_high}) -> 0x{mem_addr:04X}",
            f"    sts 0x{mem_addr:04X}, r{reg_low}      ; Store low byte",
            f"    sts 0x{mem_addr + 1:04X}, r{reg_high}  ; Store high byte",
            ""
        ]

        # Atualizar estruturas de dados
        self._spilled_vars[victim_var] = mem_addr
        del self._var_to_reg_pair[victim_var]
        self._available_pairs.append((reg_low, reg_high))

        return asm_lines

    def _load_from_spill(self, var_name: str, target_pair: Tuple[int, int]) -> List[str]:
        """
        Carrega variável spillada de volta da memória SRAM para registrador.

        Args:
            var_name: Nome da variável a ser carregada
            target_pair: Par de registradores destino (reg_low, reg_high)

        Returns:
            Lista de linhas Assembly para o load (comentários + instruções lds)

        Raises:
            KeyError: Se variável não está spillada
        """
        if var_name not in self._spilled_vars:
            raise KeyError(f"Variável {var_name} não está spillada!")

        mem_addr = self._spilled_vars[var_name]
        reg_low, reg_high = target_pair

        asm_lines = [
            f"    ; Load {var_name} de 0x{mem_addr:04X} -> r{reg_low}:r{reg_high}",
            f"    lds r{reg_low}, 0x{mem_addr:04X}      ; Load low byte",
            f"    lds r{reg_high}, 0x{mem_addr + 1:04X}  ; Load high byte",
            ""
        ]

        # Atualizar estruturas de dados
        del self._spilled_vars[var_name]
        self._var_to_reg_pair[var_name] = target_pair
        self._available_pairs.remove(target_pair)

        return asm_lines

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

        # Limpar código pendente de spill antes de processar nova instrução
        pending = self._pending_spill_code.copy()
        self._pending_spill_code.clear()

        if instr_type == "assignment":
            return pending + self._processar_assignment(instr)
        elif instr_type == "binary_op":
            return pending + self._processar_binary_op(instr)
        elif instr_type == "label":
            return pending + self._processar_label(instr)
        elif instr_type == "goto":
            return pending + self._processar_goto(instr)
        else:
            # TODO: Implementar outros tipos de instrução nos próximos sub-issues
            return pending + [f"    ; TODO: Implementar tipo '{instr_type}'", ""]

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
            # Divisão real - deferred para Sub-issue 3.5 (fixed-point)
            line = instr.get("line", "?")
            return [
                f"    ; TAC linha {line}: {instr['result']} = {instr['operand1']} | {instr['operand2']}",
                f"    ; TODO: Divisão real (|) - Implementar em Sub-issue 3.5 (fixed-point)",
                ""
            ]
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

        # Obter registradores dos operandos
        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        asm.extend([
            f"    ; Soma 16-bit: {result} = {op1} + {op2}",
            f"    add r{op1_low}, r{op2_low}   ; Low byte com carry",
            f"    adc r{op1_high}, r{op2_high} ; High byte com carry",
            f"    mov r{res_low}, r{op1_low}   ; Resultado em {result}",
            f"    mov r{res_high}, r{op1_high}",
            ""
        ])

        return asm

    def _processar_subtracao_16bit(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa subtração 16-bit: result = op1 - op2

        Usa instruções SUB (low byte) e SBC (high byte com carry/borrow).

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

        # Obter registradores dos operandos
        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        asm.extend([
            f"    ; Subtração 16-bit: {result} = {op1} - {op2}",
            f"    sub r{op1_low}, r{op2_low}   ; Low byte com borrow",
            f"    sbc r{op1_high}, r{op2_high} ; High byte com borrow",
            f"    mov r{res_low}, r{op1_low}   ; Resultado em {result}",
            f"    mov r{res_high}, r{op1_high}",
            ""
        ])

        return asm

    def _processar_multiplicacao_16bit(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa multiplicação 16-bit: result = op1 * op2

        Usa rotina auxiliar mul16 que será gerada no epílogo.
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

        # Registrar que precisamos da rotina mul16
        self._routines_needed.add("mul16")

        asm = [f"    ; TAC linha {line}: {result} = {op1} * {op2}"]

        # Obter registradores dos operandos
        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        asm.extend([
            f"    ; Multiplicação 16-bit: {result} = {op1} * {op2}",
            f"    ; Preparar parâmetros para mul16",
            f"    mov r18, r{op1_low}   ; Parâmetro 1 (low)",
            f"    mov r19, r{op1_high}  ; Parâmetro 1 (high)",
            f"    mov r20, r{op2_low}   ; Parâmetro 2 (low)",
            f"    mov r21, r{op2_high}  ; Parâmetro 2 (high)",
            f"    rcall mul16           ; Chamar rotina (resultado em R24:R25)",
            f"    mov r{res_low}, r24   ; Copiar resultado",
            f"    mov r{res_high}, r25",
            ""
        ])

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
            "    ; ==== INÍCIO DO CÓDIGO GERADO ====",
            ""
        ]

    def _gerar_epilogo(self) -> List[str]:
        """
        Gera epílogo do programa Assembly (finalização).

        Inclui:
        - Rotinas auxiliares necessárias (mul16, div16, etc.)
        - Loop infinito (fim do programa)

        Returns:
            Linhas do epílogo
        """
        epilogo = [
            "    ; ==== FIM DO CÓDIGO GERADO ====",
            ""
        ]

        # Gerar rotinas auxiliares necessárias
        if "mul16" in self._routines_needed:
            epilogo.extend(self._gerar_rotina_multiplicacao_16bit())

        if "div16" in self._routines_needed:
            epilogo.extend(self._gerar_rotina_divisao_16bit())

        if "exp16" in self._routines_needed:
            epilogo.extend(self._gerar_rotina_exponenciacao())

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
            "    ; Inicializar contador de loop (17 iterações para quociente correto)",
            "    ldi     r16, 17",
            "",
            "div16_loop:",
            "    ; Deslocar dividendo/quociente para esquerda",
            "    rol     r18           ; Shift dividend/quotient low",
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
            "",
            "div16_skip:",
            "    dec     r16           ; Decrementar contador",
            "    brne    div16_loop    ; Loop se não terminou",
            "",
            "    ; Corrigir resto (desfazer o 17º shift)",
            "    lsr     r23           ; Shift right high byte",
            "    ror     r22           ; Rotate right low byte (recebe carry de r23)",
            "",
            "    ; Complementar quociente (agora em R18:R19)",
            "    com     r18           ; Complement quotient low",
            "    com     r19           ; Complement quotient high",
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
