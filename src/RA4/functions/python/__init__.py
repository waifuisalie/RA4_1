"""
RA4 - Phase 4: Code Generation Module

This package contains all functions for Phase 4 of the compiler:
- TAC (Three Address Code) generation
- TAC optimization
- AVR Assembly code generation

Author: Phase 4 - Code Generation Team
Project: RA4_Compiladores
"""

from .tac_instructions import (
    # Base class
    TACInstruction,

    # Assignment instructions
    TACAssignment,
    TACCopy,

    # Operation instructions
    TACBinaryOp,
    TACUnaryOp,

    # Control flow instructions
    TACLabel,
    TACGoto,
    TACIfGoto,
    TACIfFalseGoto,

    # Memory access instructions
    TACMemoryRead,
    TACMemoryWrite,

    # Function/procedure instructions
    TACCall,
    TACReturn,

    # Utility functions
    instruction_from_dict,
)

from .tac_manager import (
    # TAC generation utilities
    TACManager,
)

from .ast_traverser import (
    # AST traversal and TAC generation
    ASTTraverser,
)

from .tac_output import (
    # Output serialization functions
    to_json,
    to_markdown,
    save_json,
    save_markdown,
    save_tac_output,
)

from .gerador_tac import (
    # Main TAC generation functions
    gerarTAC,
    gerarTAC_from_dict,
    get_tac_as_text,
    get_tac_with_lines,
)

__all__ = [
    # Base class
    "TACInstruction",

    # Assignment instructions
    "TACAssignment",
    "TACCopy",

    # Operation instructions
    "TACBinaryOp",
    "TACUnaryOp",

    # Control flow instructions
    "TACLabel",
    "TACGoto",
    "TACIfGoto",
    "TACIfFalseGoto",

    # Memory access instructions
    "TACMemoryRead",
    "TACMemoryWrite",

    # Function/procedure instructions
    "TACCall",
    "TACReturn",

    # Utility functions
    "instruction_from_dict",

    # TAC generation utilities
    "TACManager",
    "ASTTraverser",

    # Output serialization functions
    "to_json",
    "to_markdown",
    "save_json",
    "save_markdown",
    "save_tac_output",

    # Main TAC generation functions
    "gerarTAC",
    "gerarTAC_from_dict",
    "get_tac_as_text",
    "get_tac_with_lines",
]
