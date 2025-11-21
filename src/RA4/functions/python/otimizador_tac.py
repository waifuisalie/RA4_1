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

from .tac_instructions import TACInstruction, instruction_from_dict, TACBinaryOp, TACAssignment
from .erros_compilador import TACError, FileError, JSONError, ValidationError


def carregar_json_validado(caminho_arquivo: str, chaves_obrigatorias: List[str] = None) -> Dict[str, Any]:
    """Carrega JSON e valida chaves obrigatórias."""
    if not os.path.exists(caminho_arquivo):
        raise FileError(f"arquivo não encontrado: {caminho_arquivo}")
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise JSONError(f"JSON inválido: {e}")
    except Exception as e:
        raise FileError(f"erro ao ler arquivo: {e}")

    if chaves_obrigatorias:
        for chave in chaves_obrigatorias:
            if chave not in data:
                raise ValidationError(f"chave obrigatória ausente: {chave}")

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

    def otimizar_constant_folding(self) -> int:
        """
        Aplica constant folding: avalia expressões constantes em tempo de compilação.
        
        Exemplo: t1 = 2 + 3 → t1 = 5
        
        Returns:
            Número de otimizações aplicadas
        """
        if not self.instructions:
            return 0
            
        otimizacoes = 0
        novas_instrucoes = []
        
        for instr in self.instructions:
            # Verifica se é operação binária constante
            if (isinstance(instr, TACBinaryOp) and 
                instr.operator in ['+', '-', '*', '/', '|', '%', '^'] and
                TACInstruction.is_constant(instr.operand1) and 
                TACInstruction.is_constant(instr.operand2)):
                
                # Avalia a operação constante
                resultado = self._avaliar_operacao_constante(instr)
                
                # Cria nova instrução de atribuição
                nova_instr = TACAssignment(
                    dest=instr.result,
                    source=str(resultado),
                    line=instr.line,
                    data_type=instr.data_type
                )
                
                novas_instrucoes.append(nova_instr)
                otimizacoes += 1
            else:
                # Mantém instrução original
                novas_instrucoes.append(instr)
        
        self.instructions = novas_instrucoes
        return otimizacoes


    def _avaliar_operacao_constante(self, instr: TACBinaryOp) -> float:
        """
        Avalia uma operação binária entre constantes.
        
        Args:
            instr: Instrução TACBinaryOp com operandos constantes
            
        Returns:
            Resultado da operação como float
        """
        try:
            op1 = float(instr.operand1)
            op2 = float(instr.operand2)
            
            if instr.operator == '+':
                return op1 + op2
            elif instr.operator == '-':
                return op1 - op2
            elif instr.operator == '*':
                return op1 * op2
            elif instr.operator == '/':
                if op2 == 0:
                    raise TACError(f"divisão por zero: {op1} / {op2}", instr.line)
                return op1 / op2
            elif instr.operator == '|':
                if op2 == 0:
                    raise TACError(f"divisão por zero: {op1} | {op2}", instr.line)
                return op1 / op2
            elif instr.operator == '%':
                if op2 == 0:
                    raise TACError(f"divisão por zero: {op1} % {op2}", instr.line)
                return op1 % op2
            elif instr.operator == '^':
                return op1 ** op2
            else:
                raise TACError(f"operador não suportado: {instr.operator}", instr.line)
                
        except ValueError as e:
            raise TACError(f"erro na conversão de operandos: {e}", instr.line)
        except Exception as e:
            raise TACError(f"erro inesperado na avaliação: {e}", instr.line)