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
from .header import gerar_header
from .data_section import gerar_secao_dados
from .code_section import gerar_secao_codigo_multiplo
from .footer import gerar_footer
from .routines import gerar_rotinas_auxiliares

def gerarAssemblyMultiple(all_tokens: List[List[str]], codigoAssembly: List[str]) -> None:
    """Gera código assembly para múltiplas operações em um único arquivo."""
    codigoAssembly.clear()
    gerar_header(codigoAssembly)
    gerar_secao_dados(codigoAssembly)
    gerar_secao_codigo_multiplo(codigoAssembly, all_tokens)
    gerar_rotinas_auxiliares(codigoAssembly)
    gerar_footer(codigoAssembly)
