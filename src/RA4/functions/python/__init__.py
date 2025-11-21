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
]
