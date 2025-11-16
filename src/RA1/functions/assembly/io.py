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

from pathlib import Path

def save_assembly(codigo_assembly: list[str], nome_arquivo: str | Path = "programa.s") -> bool:
    try:
        caminho_arquivo = Path(nome_arquivo)
        caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

        with caminho_arquivo.open('w', encoding='utf-8') as arquivo:
            for linha in codigo_assembly:
                arquivo.write(linha + '\n')

        print(f"Código Assembly salvo em: {caminho_arquivo} (16-bit version)")
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo Assembly: {e}")
        return False
