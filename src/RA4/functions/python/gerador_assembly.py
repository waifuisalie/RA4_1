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
    - Suporte a 16-bit (8 pares de registradores: R0:R1 até R14:R15)
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
        # Usando registradores r16-r31 para compatibilidade com instruções LDI
        # Pares: R16:R17, R18:R19, R20:R21, R22:R23, R24:R25, R26:R27, R28:R29, R30:R31
        self._available_pairs: List[Tuple[int, int]] = [
            (16, 17), (18, 19), (20, 21), (22, 23), (24, 25), (26, 27), (28, 29), (30, 31)
        ]

        # Variáveis spilladas para memória: variável → endereço SRAM
        self._spilled_vars: Dict[str, int] = {}

        # Próximo endereço disponível para spill (inicia em RAMSTART = 0x0100)
        self._next_spill_addr: int = 0x0100

        # Acumulador de linhas Assembly geradas durante spill
        self._pending_spill_code: List[str] = []

        # Análise de vida útil das variáveis para melhor alocação
        self._var_lifetime: Dict[str, Tuple[int, int]] = {}  # var -> (first_use, last_use)

        # Rotinas auxiliares necessárias (serão geradas no epílogo)
        # Ex: {"mul16", "div16", "exp16"}
        self._routines_needed: set = set()

        # Lista completa de instruções TAC (para detectar resultado final)
        self._all_instructions: List[Dict[str, Any]] = []

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

        instructions = tac_otimizado["instructions"]
        self._all_instructions = instructions  # Armazenar para uso posterior

        # Análise de vida útil das variáveis para otimizar alocação
        self._analisar_vida_util(instructions)

        asm_lines: List[str] = []

        # 1. Gerar prólogo (inicialização do programa)
        asm_lines.extend(self._gerar_prologo())

        # 2. Processar cada instrução TAC
        for i, instr in enumerate(instructions):
            # Liberar registradores de variáveis mortas antes de processar nova instrução
            dead_code = self._liberar_registradores_mortos(i)
            asm_lines.extend(dead_code)

            asm_lines.extend(self._processar_instrucao(instr))

        # 3. Gerar epílogo (finalização do programa)
        asm_lines.extend(self._gerar_epilogo(instructions))

        return "\n".join(asm_lines)

    # =========================================================================
    # ANÁLISE DE VIDA ÚTIL DAS VARIÁVEIS
    # =========================================================================

    def _analisar_vida_util(self, instructions: List[Dict[str, Any]]) -> None:
        """
        Analisa a vida útil de cada variável TAC para otimizar alocação de registradores.

        Args:
            instructions: Lista de instruções TAC
        """
        self._var_lifetime.clear()

        for i, instr in enumerate(instructions):
            instr_type = instr.get("type")

            # Coletar variáveis usadas nesta instrução
            vars_used = set()

            if instr_type in ["assignment", "copy"]:
                vars_used.add(instr.get("dest", ""))
                source = instr.get("source", "")
                if not self._is_constant(source):
                    vars_used.add(source)

            elif instr_type == "binary_op":
                vars_used.add(instr.get("result", ""))
                vars_used.add(instr.get("operand1", ""))
                vars_used.add(instr.get("operand2", ""))

            elif instr_type in ["if_goto", "if_false_goto"]:
                vars_used.add(instr.get("condition", ""))

            # Atualizar vida útil para cada variável
            for var in vars_used:
                if var and not self._is_constant(var):
                    if var not in self._var_lifetime:
                        self._var_lifetime[var] = (i, i)
                    else:
                        first_use, _ = self._var_lifetime[var]
                        self._var_lifetime[var] = (first_use, i)

    def _liberar_registradores_mortos(self, current_instr_idx: int) -> List[str]:
        """
        Libera registradores de variáveis que não serão mais usadas.

        Args:
            current_instr_idx: Índice da instrução atual

        Returns:
            Lista de linhas Assembly para salvar variáveis que serão liberadas
        """
        asm_lines = []
        vars_to_free = []

        for var, (first_use, last_use) in self._var_lifetime.items():
            if last_use < current_instr_idx and var in self._var_to_reg_pair:
                # Variável morreu, podemos liberar o registrador
                reg_pair = self._var_to_reg_pair[var]
                self._available_pairs.append(reg_pair)
                del self._var_to_reg_pair[var]
                vars_to_free.append(var)

        if vars_to_free:
            asm_lines.append(f"    ; Liberando registradores de variáveis mortas: {', '.join(vars_to_free)}")
            asm_lines.append("")

        return asm_lines

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
        # Nota: target_pair já foi removido de _available_pairs pelo caller (_get_reg_pair)

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

        Se o registrador não suportar LDI (r0-r15), usa MOV via r16 como intermediário.

        Args:
            value: Valor da constante (int ou float)
            reg_low: Registrador para byte baixo
            reg_high: Registrador para byte alto

        Returns:
            Lista de linhas Assembly (comentário + instruções de carregamento)

        Note:
            Float de 16-bit (half-precision) será implementado em sub-issue 3.5
            Por enquanto, trata apenas inteiros
        """
        # TODO: Implementar conversão para float16 (IEEE 754 half-precision) no sub-issue 3.5
        # Por enquanto, assume inteiro
        int_value = int(value)

        low_byte = int_value & 0xFF
        high_byte = (int_value >> 8) & 0xFF

        # Verificar se registradores suportam LDI (apenas r16-r31)
        if reg_low >= 16 and reg_high >= 16:
            # Ambos os registradores suportam LDI
            return [
                f"    ldi r{reg_low}, {low_byte}   ; Constante {int_value} (low byte)",
                f"    ldi r{reg_high}, {high_byte}  ; Constante {int_value} (high byte)",
                ""
            ]
        else:
            # Pelo menos um registrador não suporta LDI - usar MOV via r16
            lines = [f"    ; Carregar constante {int_value} (usando mov via r16)"]

            # Carregar low byte
            if reg_low >= 16:
                lines.append(f"    ldi r{reg_low}, {low_byte}   ; Low byte")
            else:
                lines.extend([
                    f"    ldi r16, {low_byte}   ; Low byte via r16",
                    f"    mov r{reg_low}, r16"
                ])

            # Carregar high byte
            if reg_high >= 16:
                lines.append(f"    ldi r{reg_high}, {high_byte}  ; High byte")
            else:
                lines.extend([
                    f"    ldi r16, {high_byte}  ; High byte via r16",
                    f"    mov r{reg_high}, r16"
                ])

            lines.append("")
            return lines

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
        elif instr_type == "copy":
            return pending + self._processar_copy(instr)
        elif instr_type == "binary_op":
            return pending + self._processar_binary_op(instr)
        elif instr_type == "label":
            return pending + self._processar_label(instr)
        elif instr_type == "goto":
            return pending + self._processar_goto(instr)
        elif instr_type == "if_goto":
            return pending + self._processar_if_goto(instr)
        elif instr_type == "if_false_goto":
            return pending + self._processar_if_false_goto(instr)
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
            # Distinguir entre multiplicação inteira e real
            data_type = instr.get("data_type", "int")
            if data_type == "real":
                return self._processar_multiplicacao_real(instr)
            else:
                return self._processar_multiplicacao_inteira(instr)
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

    def _processar_multiplicacao_real(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa multiplicação 16-bit com re-normalização de escala.

        Quando multiplicando dois valores escalados (ambos 100x):
          (A * 100) * (B * 100) = (A * B) * 10,000

        Para manter escala 100x, dividimos por 100:
          result = (A * B * 10,000) / 100 = (A * B) * 100

        Exemplo: 50 * 50 = 2500, então 2500 / 100 = 25 (representa 0.5 * 0.5 = 0.25)

        Usa rotinas auxiliares mul16 e div16 que serão geradas no epílogo.
        Convenção: op1 em R0:R1, op2 em R2:R3, resultado em R4:R5

        Args:
            instr: Instrução TAC de multiplicação

        Returns:
            Linhas Assembly geradas
        """
        result = instr["result"]
        op1 = instr["operand1"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        # Registrar que precisamos das rotinas mul16 e div16
        self._routines_needed.add("mul16")
        self._routines_needed.add("div16")

        asm = [f"    ; TAC linha {line}: {result} = {op1} * {op2}"]

        # Obter registradores dos operandos
        op1_low, op1_high = self._get_reg_pair(op1)
        op2_low, op2_high = self._get_reg_pair(op2)
        res_low, res_high = self._get_reg_pair(result)

        asm.extend([
            f"    ; Multiplicação 16-bit com re-normalização de escala",
            f"    ; Preparar parâmetros para mul16",
            f"    mov r0, r{op1_low}",
            f"    mov r1, r{op1_high}",
            f"    mov r2, r{op2_low}",
            f"    mov r3, r{op2_high}",
            f"    rcall mul16              ; R4:R5 = op1 * op2 (scaled²)",
            f"    ; Re-normalize: divide by 100 to restore 100x scaling",
            f"    mov r0, r4",
            f"    mov r1, r5",
            f"    ldi r16, 100             ; Divide by scale factor",
            f"    mov r2, r16",
            f"    ldi r16, 0",
            f"    mov r3, r16",
            f"    rcall div16              ; R4:R5 = result (scaled¹)",
            f"    mov r{res_low}, r4",
            f"    mov r{res_high}, r5",
            ""
        ])

        return asm

    def _processar_multiplicacao_inteira(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa multiplicação inteira 16-bit sem re-normalização de escala.

        Para inteiros, multiplicação é direta: result = op1 * op2

        Usa rotina auxiliar mul16.
        Convenção: op1 em R0:R1, op2 em R2:R3, resultado em R4:R5

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
            f"    ; Multiplicação 16-bit inteira",
            f"    mov r0, r{op1_low}",
            f"    mov r1, r{op1_high}",
            f"    mov r2, r{op2_low}",
            f"    mov r3, r{op2_high}",
            f"    rcall mul16              ; R4:R5 = op1 * op2",
            f"    mov r{res_low}, r4",
            f"    mov r{res_high}, r5",
            ""
        ])

        return asm

    def _processar_divisao_16bit(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa divisão inteira 16-bit: result = op1 / op2

        Usa rotina auxiliar div16 que retorna quociente em R4:R5 e resto em R6:R7.
        Convenção: op1 em R0:R1 (dividendo), op2 em R2:R3 (divisor), quociente em R4:R5

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
            f"    mov r0, r{op1_low}   ; Dividendo (low)",
            f"    mov r1, r{op1_high}  ; Dividendo (high)",
            f"    mov r2, r{op2_low}   ; Divisor (low)",
            f"    mov r3, r{op2_high}  ; Divisor (high)",
            f"    rcall div16           ; Chamar rotina (quociente em R4:R5, resto em R6:R7)",
            f"    mov r{res_low}, r4   ; Copiar quociente",
            f"    mov r{res_high}, r5",
            ""
        ])

        return asm

    def _processar_modulo_16bit(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa módulo 16-bit: result = op1 % op2

        Usa mesma rotina div16, mas retorna o RESTO (R6:R7) ao invés do quociente.
        Convenção: op1 em R0:R1 (dividendo), op2 em R2:R3 (divisor), resto em R6:R7

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
            f"    mov r0, r{op1_low}   ; Dividendo (low)",
            f"    mov r1, r{op1_high}  ; Dividendo (high)",
            f"    mov r2, r{op2_low}   ; Divisor (low)",
            f"    mov r3, r{op2_high}  ; Divisor (high)",
            f"    rcall div16           ; Chamar rotina (quociente em R4:R5, resto em R6:R7)",
            f"    mov r{res_low}, r6   ; Copiar RESTO (não quociente!)",
            f"    mov r{res_high}, r7",
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
            f"    mov r0, r{op1_low}      ; Dividendo",
            f"    mov r1, r{op1_high}",
            f"    ldi r16, 100             ; Scale factor (100)",
            f"    mov r2, r16",
            f"    ldi r16, 0",
            f"    mov r3, r16",
            f"    rcall mul16              ; R4:R5 = op1 * 100",
            f"    ; Step 2: Divide scaled dividend by divisor",
            f"    mov r0, r4             ; Move result to dividend registers",
            f"    mov r1, r5",
            f"    mov r2, r{op2_low}      ; Divisor",
            f"    mov r3, r{op2_high}",
            f"    rcall div16              ; R4:R5 = (op1 * 100) / op2",
            f"    mov r{res_low}, r4      ; Copy result",
            f"    mov r{res_high}, r5",
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

        lines = [f"{label_name}:"]

        # Se for o label L1 (fim do programa), adicionar impressão do resultado
        if label_name == "L1":
            # Procurar especificamente pela variável FINAL_RESULT
            result_var = "FINAL_RESULT"
            
            if result_var and result_var in self._var_to_reg_pair:
                res_low, res_high = self._var_to_reg_pair[result_var]
                lines.extend([
                    "    ; Imprimir resultado final via UART",
                    f"    mov r4, r{res_low}    ; Copiar {result_var} para parâmetros da função",
                    f"    mov r5, r{res_high}",
                    "    rcall send_number_16bit",
                    ""
                ])

        lines.append("")
        return lines

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
        Uses jmp for long jumps to avoid AVR branch distance limitations.

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
            f"    ldi r18, 0                  ; Zero constant for comparison",
            f"    mov r2, r18",
            f"    mov r3, r18",
            f"    cp r{cond_low}, r2         ; Compare low byte with 0",
            f"    cpc r{cond_high}, r3       ; Compare high byte with carry",
            f"    breq .+2              ; If equal (false), skip jmp",
            f"    jmp {target}                ; If not equal (true), jump to {target}",
            ""
        ]

    def _processar_if_false_goto(self, instr: Dict[str, Any]) -> List[str]:
        """
        Processa salto condicional (jump if FALSE): ifFalse condition goto target

        Jumps to target if condition is zero (false).
        Uses jmp for long jumps to avoid AVR branch distance limitations.

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
            f"    ldi r18, 0                  ; Zero constant for comparison",
            f"    mov r2, r18",
            f"    mov r3, r18",
            f"    cp r{cond_low}, r2         ; Compare low byte with 0",
            f"    cpc r{cond_high}, r3       ; Compare high byte with carry",
            f"    brne .+2              ; If not equal (true), skip jmp",
            f"    jmp {target}                ; If equal (false), jump to {target}",
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
            "    ldi r16, 0xFF   ; RAMEND low byte",
            "    out 0x3D, r16          ; SPL",
            "    ldi r16, 0x08   ; RAMEND high byte",
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

        # Detectar variável do resultado final (última instrução copy/assignment)
        final_result_var = None
        if instructions:
            last_instr = instructions[-1]
            if last_instr.get("type") in ["copy", "assignment"]:
                final_result_var = last_instr.get("dest")

        # Enviar resultado via UART se identificado
        if final_result_var and final_result_var in self._var_to_reg_pair:
            res_low, res_high = self._var_to_reg_pair[final_result_var]
            epilogo.extend([
                "    ; Enviar resultado final via UART",
                f"    mov r4, r{res_low}    ; Copiar resultado para R4:R5",
                f"    mov r5, r{res_high}",
                "    rcall send_number_16bit",
                "    ldi r16, 13            ; CR",
                "    mov r0, r16",
                "    rcall uart_transmit",
                "    ldi r16, 10            ; LF",
                "    mov r0, r16",
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
            "; Entrada: R0:R1 (op1), R2:R3 (op2)",
            "; Saída: R4:R5 (resultado)",
            "; Usa: R6, R7, R8, R9",
            "; ====================================================================",
            "mul16:",
            "    ; Salvar registradores que serão modificados",
            "    push r8",
            "    push r9",
            "",
            "    ; Zerar acumulador resultado",
            "    clr r4",
            "    clr r5",
            "",
            "    ; Produto parcial 1: AL × BL (contribui totalmente)",
            "    mul r0, r2      ; R1:R0 = AL × BL",
            "    mov r4, r0       ; Byte baixo do resultado",
            "    mov r6, r1       ; Byte alto vai para temporário",
            "",
            "    ; Produto parcial 2: AL × BH (contribui byte baixo para byte alto do resultado)",
            "    mul r0, r3      ; R1:R0 = AL × BH",
            "    add r6, r0       ; Somar byte baixo ao acumulador",
            "    adc r5, r1       ; Somar byte alto com carry",
            "",
            "    ; Produto parcial 3: AH × BL (contribui byte baixo para byte alto do resultado)",
            "    mul r1, r2      ; R1:R0 = AH × BL",
            "    add r6, r0       ; Somar byte baixo ao acumulador",
            "    adc r5, r1       ; Somar byte alto com carry",
            "",
            "    ; Produto parcial 4: AH × BH (descartado - overflow além de 16 bits)",
            "    ; Não precisamos calcular pois descartamos resultado > 16 bits",
            "",
            "    ; Mover acumulador para resultado final",
            "    mov r5, r6      ; Byte alto do resultado",
            "",
            "    ; Restaurar registradores",
            "    pop r9",
            "    pop r8",
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
        - Entrada: R0:R1 (dividendo), R2:R3 (divisor)
        - Saída: R4:R5 (quociente), R6:R7 (resto)
        - Usa: R8 (contador de loop)
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
            "; Entrada: R0:R1 (dividendo), R2:R3 (divisor)",
            "; Saída: R4:R5 (quociente), R6:R7 (resto)",
            "; Usa: R8 (contador de loop)",
            "; Ciclos: ~232",
            "; ====================================================================",
            "div16:",
            "    push r8              ; Salvar registrador usado",
            "",
            "    ; Verificar divisão por zero",
            "    cp      r2, r1       ; Comparar divisor low com 0",
            "    cpc     r3, r1       ; Comparar divisor high com 0",
            "    breq    div16_by_zero ; Se zero, pular para tratamento de erro",
            "",
            "    ; Inicializar resto = 0",
            "    clr     r6           ; Resto low = 0",
            "    clr     r7           ; Resto high = 0",
            "",
            "    ; Inicializar contador de loop (16 iterações para divisão 16-bit)",
            "    ldi     r16, 16",
            "    mov     r8, r16",
            "",
            "div16_loop:",
            "    ; Deslocar dividendo/quociente para esquerda",
            "    lsl     r0           ; Logical shift left (LSB=0, no carry dependency)",
            "    rol     r1           ; Shift dividend/quotient high",
            "",
            "    ; Deslocar bit MSB do dividendo para o resto",
            "    rol     r6           ; Shift into remainder low",
            "    rol     r7           ; Shift into remainder high",
            "",
            "    ; Comparar resto com divisor",
            "    cp      r6, r2      ; Compare remainder with divisor (low)",
            "    cpc     r7, r3      ; Compare remainder with divisor (high)",
            "    brcs    div16_skip    ; If remainder < divisor, skip subtraction",
            "",
            "    ; Resto >= divisor: subtrair divisor do resto",
            "    sub     r6, r2      ; Subtract divisor from remainder (low)",
            "    sbc     r7, r3      ; Subtract divisor from remainder (high)",
            "    inc     r0           ; Set quotient LSB bit to 1",
            "",
            "div16_skip:",
            "    dec     r8           ; Decrementar contador",
            "    brne    div16_loop    ; Loop se não terminou",
            "",
            "    ; Mover quociente para registradores de saída",
            "    mov     r4, r0      ; Quotient to output (low)",
            "    mov     r5, r1      ; Quotient to output (high)",
            "",
            "    ; Resto já está em R6:R7 (correto)",
            "",
            "    pop r8",
            "    ret",
            "",
            "div16_by_zero:",
            "    ; Retornar valores de erro",
            "    ldi     r16, 0xFF     ; Quociente = 0xFFFF (indicador de erro)",
            "    mov     r4, r16",
            "    mov     r5, r16",
            "    mov     r6, r0      ; Resto = dividendo original (low)",
            "    mov     r7, r1      ; Resto = dividendo original (high)",
            "    pop r8",
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
            "    push r1",
            "uart_wait:",
            "    lds r1, 0xC0        ; UCSR0A",
            "    sbrs r1, 5          ; Wait for UDRE0",
            "    rjmp uart_wait",
            "    sts 0xC6, r0        ; UDR0 = data",
            "    pop r1",
            "    ret",
            "",
            "; ====================================================================",
            "; send_number_16bit: Envia número 16-bit como decimal via UART",
            "; Entrada: R4:R5 (número 16-bit, 0-65535)",
            "; Saída: Nenhuma (envia via UART)",
            "; ====================================================================",
            "send_number_16bit:",
            "    push r6",
            "    push r7",
            "    push r8",
            "    push r9",
            "    push r10",
            "    push r11",
            "    push r12",
            "    push r13",
            "    push r16",
            "",
            "    mov r6, r4",
            "    mov r7, r5",
            "",
            "    ; Dezenas de milhares (10000)",
            "    ldi r16, 16",
            "    mov r8, r16",
            "    ldi r16, 39",
            "    mov r9, r16",
            "    clr r10",
            "",
            "div_10000:",
            "    cp r6, r8",
            "    cpc r7, r9",
            "    brlo div_1000",
            "    sub r6, r8",
            "    sbc r7, r9",
            "    inc r10",
            "    rjmp div_10000",
            "",
            "div_1000:",
            "    ; Imprimir dezena de milhares se != 0",
            "    ldi r16, 0",
            "    cp r10, r16",
            "    breq skip_10000",
            "    mov r0, r10",
            "    ldi r16, 48",
            "    add r0, r16",
            "    rcall uart_transmit",
            "skip_10000:",
            "",
            "    ; Milhares (1000)",
            "    ldi r16, 232",
            "    mov r8, r16",
            "    ldi r16, 3",
            "    mov r9, r16",
            "    clr r10",
            "",
            "div_1000_loop:",
            "    cp r6, r8",
            "    cpc r7, r9",
            "    brlo div_100",
            "    sub r6, r8",
            "    sbc r7, r9",
            "    inc r10",
            "    rjmp div_1000_loop",
            "",
            "div_100:",
            "    ; Imprimir milhares",
            "    mov r0, r10",
            "    ldi r16, 48",
            "    add r0, r16",
            "    rcall uart_transmit",
            "",
            "    ; Centenas (100)",
            "    ldi r16, 100",
            "    mov r8, r16",
            "    clr r9",
            "    clr r10",
            "",
            "div_100_loop:",
            "    cp r6, r8",
            "    cpc r7, r9",
            "    brlo div_10",
            "    sub r6, r8",
            "    sbc r7, r9",
            "    inc r10",
            "    rjmp div_100_loop",
            "",
            "div_10:",
            "    ; Imprimir centenas",
            "    mov r0, r10",
            "    ldi r16, 48",
            "    add r0, r16",
            "    rcall uart_transmit",
            "",
            "    ; Dezenas (10)",
            "    ldi r16, 10",
            "    mov r8, r16",
            "    clr r9",
            "    clr r10",
            "",
            "div_10_loop:",
            "    cp r6, r8",
            "    cpc r7, r9",
            "    brlo print_units",
            "    sub r6, r8",
            "    sbc r7, r9",
            "    inc r10",
            "    rjmp div_10_loop",
            "",
            "print_units:",
            "    ; Imprimir dezenas",
            "    mov r0, r10",
            "    ldi r16, 48",
            "    add r0, r16",
            "    rcall uart_transmit",
            "",
            "    ; Imprimir unidades",
            "    mov r0, r6",
            "    ldi r16, 48",
            "    add r0, r16",
            "    rcall uart_transmit",
            "",
            "    pop r13",
            "    pop r12",
            "    pop r11",
            "    pop r10",
            "    pop r9",
            "    pop r8",
            "    pop r7",
            "    pop r6",
            "    pop r16",
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
