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

    def otimizarTAC(self, file_name: str) -> Dict[str, int]:
        """
        Aplica todas as otimizações TAC em múltiplas passadas até ponto fixo.

        Ordem Ótima das Otimizações (baseada em dependências):
        1. Constant Folding: Avalia operações constantes primeiro
        2. Constant Propagation: Propaga constantes recém-criadas
        3. Dead Code Elimination: Remove código morto após propagação
        4. Jump Elimination: Remove saltos redundantes

        Algoritmo Multi-Pass:
        mudou = True
        iteracao = 0

        while mudou and iteracao < 100:
            iteracao++
            mudou = False

            # Pass 1: Constant Folding
            if otimizar_constant_folding():
                mudou = True

            # Pass 2: Constant Propagation
            if otimizar_constant_propagation():
                mudou = True

            # Pass 3: Dead Code Elimination
            if otimizar_dead_code_elimination():
                mudou = True

            # Pass 4: Jump Elimination
            if otimizar_jump_elimination():
                mudou = True

        Args:
            file_name: Nome do arquivo TAC original (para geração de relatórios)

        Returns:
            Dicionário com estatísticas das otimizações aplicadas
        """
        if not self.instructions:
            return {'constant_folding': 0, 'constant_propagation': 0, 'dead_code_elimination': 0, 'jump_elimination': 0, 'total': 0, 'iterations': 0}

        # Estatísticas iniciais
        initial_instructions = len(self.instructions)
        initial_temporaries = self._contar_temporarios()

        # Algoritmo multi-pass
        mudou = True
        iteracao = 0
        total_foldings = 0
        total_propagations = 0
        total_dead_code = 0
        total_jump_elim = 0

        while mudou and iteracao < 100:
            iteracao += 1
            mudou = False

            # Pass 1: Constant Folding
            foldings = self.otimizar_constant_folding()
            if foldings > 0:
                mudou = True
                total_foldings += foldings

            # Pass 2: Constant Propagation
            propagations = self.otimizar_constant_propagation()
            if propagations > 0:
                mudou = True
                total_propagations += propagations

            # Pass 3: Dead Code Elimination
            dead_code = self.otimizar_dead_code_elimination()
            if dead_code > 0:
                mudou = True
                total_dead_code += dead_code

            # Pass 4: Jump Elimination
            jump_elim = self.otimizar_jump_elimination()
            if jump_elim > 0:
                mudou = True
                total_jump_elim += jump_elim

        # Estatísticas finais
        final_instructions = len(self.instructions)
        final_temporaries = self._contar_temporarios()

        # Gerar relatórios
        self._gerar_tac_otimizado_md(file_name)
        self._gerar_tac_otimizado_json(file_name)
        self._gerar_relatorio_otimizacoes_md(file_name, {
            'initial_instructions': initial_instructions,
            'final_instructions': final_instructions,
            'initial_temporaries': initial_temporaries,
            'final_temporaries': final_temporaries,
            'foldings': total_foldings,
            'propagations': total_propagations,
            'dead_code': total_dead_code,
            'jump_elim': total_jump_elim,
            'iterations': iteracao
        })

        return {
            'constant_folding': total_foldings,
            'constant_propagation': total_propagations,
            'dead_code_elimination': total_dead_code,
            'jump_elimination': total_jump_elim,
            'total': total_foldings + total_propagations + total_dead_code + total_jump_elim,
            'iterations': iteracao
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

    #########################
    # HELPERS PARA CONTAGEM
    #########################

    def _contar_temporarios(self) -> int:
        """Conta o número de temporários únicos (variáveis começando com 't')."""
        temporarios = set()
        
        for instr in self.instructions:
            # Verificar resultado da instrução
            if hasattr(instr, 'result') and instr.result and instr.result.startswith('t'):
                temporarios.add(instr.result)
            
            # Verificar operandos
            for attr in ['operand1', 'operand2', 'operand', 'condition', 'source']:
                if hasattr(instr, attr):
                    var = getattr(instr, attr)
                    if isinstance(var, str) and var.startswith('t'):
                        temporarios.add(var)
        
        return len(temporarios)

    #########################
    # GERAÇÃO DE RELATÓRIOS
    #########################

    def _gerar_tac_otimizado_md(self, file_name: str) -> None:
        """Gera TAC_otimizado.md com representação legível do TAC otimizado."""
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'relatorios', 'RA4')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'TAC_otimizado_{base_name}.md')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f'# TAC Otimizado - {base_name}\n\n')

            # Representação das instruções otimizadas
            for i, instr in enumerate(self.instructions, 1):
                f.write(f'## Linha {i}: {instr.to_string()}\n\n')

            # Estatísticas
            f.write('## Estatísticas\n')
            f.write(f'- Total de instruções: {len(self.instructions)}\n')
            f.write(f'- Temporários criados: {self._contar_temporarios()}\n')

    def _gerar_tac_otimizado_json(self, file_name: str) -> None:
        """Gera TAC_otimizado.json com dados estruturados para o gerador Assembly."""
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'relatorios', 'RA4')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'TAC_otimizado_{base_name}.json')

        # Converter instruções para formato JSON
        instructions_json = [instr.to_dict() for instr in self.instructions]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({'instructions': instructions_json}, f, indent=2, ensure_ascii=False)

    def _gerar_relatorio_otimizacoes_md(self, file_name: str, stats: Dict[str, Any]) -> None:
        """Gera otimizacao_tac.md conforme especificação."""
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'relatorios', 'RA4')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'otimizacao_tac.md')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('# Relatório de Otimizações TAC\n\n')

            # 1. Resumo Executivo
            f.write('## 1. Resumo Executivo\n')
            reducao = ((stats['initial_instructions'] - stats['final_instructions']) / stats['initial_instructions'] * 100) if stats['initial_instructions'] > 0 else 0
            temporarios_eliminados = stats['initial_temporaries'] - stats['final_temporaries']
            f.write(f'- Instruções antes: {stats["initial_instructions"]}\n')
            f.write(f'- Instruções depois: {stats["final_instructions"]}\n')
            f.write(f'- Redução: {reducao:.1f}%\n')
            f.write(f'- Temporários eliminados: {temporarios_eliminados}\n\n')

            # 2. Técnicas Implementadas
            f.write('## 2. Técnicas Implementadas\n\n')

            # 2.1 Constant Folding
            f.write('### 2.1 Constant Folding\n')
            f.write('**Descrição:** Avalia operações constantes em tempo de compilação, substituindo expressões por seus valores calculados.\n\n')
            f.write('**Exemplo:**\n')
            f.write('Antes:\n')
            f.write('```\n')
            f.write('t0 = 2\n')
            f.write('t1 = 3\n')
            f.write('t2 = t0 + t1\n')
            f.write('```\n')
            f.write('Depois:\n')
            f.write('```\n')
            f.write('t2 = 5\n')
            f.write('```\n')
            f.write(f'\n**Impacto:** {stats["foldings"]} operações constantes avaliadas\n\n')

            # 2.2 Constant Propagation
            f.write('### 2.2 Constant Propagation\n')
            f.write('**Descrição:** Propaga constantes conhecidas, substituindo referências a variáveis constantes por seus valores.\n\n')
            f.write('**Exemplo:**\n')
            f.write('Antes:\n')
            f.write('```\n')
            f.write('t0 = 5\n')
            f.write('t1 = t0 + 3\n')
            f.write('t2 = t0 * 2\n')
            f.write('```\n')
            f.write('Depois:\n')
            f.write('```\n')
            f.write('t0 = 5\n')
            f.write('t1 = 8\n')
            f.write('t2 = 10\n')
            f.write('```\n')
            f.write(f'\n**Impacto:** {stats["propagations"]} propagações aplicadas\n\n')

            # 2.3 Dead Code Elimination
            f.write('### 2.3 Dead Code Elimination\n')
            f.write('**Descrição:** Remove instruções que não afetam o resultado final do programa.\n\n')
            f.write('**Exemplo:**\n')
            f.write('Antes:\n')
            f.write('```\n')
            f.write('t0 = x + y\n')
            f.write('t1 = t0 * 2\n')
            f.write('result = t0 + 1\n')
            f.write('```\n')
            f.write('Depois:\n')
            f.write('```\n')
            f.write('t0 = x + y\n')
            f.write('result = t0 + 1\n')
            f.write('```\n')
            f.write(f'\n**Impacto:** {stats["dead_code"]} instruções removidas\n\n')

            # 2.4 Eliminação de Saltos Redundantes
            f.write('### 2.4 Eliminação de Saltos Redundantes\n')
            f.write('**Descrição:** Remove saltos desnecessários e rótulos não utilizados.\n\n')
            f.write('**Exemplo:**\n')
            f.write('Antes:\n')
            f.write('```\n')
            f.write('goto L1\n')
            f.write('L1:\n')
            f.write('t0 = 5\n')
            f.write('```\n')
            f.write('Depois:\n')
            f.write('```\n')
            f.write('t0 = 5\n')
            f.write('```\n')
            f.write(f'\n**Impacto:** {stats["jump_elim"]} saltos eliminados\n\n')

            # 3. Estatísticas Detalhadas
            f.write('## 3. Estatísticas Detalhadas\n')
            f.write(f'- Número de instruções TAC antes: {stats["initial_instructions"]}\n')
            f.write(f'- Número de instruções TAC depois: {stats["final_instructions"]}\n')
            f.write(f'- Número de temporários eliminados: {temporarios_eliminados}\n')
            f.write(f'- Redução percentual: {reducao:.1f}%\n')
            f.write(f'- Número de iterações até convergência: {stats["iterations"]}\n')
            f.write('\n')

            # 4. Análise do Impacto no Código Assembly Gerado
            f.write('## 4. Análise do Impacto no Código Assembly Gerado\n')
            f.write('[Análise pendente - aguardando implementação da geração de Assembly]\n')