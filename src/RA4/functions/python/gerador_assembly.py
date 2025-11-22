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

        Note:
            Implementação completa de operadores será em sub-issue 3.4
        """
        result = instr["result"]
        op1 = instr["operand1"]
        operator = instr["operator"]
        op2 = instr["operand2"]
        line = instr.get("line", "?")

        asm = [f"    ; TAC linha {line}: {result} = {op1} {operator} {op2}"]

        # TODO: Implementar operadores completos no sub-issue 3.4
        # Por enquanto, apenas soma básica
        if operator == "+":
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
        else:
            asm.append(f"    ; TODO: Implementar operador '{operator}' no sub-issue 3.4")
            asm.append("")

        return asm

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
        - Loop infinito (fim do programa)

        Returns:
            Linhas do epílogo
        """
        return [
            "    ; ==== FIM DO CÓDIGO GERADO ====",
            "",
            "fim:",
            "    rjmp fim   ; Loop infinito",
            "",
            "; ====================================================================",
            "; Fim do programa",
            "; ===================================================================="
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
