#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA4_1

"""
Saída TAC - Funções de Serialização

Módulo para exportar instruções TAC em:
- JSON: Para acesso programático.
- Markdown: Para leitura humana e documentação.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from .tac_instructions import TACInstruction


#########################
# FUNÇÕES DE CONVERSÃO
#########################

def to_json(
    instructions: List[TACInstruction],
    statistics: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Converte instruções TAC para dicionário serializável em JSON."""
    result = {
        "metadata": metadata or {
            "generated_at": datetime.now().isoformat(),
            "generator": "RA4 TAC Generator",
            "version": "1.0"
        },
        "statistics": statistics or {},
        "instructions": [instr.to_dict() for instr in instructions]
    }

    return result


def to_markdown(
    instructions: List[TACInstruction],
    statistics: Optional[Dict[str, Any]] = None,
    title: str = "TAC Output"
) -> str:
    """Converte instruções TAC para string formatada em Markdown."""
    lines = []

    # Cabeçalho
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Seção de Instruções
    lines.append("## Instructions")
    lines.append("")
    lines.append("```")

    for instr in instructions:
        # Formato simples: Line X: instruction [type: type]
        line_num = getattr(instr, 'line', 0)
        instr_str = instr.to_string()
        type_info = getattr(instr, 'data_type', '')

        # Formata com alinhamento
        line_prefix = f"Line {line_num:2d}: "
        instr_padded = f"{instr_str:<25}"
        type_suffix = f"[type: {type_info}]" if type_info else ""

        lines.append(f"{line_prefix}{instr_padded}{type_suffix}")

    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Seção de Estatísticas
    lines.append("## Statistics")
    lines.append("")
    if statistics:
        for key, value in statistics.items():
            lines.append(f"- **{key}:** {value}")

    return "\n".join(lines)


#########################
# FUNÇÕES DE SALVAMENTO
#########################

def save_json(
    instructions: List[TACInstruction],
    output_path: Path,
    statistics: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """Salva instruções TAC em arquivo JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = to_json(instructions, statistics, metadata)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_markdown(
    instructions: List[TACInstruction],
    output_path: Path,
    statistics: Optional[Dict[str, Any]] = None,
    title: str = "TAC Output"
) -> None:
    """Salva instruções TAC em arquivo Markdown."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = to_markdown(instructions, statistics, title)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def save_tac_output(
    instructions: List[TACInstruction],
    output_dir: Path,
    statistics: Optional[Dict[str, Any]] = None,
    source_file: Optional[str] = None
) -> Dict[str, Path]:
    """
    Função de conveniência: Salva TAC em ambos formatos (JSON e Markdown).
    
    Returns:
        Dicionário com os caminhos dos arquivos gerados.
    """
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "generator": "RA4 TAC Generator",
        "version": "1.0"
    }
    if source_file:
        metadata["source_file"] = source_file

    json_path = output_dir / "tac_instructions.json"
    md_path = output_dir / "tac_output.md"

    title = "TAC Output"
    if source_file:
        title = f"TAC Output - {source_file}"

    save_json(instructions, json_path, statistics, metadata)
    save_markdown(instructions, md_path, statistics, title)

    return {
        "json": json_path,
        "markdown": md_path
    }