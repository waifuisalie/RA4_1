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
from typing import List, Dict, Any, Optional

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
        4. Jump Elimination - remove saltos redundantes e rótulos não utilizados

        Returns:
            Dicionário com estatísticas das otimizações aplicadas
        """
        if not self.instructions:
            return {'constant_folding': 0, 'constant_propagation': 0, 'dead_code_elimination': 0, 'jump_elimination': 0, 'total': 0}

        # 1. Constant Folding primeiro (avalia operações constantes)
        foldings = self.otimizar_constant_folding()

        # 2. Constant Propagation depois (substitui variáveis por constantes)
        propagations = self.otimizar_constant_propagation()

        # 3. Dead Code Elimination (remove código morto e inalcançável)
        dead_code = self.otimizar_dead_code_elimination()

        # 4. Jump Elimination (remove saltos redundantes)
        jump_elim = self.otimizar_jump_elimination()

        total_otimizacoes = propagations + foldings + dead_code + jump_elim

        return {
            'constant_folding': foldings,
            'constant_propagation': propagations,
            'dead_code_elimination': dead_code,
            'jump_elimination': jump_elim,
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

        # Fase 1: Análise completa de liveness
        liveness_info = self._analisar_liveness_completa()

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

            # Verificar se é uma atribuição a variável temporária não utilizada
            dest_var = getattr(instr, 'result', getattr(instr, 'dest', None))
            if (dest_var and dest_var.startswith('t') and 
                dest_var not in liveness_info[idx]['live_out'] and
                isinstance(instr, (TACAssignment, TACBinaryOp, TACUnaryOp)) and
                getattr(instr, 'source', '') != ''):  # Não remover labels (source vazia)
                removidas += 1
                continue

            # Manter instrução
            novas_instrucoes.append(instr)

        self.instructions = novas_instrucoes
        return removidas

    #########################
    # HELPERS PARA DEAD CODE ELIMINATION
    #########################

    def _analisar_liveness_completa(self) -> Dict[int, Dict[str, set]]:
        """
        Análise completa de liveness usando algoritmo backward.
        
        Returns:
            Dict[instr_index, {'live_in': set, 'live_out': set}]
        """
        if not self.instructions:
            return {}
        
        n = len(self.instructions)
        
        # Inicializar live_out (conjunto vazio para todas)
        live_out = [set() for _ in range(n)]
        
        # Mapear labels para índices
        label_to_index = {}
        for i, instr in enumerate(self.instructions):
            if isinstance(instr, TACAssignment) and instr.source == '' and instr.dest:
                label_to_index[instr.dest] = i
        
        # Algoritmo iterativo até ponto fixo
        changed = True
        while changed:
            changed = False
            
            # Processar do fim para o início (backward)
            for i in range(n - 1, -1, -1):
                instr = self.instructions[i]
                old_live_out = live_out[i].copy()
                
                # Calcular live_out baseado nos sucessores
                new_live_out = set()
                successors = self._get_successors(i, label_to_index)
                
                for succ in successors:
                    if succ < n:
                        new_live_out.update(live_out[succ])
                
                live_out[i] = new_live_out
                
                if live_out[i] != old_live_out:
                    changed = True
        
        # Agora calcular live_in para cada instrução
        result = {}
        for i in range(n):
            instr = self.instructions[i]
            
            # Calcular use[i] - variáveis usadas nesta instrução
            use_vars = self._get_used_variables(instr)
            
            # Calcular def[i] - variável definida nesta instrução
            def_var = self._get_defined_variable(instr)
            
            # live_in[i] = use[i] ∪ (live_out[i] - def[i])
            live_in = use_vars.union(live_out[i])
            if def_var:
                live_in.discard(def_var)
            
            result[i] = {
                'live_in': live_in,
                'live_out': live_out[i]
            }
        
        return result

    #########################
    # HELPERS PARA LIVENESS ANALYSIS
    #########################

    def _get_successors(self, index: int, label_to_index: Dict[str, int]) -> List[int]:
        """
        Retorna lista de índices dos sucessores da instrução no índice dado.
        """
        instr = self.instructions[index]
        successors = []
        
        # Instruções de controle de fluxo
        if isinstance(instr, TACGoto):
            # Goto incondicional: só vai para o target
            if instr.target in label_to_index:
                successors.append(label_to_index[instr.target])
        elif isinstance(instr, (TACIfGoto, TACIfFalseGoto)):
            # If-goto: vai para target E para fall-through
            if instr.target in label_to_index:
                successors.append(label_to_index[instr.target])
            if index < len(self.instructions) - 1:
                successors.append(index + 1)
        else:
            # Instrução normal: sucessor é a próxima instrução
            if index < len(self.instructions) - 1:
                successors.append(index + 1)
        
        return successors
    
    def _get_used_variables(self, instr) -> set:
        """Retorna conjunto de variáveis usadas pela instrução."""
        used = set()
        for attr in ['operand1', 'operand2', 'operand', 'condition', 'source']:
            if hasattr(instr, attr):
                var = getattr(instr, attr)
                if var and not TACInstruction.is_constant(var):
                    used.add(var)
        return used
    
    def _get_defined_variable(self, instr) -> Optional[str]:
        """Retorna variável definida pela instrução, se houver."""
        for attr in ['result', 'dest']:
            if hasattr(instr, attr):
                var = getattr(instr, attr)
                if var:
                    return var
        return None

    #########################
    # OTIMIZAÇÕES: JUMP ELIMINATION
    #########################

    def otimizar_jump_elimination(self) -> int:
        """
        Aplica jump elimination: remove saltos redundantes e rótulos não utilizados.

        Remove:
        - Saltos para a próxima instrução (goto L1; L1:)
        - Saltos para rótulos inexistentes
        - Rótulos não utilizados

        Returns:
            Número de instruções removidas
        """
        if not self.instructions:
            return 0

        # Identificar labels para análise
        referenced_labels = self._identificar_labels_referenciados()
        existing_labels = self._identificar_labels_existentes()

        # Filtrar instruções, removendo saltos redundantes e labels não utilizados
        novas_instrucoes = []
        i = 0
        removidas = 0

        while i < len(self.instructions):
            instr = self.instructions[i]

            if isinstance(instr, TACGoto):
                # Salto para próxima instrução (remover goto + label)
                if self._eh_salto_para_proxima_instrucao(i, instr.target):
                    removidas += 2
                    i += 2  # Pular goto e label
                    continue
                # Salto para label inexistente
                elif instr.target not in existing_labels:
                    removidas += 1
                    i += 1
                    continue

            elif isinstance(instr, TACAssignment) and instr.source == '' and instr.dest not in referenced_labels:
                # Label não utilizado
                removidas += 1
                i += 1
                continue

            # Manter instrução
            novas_instrucoes.append(instr)
            i += 1

        self.instructions = novas_instrucoes
        return removidas

    #########################
    # HELPERS PARA JUMP ELIMINATION
    #########################

    def _identificar_labels_referenciados(self) -> set:
        """Identifica todos os labels que são referenciados por gotos."""
        referenced = set()
        for instr in self.instructions:
            if isinstance(instr, TACGoto):
                referenced.add(instr.target)
            elif hasattr(instr, 'target') and instr.target:
                referenced.add(instr.target)
        return referenced

    def _identificar_labels_existentes(self) -> set:
        """Identifica todos os labels que existem fisicamente no código."""
        existentes = set()
        for instr in self.instructions:
            if isinstance(instr, TACAssignment) and instr.source == '':
                existentes.add(instr.dest)
        return existentes

    def _eh_salto_para_proxima_instrucao(self, current_index: int, target_label: str) -> bool:
        """Verifica se um goto salta para a próxima instrução (label)."""
        # Procurar o label alvo nas próximas instruções
        for j in range(current_index + 1, len(self.instructions)):
            next_instr = self.instructions[j]
            if isinstance(next_instr, TACAssignment) and next_instr.source == '' and next_instr.dest == target_label:
                # Encontrou o label na próxima instrução
                return True
            elif not (isinstance(next_instr, TACAssignment) and next_instr.source == ''):
                # Encontrou uma instrução não-label, parar busca
                break
        return False

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