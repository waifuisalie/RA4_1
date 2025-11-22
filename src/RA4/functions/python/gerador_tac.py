#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA4_1

"""
Gerador TAC - Ponto de Entrada

Módulo principal para geração de código TAC a partir da AST (Fase 3).
Orquestra o pipeline de geração e salvamento.
"""

import json
from pathlib import Path
from typing import Dict, Any, Union, List, Optional

from .tac_manager import TACManager
from .ast_traverser import ASTTraverser
from .tac_instructions import TACInstruction
from .tac_output import save_tac_output


#########################
# FUNÇÃO PRINCIPAL
#########################

def gerarTAC(
    ast_input: Union[str, Path, Dict[str, Any]],
    output_dir: Union[str, Path] = "outputs/RA4",
    save_output: bool = True,
    source_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Gera código TAC a partir de uma AST atribuída.
    
    Args:
        ast_input: Caminho do arquivo JSON ou dicionário da AST.
        output_dir: Diretório para salvar saídas.
        save_output: Se deve salvar arquivos JSON/MD.
        source_file: Nome do arquivo fonte (para metadados).

    Returns:
        Dicionário contendo sucesso, instruções e estatísticas.
    """
    result = {
        "success": False,
        "instructions": [],
        "statistics": {},
        "output_files": None,
        "error": None
    }

    try:
        # Carrega AST se for um caminho de arquivo
        if isinstance(ast_input, (str, Path)):
            ast_path = Path(ast_input)
            if not ast_path.exists():
                raise FileNotFoundError(f"Arquivo AST não encontrado: {ast_path}")

            with open(ast_path, 'r', encoding='utf-8') as f:
                ast_dict = json.load(f)

            if source_file is None:
                source_file = ast_path.name
        else:
            ast_dict = ast_input

        # Validação básica da estrutura
        if not isinstance(ast_dict, dict):
            raise ValueError("AST deve ser um dicionário")

        if "arvore_atribuida" not in ast_dict:
            raise ValueError("AST deve conter a chave 'arvore_atribuida'")

        # Inicializa componentes do gerador
        manager = TACManager()
        traverser = ASTTraverser(manager)

        # Executa geração
        instructions = traverser.generate_tac(ast_dict)
        statistics = traverser.get_statistics()

        result["success"] = True
        result["instructions"] = instructions
        result["statistics"] = statistics

        # Salva arquivos se solicitado
        if save_output:
            output_path = Path(output_dir)
            output_files = save_tac_output(
                instructions,
                output_path,
                statistics,
                source_file
            )
            result["output_files"] = output_files

    except Exception as e:
        result["error"] = f"Erro inesperado: {type(e).__name__}: {e}"

    return result


def gerarTAC_from_dict(
    ast_dict: Dict[str, Any],
    output_dir: Union[str, Path] = "outputs/RA4",
    save_output: bool = True
) -> Dict[str, Any]:
    """Wrapper de conveniência para gerar TAC direto de um dicionário."""
    return gerarTAC(ast_dict, output_dir, save_output)


#########################
# UTILITÁRIOS DE TEXTO
#########################

def get_tac_as_text(instructions: List[TACInstruction]) -> str:
    """Converte instruções TAC para texto simples (uma por linha)."""
    return "\n".join(instr.to_string() for instr in instructions)


def get_tac_with_lines(instructions: List[TACInstruction]) -> str:
    """Converte instruções TAC para texto com anotações de linha original."""
    lines = []
    current_line = None

    for instr in instructions:
        line_num = getattr(instr, 'line', 0)
        if line_num != current_line:
            if current_line is not None:
                lines.append("")
            lines.append(f"# Linha {line_num}")
            current_line = line_num

        type_info = ""
        if hasattr(instr, 'data_type') and instr.data_type:
            type_info = f"  ; [{instr.data_type}]"

        lines.append(f"    {instr.to_string()}{type_info}")

    return "\n".join(lines)


# Execução standalone para testes
if __name__ == "__main__":
    import sys

    default_ast = Path("outputs/RA3/arvore_atribuida.json")
    default_output = Path("outputs/RA4")

    ast_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_ast
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else default_output

    print(f"Gerador TAC")
    print(f"Entrada: {ast_path}")
    print(f"Saída: {output_path}")
    print("-" * 50)

    result = gerarTAC(ast_path, output_path)

    if result["success"]:
        print(f"Sucesso! {result['statistics']['total_instructions']} instruções geradas.")
        print("-" * 50)
        print(get_tac_with_lines(result["instructions"]))
    else:
        print(f"Erro: {result['error']}")
        sys.exit(1)