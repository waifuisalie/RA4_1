#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

# ============================================================================
# LEGACY CODE - RA1 PHASE ONLY
# ============================================================================
# Este módulo foi usado na RA1 para geração de código Assembly RISC-V
# para Arduino Uno R3 (processador de 8 bits)
#
# STATUS: Não é mais necessário para RA2 (Parser) ou RA3+ (Analisador Semântico)
# MOTIVO: A especificação do RA3 afirma "Nesta fase, não será necessário gerar
#         código Assembly" - foco mudou para análise sintática e semântica
#
# Este arquivo é mantido para referência histórica e preservação da nota do RA1
# NÃO CORRIJA BUGS neste módulo a menos que esteja trabalhando no RA1
# ============================================================================

from .builder import gerarAssemblyMultiple
from .io import save_assembly
from .registers import save_registers_inc

__all__ = ["gerarAssemblyMultiple", "save_assembly", "save_registers_inc"]