"""
Saída TAC - Serialização de instruções para arquivos de saída.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

from .instrucoes_tac import InstrucaoTAC


def para_json(instrucoes: List[InstrucaoTAC]) -> Dict[str, Any]:
    """Converte instruções TAC para dicionário JSON."""
    return {
        "instrucoes": [instr.para_dicionario() for instr in instrucoes]
    }


def para_texto(instrucoes: List[InstrucaoTAC]) -> str:
    """Converte instruções TAC para texto simples."""
    linhas = []
    for instr in instrucoes:
        linhas.append(instr.para_string())
    return "\n".join(linhas)


def salvar_json(instrucoes: List[InstrucaoTAC], caminho: Path) -> None:
    """Salva instruções em arquivo JSON."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    dados = para_json(instrucoes)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def salvar_texto(instrucoes: List[InstrucaoTAC], caminho: Path) -> None:
    """Salva instruções em arquivo texto."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    conteudo = para_texto(instrucoes)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)


def salvar_saida_tac(
    instrucoes: List[InstrucaoTAC],
    diretorio: Path,
    **kwargs  # ignora parâmetros extras para compatibilidade
) -> Dict[str, Path]:
    """Salva instruções TAC em arquivos JSON e texto."""
    caminho_json = diretorio / "TAC.json"
    caminho_txt = diretorio / "TAC.txt"

    salvar_json(instrucoes, caminho_json)
    salvar_texto(instrucoes, caminho_txt)

    return {"json": caminho_json, "texto": caminho_txt}
