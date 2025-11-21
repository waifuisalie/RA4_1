#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA4_1

import json
import os
from typing import List, Dict, Any

from .tac_instructions import TACInstruction, instruction_from_dict
from .erros_compilador import TACError, FileError, JSONError, ValidationError


def carregar_json_validado(caminho_arquivo: str, chaves_obrigatorias: List[str] = None) -> Dict[str, Any]:
    """
    Carrega arquivo JSON e valida estrutura básica.

    Args:
        caminho_arquivo: Caminho para arquivo JSON
        chaves_obrigatorias: Lista de chaves que devem existir no JSON

    Returns:
        Dados JSON carregados

    Raises:
        FileError: Se arquivo não existir
        JSONError: Se JSON for inválido
        ValidationError: Se estrutura for inválida
    """
    # Verifica se arquivo existe
    if not os.path.exists(caminho_arquivo):
        raise FileError(f"arquivo não encontrado: {caminho_arquivo}")

    # Carrega JSON
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise JSONError(f"JSON inválido: {e}")
    except Exception as e:
        raise FileError(f"erro ao ler arquivo: {e}")

    # Valida estrutura se chaves obrigatórias foram especificadas
    if chaves_obrigatorias:
        for chave in chaves_obrigatorias:
            if chave not in data:
                raise ValidationError(f"chave obrigatória ausente: {chave}", context={"missing_key": chave, "available_keys": list(data.keys())})

    return data


class TACOptimizer:
    """Otimizador TAC - Carrega, valida e representa TAC para otimizações."""

    def __init__(self):
        self.instructions: List[TACInstruction] = []

    def carregar_tac(self, arquivo_json: str) -> None:
        """Carrega TAC.json e converte para objetos TACInstruction."""
        data = carregar_json_validado(arquivo_json, ['instructions'])

        instructions = []
        for i, item in enumerate(data['instructions']):
            try:
                instruction = instruction_from_dict(item)
                instructions.append(instruction)
            except Exception as e:
                raise TACError(f"erro na instrução {i}: {e}", i, {"data": item})

        self.instructions = instructions

    def validar_formato(self) -> bool:
        """Valida formato básico das instruções TAC."""
        if not self.instructions:
            raise TACError("nenhuma instrução TAC carregada")

        return True