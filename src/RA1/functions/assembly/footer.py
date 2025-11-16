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

def gerar_footer(codigo: list[str]) -> None:
    footer = [
        "; ====================================================================",
        "; FINALIZAÇÃO - 16-BIT VERSION",
        "; ====================================================================",
        "",
        "end_program:",
        "    rjmp end_program         ; Loop infinito",
        "",
        "; ====================================================================",
        "; FIM DO CÓDIGO - 16-BIT RPN CALCULATOR",
        "; Suporte completo para inteiros de 0 a 65535",
        "; ====================================================================",
    ]
    codigo.extend(footer)
