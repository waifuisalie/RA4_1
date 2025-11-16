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

def gerar_header(codigo: list[str]) -> None:
    header = [
        "; ====================================================================",
        "; Código Assembly gerado automaticamente para Arduino Uno (ATmega328p)",
        "; Processador RPN - 16-BIT VERSION",
        "; Suporte para inteiros de 0 a 65535",
        "; Compilado com PlatformIO/AVR-GCC",
        "; ====================================================================",
        "",
        '#include "registers.inc"',
        ".global main",
        "",
        ".section .text",
        ""
    ]
    codigo.extend(header)
