#!/usr/bin/env python3
"""
Script de Geração TAC

Gera código de três endereços (TAC) a partir da AST atribuída da Fase 3.

Uso:
    # Primeiro, gere a AST com o compilador
    python compilador.py inputs/RA3/teste2.txt

    # Depois gere o TAC
    python generate_tac.py

Arquivos de Saída:
    - outputs/RA4/TAC.json (formato JSON estruturado)
    - outputs/RA4/TAC.txt (formato texto simples)
"""

import json
import sys
from pathlib import Path

# Adiciona src ao path
RAIZ_PROJETO = Path(__file__).parent
sys.path.insert(0, str(RAIZ_PROJETO / "src"))

from src.RA4.functions.python.gerenciador_tac import GerenciadorTAC
from src.RA4.functions.python.percorredor_ast import PercorredorAST
from src.RA4.functions.python.saida_tac import salvar_saida_tac

# Caminhos dos arquivos
ENTRADA_AST = RAIZ_PROJETO / "outputs" / "RA3" / "arvore_atribuida.json"
DIRETORIO_SAIDA = RAIZ_PROJETO / "outputs" / "RA4"


def carregar_ast():
    """Carrega a AST atribuída da saída da Fase 3."""
    if not ENTRADA_AST.exists():
        print(f"Erro: Arquivo AST não encontrado em {ENTRADA_AST}")
        print("\nExecute o compilador primeiro para gerar a AST:")
        print("  python compilador.py inputs/RA3/teste2.txt")
        sys.exit(1)

    try:
        with open(ENTRADA_AST, 'r', encoding='utf-8') as f:
            ast = json.load(f)
        return ast
    except json.JSONDecodeError as e:
        print(f"Erro: JSON inválido no arquivo AST: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao carregar AST: {e}")
        sys.exit(1)


def gerar_tac(ast):
    """Gera instruções TAC a partir da AST."""
    try:
        gerenciador = GerenciadorTAC()
        percorredor = PercorredorAST(gerenciador)
        instrucoes = percorredor.gerar_tac(ast)
        estatisticas = percorredor.obter_estatisticas()
        return instrucoes, estatisticas
    except IndexError as e:
        print(f"\nAviso: Geração TAC parou devido a recurso não implementado")
        print(f"   Erro: {e}")
        print(f"\n   Provavelmente operadores lógicos (!, &&, ||) que ainda")
        print(f"   não estão implementados. Operadores aritméticos e de")
        print(f"   comparação devem funcionar corretamente.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao gerar TAC: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def imprimir_resumo(instrucoes, estatisticas):
    """Imprime resumo no console."""
    print("\n" + "=" * 60)
    print("GERAÇÃO TAC COMPLETA")
    print("=" * 60)
    print(f"\nAST fonte: {ENTRADA_AST}")
    print(f"Instruções geradas: {len(instrucoes)}")

    print("\nEstatísticas:")
    for chave, valor in estatisticas.items():
        print(f"  {chave}: {valor}")

    print(f"\nArquivos de saída:")
    print(f"  JSON: {DIRETORIO_SAIDA / 'TAC.json'}")
    print(f"  Texto: {DIRETORIO_SAIDA / 'TAC.txt'}")

    print("\nPrimeiras 10 instruções:")
    for i, instr in enumerate(instrucoes[:10], 1):
        tipo = f"[{instr.tipo_dado}]" if hasattr(instr, 'tipo_dado') and instr.tipo_dado else ""
        print(f"  {i:2}. Linha {instr.linha:2}: {instr.para_string():<25} {tipo}")

    if len(instrucoes) > 10:
        print(f"  ... e mais {len(instrucoes) - 10} instruções")

    print("\n" + "=" * 60)


def main():
    """Ponto de entrada principal."""
    print("\nGerador TAC")
    print("=" * 60)

    # Carrega AST
    print(f"\nCarregando AST de: {ENTRADA_AST}")
    ast = carregar_ast()
    num_linhas = len(ast.get('arvore_atribuida', []))
    print(f"AST carregada com {num_linhas} linhas")

    # Gera TAC
    print("\nGerando instruções TAC...")
    instrucoes, estatisticas = gerar_tac(ast)
    print(f"Geradas {len(instrucoes)} instruções")

    # Salva saídas
    print("\nSalvando arquivos...")
    arquivos = salvar_saida_tac(instrucoes, DIRETORIO_SAIDA)
    print(f"  JSON: {arquivos['json']}")
    print(f"  Texto: {arquivos['texto']}")

    # Imprime resumo
    imprimir_resumo(instrucoes, estatisticas)


if __name__ == "__main__":
    main()
