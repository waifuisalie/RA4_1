#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA4_1

from typing import Dict, Any


class CompilerError(Exception):
    """Erro base do compilador."""

    def __init__(self, message: str, line: int = -1, context: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.context = context or {}


class FileError(CompilerError):
    """Erro de arquivo."""
    pass


class JSONError(CompilerError):
    """Erro de JSON."""
    pass


class ValidationError(CompilerError):
    """Erro de validação."""
    pass


class TACError(CompilerError):
    """Erro específico de TAC."""
    pass