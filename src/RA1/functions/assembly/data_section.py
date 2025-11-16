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

def gerar_secao_dados(codigo: list[str]) -> None:
    dados = [
        "; ====================================================================",
        "; SEÇÃO DE DADOS - 16-BIT VERSION",
        "; ====================================================================",
        "",
        ".section .data",
        "stack_ptr: .byte 1        ; Ponteiro da pilha RPN",
        "mem_vars:  .space 52      ; 26 variáveis 16-bit (A-Z)",
        "temp_result: .space 4     ; Resultado temporário",
        "",
        ".section .text",
        ""
    ]
    codigo.extend(dados)