#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

# ============================================================================
# LEGACY CODE - RA1 PHASE ONLY (Assembly Generation)
# ============================================================================
# Geração de código Assembly RISC-V para Arduino Uno
# Não usado em RA2/RA3+ - mantido apenas para referência histórica do RA1
# ============================================================================

from typing import List

# -----------------------------
# Helpers de análise de tokens
# -----------------------------

# Lista de todos os operadores e comandos especiais
OPERADORES = ['+', '-', '*', '/', '%', '^', '<', '>', '==', '<=', '>=', '!=', '!', '||', '&&']
COMANDOS_ESPECIAIS = ['RES', 'WHILE', 'FOR', 'IFELSE']

def is_number(token: str) -> bool:
    # Ignora operadores e comandos especiais silenciosamente
    if token in OPERADORES or token in COMANDOS_ESPECIAIS:
        return False
    try:
        float(token)
        return True
    except ValueError:
        return False

def is_integer(token: str) -> bool:
    # Ignora operadores e comandos especiais silenciosamente
    if token in OPERADORES or token in COMANDOS_ESPECIAIS:
        return False
    try:
        val = float(token)
        return val == int(val)
    except ValueError:
        return False

def is_variable_mem(token: str) -> bool:
    # Qualquer sequência de caracteres que não seja um operador ou comando especial
    return (token not in OPERADORES and 
            token not in COMANDOS_ESPECIAIS and 
            not is_number(token))

def is_comparison_operator(token: str) -> bool:
    return token in ['<', '>', '==', '<=', '>=', '!=']

def is_logical_operator(token: str) -> bool:
    return token in ['!', '||', '&&']

def is_control_structure(token: str) -> bool:
    return token in ['WHILE', 'FOR', 'IFELSE']

# ---------------------------------
# Geração de PUSH (público + interno)
# ---------------------------------

def _gerar_push_int_com_debug(valor: int) -> List[str]:
    return [
        f"    ; Push {valor} para a pilha",
        f"    ldi r16, {valor & 0xFF}      ; Byte baixo",
        f"    ldi r17, {(valor >> 8) & 0xFF} ; Byte alto",
        "    rcall stack_push_int",
        ""
    ]

def gerar_push_int(valor: int) -> List[str]:
    """Wrapper público (não recursivo)."""
    return _gerar_push_int_com_debug(valor)

# ---------------------------------
# Geração de operações aritméticas
# ---------------------------------

def _operacao_map() -> dict[str, List[str]]:
    return {
        # Operadores aritméticos existentes
        '+': [
            "    ; Operação de soma",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Soma 16-bit",
            "    add r16, r18",
            "    adc r17, r19",
            "",
            "    rcall stack_push_int",
            ""
        ],
        '-': [
            "    ; Operação de subtração",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Subtração 16-bit",
            "    sub r16, r18",
            "    sbc r17, r19",
            "",
            "    rcall stack_push_int",
            ""
        ],
        '*': [
            "    ; Operação de multiplicação",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Multiplicação 16-bit",
            "    rcall multiply_int",
            "",
            "    rcall stack_push_int",
            ""
        ],
        '/': [
            "    ; Operação de divisão",
            "    rcall stack_pop_int      ; Remove divisor",
            "    mov r18, r16             ; guarda divisor",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove dividendo",
            "",
            "    ; Divisão 16-bit",
            "    rcall divide_int",
            "",
            "    rcall stack_push_int",
            ""
        ],
        '%': [
            "    ; Operação de módulo",
            "    rcall stack_pop_int      ; Remove divisor",
            "    mov r18, r16             ; guarda divisor",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove dividendo",
            "",
            "    ; Módulo 16-bit",
            "    rcall modulo_int",
            "",
            "    rcall stack_push_int",
            ""
        ],
        '^': [
            "    ; Operação de potência",
            "    rcall stack_pop_int      ; Remove expoente",
            "    mov r18, r16             ; guarda expoente",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove base",
            "",
            "    ; Potência 16-bit",
            "    rcall power_int",
            "",
            "    rcall stack_push_int",
            ""
        ],
        
        # Novos operadores de comparação
        '<': [
            "    ; Operação menor que",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Comparação menor que",
            "    cp r16, r18              ; Compara low bytes",
            "    cpc r17, r19             ; Compara high bytes com carry",
            "    brlt _menor_true         ; Branch if less than",
            "    ldi r16, 0               ; False",
            "    ldi r17, 0",
            "    rjmp _menor_fim",
            "_menor_true:",
            "    ldi r16, 1               ; True",
            "    ldi r17, 0",
            "_menor_fim:",
            "    rcall stack_push_int",
            ""
        ],
        '>': [
            "    ; Operação maior que",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Comparação maior que",
            "    cp r16, r18              ; Compara low bytes",
            "    cpc r17, r19             ; Compara high bytes com carry",
            "    brgt _maior_true         ; Branch if greater than",
            "    ldi r16, 0               ; False",
            "    ldi r17, 0",
            "    rjmp _maior_fim",
            "_maior_true:",
            "    ldi r16, 1               ; True",
            "    ldi r17, 0",
            "_maior_fim:",
            "    rcall stack_push_int",
            ""
        ],
        '==': [
            "    ; Operação igual a",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Comparação de igualdade",
            "    cp r16, r18              ; Compara low bytes",
            "    brne _igual_false        ; Se diferentes, é falso",
            "    cp r17, r19              ; Compara high bytes",
            "    brne _igual_false        ; Se diferentes, é falso",
            "    ldi r16, 1               ; True",
            "    ldi r17, 0",
            "    rjmp _igual_fim",
            "_igual_false:",
            "    ldi r16, 0               ; False",
            "    ldi r17, 0",
            "_igual_fim:",
            "    rcall stack_push_int",
            ""
        ],
        '<=': [
            "    ; Operação menor ou igual a",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Comparação menor ou igual",
            "    cp r16, r18              ; Compara low bytes",
            "    cpc r17, r19             ; Compara high bytes com carry",
            "    brle _menor_igual_true   ; Branch if less or equal",
            "    ldi r16, 0               ; False",
            "    ldi r17, 0",
            "    rjmp _menor_igual_fim",
            "_menor_igual_true:",
            "    ldi r16, 1               ; True",
            "    ldi r17, 0",
            "_menor_igual_fim:",
            "    rcall stack_push_int",
            ""
        ],
        '>=': [
            "    ; Operação maior ou igual a",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Comparação maior ou igual",
            "    cp r16, r18              ; Compara low bytes",
            "    cpc r17, r19             ; Compara high bytes com carry",
            "    brge _maior_igual_true   ; Branch if greater or equal",
            "    ldi r16, 0               ; False",
            "    ldi r17, 0",
            "    rjmp _maior_igual_fim",
            "_maior_igual_true:",
            "    ldi r16, 1               ; True",
            "    ldi r17, 0",
            "_maior_igual_fim:",
            "    rcall stack_push_int",
            ""
        ],
        '!=': [
            "    ; Operação diferente de",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Comparação de diferença",
            "    cp r16, r18              ; Compara low bytes",
            "    brne _diferente_true     ; Se diferentes, é verdadeiro",
            "    cp r17, r19              ; Compara high bytes",
            "    brne _diferente_true     ; Se diferentes, é verdadeiro",
            "    ldi r16, 0               ; False",
            "    ldi r17, 0",
            "    rjmp _diferente_fim",
            "_diferente_true:",
            "    ldi r16, 1               ; True",
            "    ldi r17, 0",
            "_diferente_fim:",
            "    rcall stack_push_int",
            ""
        ],
        
        # Operadores lógicos
        '!': [
            "    ; Operação NOT",
            "    rcall stack_pop_int      ; Remove operando",
            "",
            "    ; NOT lógico",
            "    cp r16, __zero_reg__     ; Compara com zero",
            "    cpc r17, __zero_reg__",
            "    breq _not_true           ; Se zero, resultado é 1",
            "    ldi r16, 0               ; Não é zero, resultado é 0",
            "    ldi r17, 0",
            "    rjmp _not_fim",
            "_not_true:",
            "    ldi r16, 1               ; É zero, resultado é 1",
            "    ldi r17, 0",
            "_not_fim:",
            "    rcall stack_push_int",
            ""
        ],
        '||': [
            "    ; Operação OR",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; OR lógico",
            "    cp r16, __zero_reg__     ; Verifica primeiro operando",
            "    cpc r17, __zero_reg__",
            "    brne _or_true            ; Se não é zero, resultado é 1",
            "    cp r18, __zero_reg__     ; Verifica segundo operando",
            "    cpc r19, __zero_reg__",
            "    brne _or_true            ; Se não é zero, resultado é 1",
            "    ldi r16, 0               ; Ambos são zero, resultado é 0",
            "    ldi r17, 0",
            "    rjmp _or_fim",
            "_or_true:",
            "    ldi r16, 1               ; Pelo menos um não é zero",
            "    ldi r17, 0",
            "_or_fim:",
            "    rcall stack_push_int",
            ""
        ],
        '&&': [
            "    ; Operação AND",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; AND lógico",
            "    cp r16, __zero_reg__     ; Verifica primeiro operando",
            "    cpc r17, __zero_reg__",
            "    breq _and_false          ; Se é zero, resultado é 0",
            "    cp r18, __zero_reg__     ; Verifica segundo operando",
            "    cpc r19, __zero_reg__",
            "    breq _and_false          ; Se é zero, resultado é 0",
            "    ldi r16, 1               ; Ambos não são zero",
            "    ldi r17, 0",
            "    rjmp _and_fim",
            "_and_false:",
            "    ldi r16, 0               ; Pelo menos um é zero",
            "    ldi r17, 0",
            "_and_fim:",
            "    rcall stack_push_int",
            ""
        ],
    }

def gerar_operacao(operador: str) -> List[str]:
    """Retorna as linhas Assembly para o operador informado."""
    mapa = _operacao_map()
    return mapa.get(operador, [f"    ; Operação {operador} não implementada", ""])

__all__ = [
    "is_number", "is_integer", "is_variable_mem",
    "is_comparison_operator", "is_logical_operator",
    "is_control_structure", "is_special_identifier",
    "gerar_push_int", "gerar_operacao",
]
