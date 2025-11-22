"""
RA4 - Fase 4: Módulo de Geração de Código

Pacote responsável pela Fase 4 do compilador:
- Geração de Código Intermediário (TAC)
- Otimização de TAC
- Geração de Código Assembly AVR
"""

from .tac_instructions import (
    # Classe base
    TACInstruction,

    # Instruções de Atribuição
    TACAssignment,
    TACCopy,

    # Instruções de Operação
    TACBinaryOp,
    TACUnaryOp,

    # Controle de Fluxo
    TACLabel,
    TACGoto,
    TACIfGoto,
    TACIfFalseGoto,

    # Acesso à Memória
    TACMemoryRead,
    TACMemoryWrite,

    # Funções
    TACCall,
    TACReturn,

    # Utilitários
    instruction_from_dict,
)

from .tac_manager import (
    TACManager,
)

from .ast_traverser import (
    ASTTraverser,
)

from .tac_output import (
    to_json,
    to_markdown,
    save_json,
    save_markdown,
    save_tac_output,
)

from .gerador_tac import (
    gerarTAC,
    gerarTAC_from_dict,
    get_tac_as_text,
    get_tac_with_lines,
)

__all__ = [
    # Classes base e instruções
    "TACInstruction",
    "TACAssignment",
    "TACCopy",
    "TACBinaryOp",
    "TACUnaryOp",
    "TACLabel",
    "TACGoto",
    "TACIfGoto",
    "TACIfFalseGoto",
    "TACMemoryRead",
    "TACMemoryWrite",
    "TACCall",
    "TACReturn",
    "instruction_from_dict",

    # Gerenciadores
    "TACManager",
    "ASTTraverser",

    # Serialização
    "to_json",
    "to_markdown",
    "save_json",
    "save_markdown",
    "save_tac_output",

    # Funções principais
    "gerarTAC",
    "gerarTAC_from_dict",
    "get_tac_as_text",
    "get_tac_with_lines",
]