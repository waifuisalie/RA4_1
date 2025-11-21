"""
TAC Generator - Main Entry Point for TAC Generation

Issue 1.8 - Main Generator Function

This module provides the main entry point for TAC generation from Phase 3's
attributed AST. It orchestrates the entire TAC generation pipeline.

Usage:
    from src.RA4.functions.python.gerador_tac import gerarTAC

    # Generate TAC from AST file
    result = gerarTAC("outputs/RA3/arvore_atribuida.json", "outputs/RA4")

    # Or from AST dictionary
    result = gerarTAC(ast_dict, "outputs/RA4")
"""

import json
from pathlib import Path
from typing import Dict, Any, Union, List, Optional

from .tac_manager import TACManager
from .ast_traverser import ASTTraverser
from .tac_instructions import TACInstruction
from .tac_output import save_tac_output


def gerarTAC(
    ast_input: Union[str, Path, Dict[str, Any]],
    output_dir: Union[str, Path] = "outputs/RA4",
    save_output: bool = True,
    source_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main function to generate TAC from attributed AST.

    This is the primary entry point for Phase 4's TAC generation.
    It takes the attributed AST from Phase 3 and generates Three Address Code.

    Args:
        ast_input: Either:
            - Path to arvore_atribuida.json file (str or Path)
            - Dictionary containing the AST directly
        output_dir: Directory to save output files (default: "outputs/RA4")
        save_output: Whether to save TAC.json and TAC.md files (default: True)
        source_file: Optional source file name for metadata

    Returns:
        Dictionary containing:
        {
            "success": bool,
            "instructions": List[TACInstruction],
            "statistics": Dict[str, Any],
            "output_files": Dict[str, Path] (if save_output=True),
            "error": str (if success=False)
        }

    Example:
        >>> result = gerarTAC("outputs/RA3/arvore_atribuida.json")
        >>> if result["success"]:
        ...     print(f"Generated {result['statistics']['total_instructions']} instructions")
        ...     for instr in result["instructions"]:
        ...         print(instr.to_string())

    Raises:
        FileNotFoundError: If AST file path doesn't exist
        json.JSONDecodeError: If AST file contains invalid JSON
        ValueError: If AST structure is invalid
    """
    result = {
        "success": False,
        "instructions": [],
        "statistics": {},
        "output_files": None,
        "error": None
    }

    try:
        # Load AST if path is provided
        if isinstance(ast_input, (str, Path)):
            ast_path = Path(ast_input)
            if not ast_path.exists():
                raise FileNotFoundError(f"AST file not found: {ast_path}")

            with open(ast_path, 'r', encoding='utf-8') as f:
                ast_dict = json.load(f)

            # Extract source file name from path if not provided
            if source_file is None:
                source_file = ast_path.name
        else:
            ast_dict = ast_input

        # Validate AST structure
        if not isinstance(ast_dict, dict):
            raise ValueError("AST must be a dictionary")

        if "arvore_atribuida" not in ast_dict:
            raise ValueError("AST must contain 'arvore_atribuida' key")

        # Create TAC generator components
        manager = TACManager()
        traverser = ASTTraverser(manager)

        # Generate TAC
        instructions = traverser.generate_tac(ast_dict)
        statistics = traverser.get_statistics()

        # Store results
        result["success"] = True
        result["instructions"] = instructions
        result["statistics"] = statistics

        # Save output files if requested
        if save_output:
            output_path = Path(output_dir)
            output_files = save_tac_output(
                instructions,
                output_path,
                statistics,
                source_file
            )
            result["output_files"] = output_files

    except FileNotFoundError as e:
        result["error"] = str(e)
    except json.JSONDecodeError as e:
        result["error"] = f"Invalid JSON in AST file: {e}"
    except ValueError as e:
        result["error"] = f"Invalid AST structure: {e}"
    except NotImplementedError as e:
        result["error"] = f"Unimplemented feature: {e}"
    except Exception as e:
        result["error"] = f"Unexpected error: {type(e).__name__}: {e}"

    return result


def gerarTAC_from_dict(
    ast_dict: Dict[str, Any],
    output_dir: Union[str, Path] = "outputs/RA4",
    save_output: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to generate TAC directly from AST dictionary.

    Args:
        ast_dict: Dictionary containing the attributed AST
        output_dir: Directory to save output files
        save_output: Whether to save output files

    Returns:
        Same as gerarTAC()
    """
    return gerarTAC(ast_dict, output_dir, save_output)


def get_tac_as_text(instructions: List[TACInstruction]) -> str:
    """
    Convert TAC instructions to simple text format.

    Args:
        instructions: List of TACInstruction objects

    Returns:
        String with one instruction per line

    Example:
        >>> text = get_tac_as_text(instructions)
        >>> print(text)
        t0 = 5
        t1 = 3
        t2 = t0 + t1
    """
    return "\n".join(instr.to_string() for instr in instructions)


def get_tac_with_lines(instructions: List[TACInstruction]) -> str:
    """
    Convert TAC instructions to text with line number annotations.

    Args:
        instructions: List of TACInstruction objects

    Returns:
        String with line annotations and instructions

    Example:
        >>> text = get_tac_with_lines(instructions)
        >>> print(text)
        # Line 1
        t0 = 5
        t1 = 3
        t2 = t0 + t1
        # Line 2
        ...
    """
    lines = []
    current_line = None

    for instr in instructions:
        line_num = getattr(instr, 'line', 0)
        if line_num != current_line:
            if current_line is not None:
                lines.append("")
            lines.append(f"# Line {line_num}")
            current_line = line_num

        type_info = ""
        if hasattr(instr, 'data_type') and instr.data_type:
            type_info = f"  ; [{instr.data_type}]"

        lines.append(f"    {instr.to_string()}{type_info}")

    return "\n".join(lines)


# Main execution for standalone testing
if __name__ == "__main__":
    import sys

    # Default paths
    default_ast = Path("outputs/RA3/arvore_atribuida.json")
    default_output = Path("outputs/RA4")

    # Parse command line arguments
    ast_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_ast
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else default_output

    print(f"TAC Generator")
    print(f"Input: {ast_path}")
    print(f"Output: {output_path}")
    print("-" * 50)

    # Generate TAC
    result = gerarTAC(ast_path, output_path)

    if result["success"]:
        print(f"Success! Generated {result['statistics']['total_instructions']} instructions")
        print()
        print("Statistics:")
        for key, value in result["statistics"].items():
            print(f"  {key}: {value}")
        print()
        print("Output files:")
        for fmt, path in result["output_files"].items():
            print(f"  {fmt}: {path}")
        print()
        print("TAC Output:")
        print("-" * 50)
        print(get_tac_with_lines(result["instructions"]))
    else:
        print(f"Error: {result['error']}")
        sys.exit(1)
