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

from .tac_instructions import TACInstruction, instruction_from_dict, TACBinaryOp, TACAssignment, TACUnaryOp, TACIfGoto, TACIfFalseGoto, TACGoto
from .erros_compilador import TACError, FileError, JSONError, ValidationError


#########################
# FUNÇÕES AUXILIARES
#########################

def _carregar_json_validado(caminho_arquivo: str, chaves_obrigatorias: List[str] = None) -> Dict[str, Any]:
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


#########################
# CLASSE PRINCIPAL: TACOptimizer
#########################

class TACOptimizer:
    """Otimizador TAC - Carrega, valida e representa TAC para otimizações."""

    def __init__(self):
        self.instructions: List[TACInstruction] = []

    #########################
    # MÉTODO PRINCIPAL DE OTIMIZAÇÃO
    #########################

    def otimizarTAC(self) -> Dict[str, int]:
        """
        Aplica todas as otimizações TAC na ordem correta.

        Ordem de aplicação:
        1. Constant Folding - avalia operações constantes em tempo de compilação
        2. Constant Propagation - propaga constantes conhecidas, substituindo variáveis
        3. Dead Code Elimination - remove código morto e inalcançável

        Returns:
            Dicionário com estatísticas das otimizações aplicadas
        """
        if not self.instructions:
            return {'constant_folding': 0, 'constant_propagation': 0, 'dead_code_elimination': 0, 'total': 0}

        # 1. Constant Folding primeiro (avalia operações constantes)
        foldings = self.otimizar_constant_folding()

        # 2. Constant Propagation depois (substitui variáveis por constantes)
        propagations = self.otimizar_constant_propagation()

        # 3. Dead Code Elimination (remove código morto e inalcançável)
        dead_code = self.otimizar_dead_code_elimination()

        total_otimizacoes = propagations + foldings + dead_code

        return {
            'constant_folding': foldings,
            'constant_propagation': propagations,
            'dead_code_elimination': dead_code,
            'total': total_otimizacoes
        }

    #########################
    # CARREGAMENTO E PARSING DE TAC
    #########################

    def carregar_tac(self, arquivo_json: str) -> None:
        """Carrega TAC.json e converte para objetos TACInstruction."""
        data = _carregar_json_validado(arquivo_json, ['instructions'])

        instructions = []
        for i, item in enumerate(data['instructions']):
            try:
                instruction = instruction_from_dict(item)
                instructions.append(instruction)
            except Exception as e:
                raise TACError(f"erro na instrução {i}: {e}", i, {"data": item})

        self.instructions = instructions

    #########################
    # OTIMIZAÇÕES: CONSTANT PROPAGATION
    #########################

    def otimizar_constant_propagation(self) -> int:
        """
        Aplica constant propagation: substitui referências a variáveis constantes por seus valores.

        Exemplo:
        Antes: t1 = 5
               t2 = t1 + 3
               t3 = t1 * 2
        Depois: t1 = 5
                t2 = 5 + 3
                t3 = 5 * 2

        Returns:
            Número de propagações aplicadas
        """
        if not self.instructions:
            return 0

        propagacoes = 0
        mapa_constantes = {}  # variável -> valor_constante

        for i, instr in enumerate(self.instructions):
            # Processa a instrução: propaga constantes e atualiza mapa
            instr_modificada, modificada = self._processar_instrucao_com_constantes(instr, mapa_constantes)

            if modificada:
                self.instructions[i] = instr_modificada
                propagacoes += 1

        return propagacoes

    #########################
    # HELPERS PARA CONSTANT PROPAGATION
    #########################

    def _processar_instrucao_com_constantes(self, instr, mapa_constantes):
        """Processa instrução TAC: propaga constantes e atualiza mapa."""
        # Determina variável de destino
        dest_var = getattr(instr, 'result', getattr(instr, 'dest', None))

        # Atualiza mapa de constantes
        if dest_var:
            if isinstance(instr, TACAssignment) and TACInstruction.is_constant(instr.source):
                mapa_constantes[dest_var] = instr.source
            elif dest_var in mapa_constantes:
                del mapa_constantes[dest_var]

        # Propaga constantes na instrução
        if isinstance(instr, TACBinaryOp):
            novo_op1 = mapa_constantes.get(instr.operand1, instr.operand1)
            novo_op2 = mapa_constantes.get(instr.operand2, instr.operand2)

            if novo_op1 != instr.operand1 or novo_op2 != instr.operand2:
                return TACBinaryOp(
                    result=instr.result,
                    operand1=novo_op1,
                    operator=instr.operator,
                    operand2=novo_op2,
                    line=instr.line,
                    data_type=instr.data_type
                ), True

        elif isinstance(instr, TACUnaryOp):
            novo_op = mapa_constantes.get(instr.operand, instr.operand)

            if novo_op != instr.operand:
                return TACUnaryOp(
                    result=instr.result,
                    operator=instr.operator,
                    operand=novo_op,
                    line=instr.line,
                    data_type=instr.data_type
                ), True

        elif isinstance(instr, (TACIfGoto, TACIfFalseGoto)):
            nova_cond = mapa_constantes.get(instr.condition, instr.condition)

            if nova_cond != instr.condition:
                if isinstance(instr, TACIfGoto):
                    return TACIfGoto(condition=nova_cond, target=instr.target, line=instr.line), True
                else:
                    return TACIfFalseGoto(condition=nova_cond, target=instr.target, line=instr.line), True

        return instr, False

    #########################
    # OTIMIZAÇÕES: DEAD CODE ELIMINATION
    #########################

    def otimizar_dead_code_elimination(self) -> int:
        """
        Aplica dead code elimination: remove código morto e inalcançável.

        Remove:
        - Atribuições a variáveis nunca utilizadas
        - Código após saltos incondicionais (goto)

        Returns:
            Número de instruções removidas
        """
        if not self.instructions:
            return 0

        # Fase 1: Análise de liveness (variáveis utilizadas)
        used_vars = self._analisar_liveness()

        # Fase 2: Remover código morto e inalcançável
        novas_instrucoes = []
        removidas = 0
        skip_until_label = None

        for idx, instr in enumerate(self.instructions):
            # Se estamos pulando código inalcançável
            if skip_until_label:
                # Verificar se encontrou o label alvo
                if isinstance(instr, TACAssignment) and instr.source == '' and instr.dest == skip_until_label:
                    skip_until_label = None  # Encontrou o label, para de pular
                else:
                    removidas += 1
                    continue

            # Verificar se é um goto incondicional
            if isinstance(instr, TACGoto):
                # Verificar se o label alvo existe depois nesta sequência linear
                target = instr.target
                label_found_later = False
                for future_instr in self.instructions[idx+1:]:
                    if isinstance(future_instr, TACAssignment) and future_instr.source == '' and future_instr.dest == target:
                        label_found_later = True
                        break
                if label_found_later:
                    skip_until_label = instr.target
                novas_instrucoes.append(instr)
                continue

            # Verificar se é uma atribuição a variável não utilizada
            dest_var = getattr(instr, 'result', getattr(instr, 'dest', None))
            if (dest_var and dest_var not in used_vars and dest_var.startswith('t') and
                isinstance(instr, (TACAssignment, TACBinaryOp, TACUnaryOp)) and
                getattr(instr, 'source', '') != ''):  # Não remover labels (source vazia) ou outputs
                removidas += 1
                continue

            # Manter instrução
            novas_instrucoes.append(instr)

        self.instructions = novas_instrucoes
        return removidas

    #########################
    # HELPERS PARA DEAD CODE ELIMINATION
    #########################

    def _analisar_liveness(self) -> set:
        """Analisa quais variáveis são utilizadas no código."""
        used_vars = set()
        
        # Coletar todas as variáveis utilizadas como operandos
        for instr in self.instructions:
            # Adicionar operandos utilizados
            if hasattr(instr, 'operand1') and instr.operand1 and not TACInstruction.is_constant(instr.operand1):
                used_vars.add(instr.operand1)
            if hasattr(instr, 'operand2') and instr.operand2 and not TACInstruction.is_constant(instr.operand2):
                used_vars.add(instr.operand2)
            if hasattr(instr, 'operand') and instr.operand and not TACInstruction.is_constant(instr.operand):
                used_vars.add(instr.operand)
            if hasattr(instr, 'condition') and instr.condition and not TACInstruction.is_constant(instr.condition):
                used_vars.add(instr.condition)
            # Para assignments, adicionar source se não constante
            if isinstance(instr, TACAssignment) and instr.source and not TACInstruction.is_constant(instr.source):
                used_vars.add(instr.source)
                
        return used_vars

    #########################
    # OTIMIZAÇÕES: CONSTANT FOLDING
    #########################

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


    #########################
    # HELPERS PARA CONSTANT FOLDING
    #########################

    def _avaliar_operacao_constante(self, instr: TACBinaryOp) -> float:
        """Avalia operação binária entre constantes."""
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
                return op1 // op2
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