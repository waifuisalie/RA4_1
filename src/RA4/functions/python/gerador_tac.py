"""
Gerador TAC - Ponto de entrada para geração de código de três endereços.
"""

import json
from pathlib import Path
from typing import Dict, Any, Union, List, Optional

from .gerenciador_tac import GerenciadorTAC
from .percorredor_ast import PercorredorAST
from .instrucoes_tac import InstrucaoTAC
from .saida_tac import salvar_saida_tac


def gerarTAC(
    entrada_ast: Union[str, Path, Dict[str, Any]],
    diretorio_saida: Union[str, Path] = "outputs/RA4",
    salvar_saida: bool = True,
    arquivo_fonte: Optional[str] = None
) -> Dict[str, Any]:
    """
    Gera TAC a partir da AST atribuída.

    Args:
        entrada_ast: Caminho para arvore_atribuida.json ou dicionário AST
        diretorio_saida: Diretório para saídas (padrão: outputs/RA4)
        salvar_saida: Se deve salvar TAC.json e TAC.txt
        arquivo_fonte: Nome do arquivo fonte (opcional)

    Returns:
        {sucesso, instrucoes, estatisticas, arquivos_saida, erro}
    """
    resultado = {
        "sucesso": False,
        "instrucoes": [],
        "estatisticas": {},
        "arquivos_saida": None,
        "erro": None
    }

    try:
        # Carrega AST
        if isinstance(entrada_ast, (str, Path)):
            caminho_ast = Path(entrada_ast)
            if not caminho_ast.exists():
                raise FileNotFoundError(f"Arquivo AST não encontrado: {caminho_ast}")

            with open(caminho_ast, 'r', encoding='utf-8') as f:
                dicionario_ast = json.load(f)

            if arquivo_fonte is None:
                arquivo_fonte = caminho_ast.name
        else:
            dicionario_ast = entrada_ast

        # Valida AST
        if not isinstance(dicionario_ast, dict):
            raise ValueError("AST deve ser um dicionário")

        if "arvore_atribuida" not in dicionario_ast:
            raise ValueError("AST deve conter 'arvore_atribuida'")

        # Gera TAC
        gerenciador = GerenciadorTAC()
        percorredor = PercorredorAST(gerenciador)
        instrucoes = percorredor.gerar_tac(dicionario_ast)
        estatisticas = percorredor.obter_estatisticas()

        resultado["sucesso"] = True
        resultado["instrucoes"] = instrucoes
        resultado["estatisticas"] = estatisticas

        # Salva saída
        if salvar_saida:
            caminho_saida = Path(diretorio_saida)
            arquivos_saida = salvar_saida_tac(instrucoes, caminho_saida)
            resultado["arquivos_saida"] = arquivos_saida

    except FileNotFoundError as e:
        resultado["erro"] = str(e)
    except json.JSONDecodeError as e:
        resultado["erro"] = f"JSON inválido: {e}"
    except ValueError as e:
        resultado["erro"] = f"AST inválida: {e}"
    except NotImplementedError as e:
        resultado["erro"] = f"Não implementado: {e}"
    except Exception as e:
        resultado["erro"] = f"Erro: {type(e).__name__}: {e}"

    return resultado


def gerarTAC_de_dicionario(
    dicionario_ast: Dict[str, Any],
    diretorio_saida: Union[str, Path] = "outputs/RA4",
    salvar_saida: bool = True
) -> Dict[str, Any]:
    """Gera TAC a partir de dicionário AST."""
    return gerarTAC(dicionario_ast, diretorio_saida, salvar_saida)


def obter_tac_como_texto(instrucoes: List[InstrucaoTAC]) -> str:
    """Converte instruções TAC para texto simples."""
    return "\n".join(instr.para_string() for instr in instrucoes)


def obter_tac_com_linhas(instrucoes: List[InstrucaoTAC]) -> str:
    """Converte instruções TAC para texto com números de linha."""
    linhas = []
    linha_atual = None

    for instr in instrucoes:
        num_linha = getattr(instr, 'linha', 0)
        if num_linha != linha_atual:
            if linha_atual is not None:
                linhas.append("")
            linhas.append(f"# Linha {num_linha}")
            linha_atual = num_linha

        info_tipo = ""
        if hasattr(instr, 'tipo_dado') and instr.tipo_dado:
            info_tipo = f"  ; [{instr.tipo_dado}]"

        linhas.append(f"    {instr.para_string()}{info_tipo}")

    return "\n".join(linhas)


if __name__ == "__main__":
    import sys

    ast_padrao = Path("outputs/RA3/arvore_atribuida.json")
    saida_padrao = Path("outputs/RA4")

    caminho_ast = Path(sys.argv[1]) if len(sys.argv) > 1 else ast_padrao
    caminho_saida = Path(sys.argv[2]) if len(sys.argv) > 2 else saida_padrao

    print(f"Gerador TAC")
    print(f"Entrada: {caminho_ast}")
    print(f"Saída: {caminho_saida}")
    print("-" * 50)

    resultado = gerarTAC(caminho_ast, caminho_saida)

    if resultado["sucesso"]:
        print(f"Gerou {resultado['estatisticas']['total_instrucoes']} instruções")
        print()
        print("Arquivos de saída:")
        for fmt, caminho in resultado["arquivos_saida"].items():
            print(f"  {fmt}: {caminho}")
        print()
        print("TAC:")
        print("-" * 50)
        print(obter_tac_com_linhas(resultado["instrucoes"]))
    else:
        print(f"Erro: {resultado['erro']}")
        sys.exit(1)
