#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1

from typing import Dict, Any, Optional, List, Tuple
from src.RA3.functions.python.analisador_tipos import analisarSemantica as analisarSemanticaTipos, ErroSemantico
from src.RA3.functions.python.analisador_memoria_controle import analisarSemanticaMemoria, analisarSemanticaControle
from src.RA3.functions.python.tabela_simbolos import TabelaSimbolos


def _converter_arvore_json_para_analisador(arvore_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converte a árvore sintática JSON exportada pelo parser RA2
    para o formato esperado pelo analisador semântico.
    
    Formato JSON (RA2):
    {
      "linhas": [
        {
          "numero_linha": 1,
          "arvore": {...},
          "tokens": [...]
        }
      ]
    }
    
    Formato esperado pelo analisador:
    {
      "linhas": [
        {
          "numero_linha": 1,
          "filhos": [
            {
              "elementos": [...],
              "operador": "..."
            }
          ]
        }
      ]
    }
    """
    linhas_convertidas = []
    
    if not isinstance(arvore_json, dict):
        return {'linhas': []}
    
    for linha_json in arvore_json.get('linhas', []):
        if not isinstance(linha_json, dict):
            continue
            
        numero_linha = linha_json.get('numero_linha')
        arvore = linha_json.get('arvore')
        tokens = linha_json.get('tokens', [])
        
        if arvore is None:
            continue  # Pular linhas com erro sintático
            
        # Extrair elementos e operador da árvore sintática usando tokens
        elementos, operador = _extrair_elementos_e_operador(arvore, tokens)
        
        linha_convertida = {
            'numero_linha': numero_linha,
            'filhos': [{
                'elementos': elementos,
                'operador': operador
            }]
        }
        linhas_convertidas.append(linha_convertida)
    
    return {'linhas': linhas_convertidas}


def _extrair_elementos_e_operador_sub(arvore: Dict[str, Any], tokens: List[str] = None, start_idx: int = 0) -> Tuple[List[Dict[str, Any]], str]:
    """
    Versão para subexpressões que usa tokens com índice controlado.
    
    Args:
        arvore: Árvore sintática JSON da subexpressão
        tokens: Lista de tokens (opcional, para compatibilidade)
        start_idx: Índice inicial nos tokens
        
    Returns:
        Tupla (elementos, operador)
    """
    elementos = []
    operador = ""
    idx = start_idx
    
    def _processar_sequencia_sub(seq_node):
        nonlocal elementos, operador, idx
        
        if not isinstance(seq_node, dict):
            return
            
        filhos = seq_node.get('filhos', [])
        i = 0
        while i < len(filhos):
            filho = filhos[i]
            if isinstance(filho, dict):
                label = filho.get('label', '')
                
                if label == 'OPERANDO':
                    # Processar operando
                    elemento = None
                    has_res = False
                    
                    for sub_filho in filho.get('filhos', []):
                        if isinstance(sub_filho, dict):
                            sub_label = sub_filho.get('label', '')
                            
                            if sub_label == 'LINHA':
                                # Sub-subexpressão - avançar parênteses
                                if tokens and idx < len(tokens) and tokens[idx] == '(':
                                    idx += 1  # Pular '('
                                sub_sub_elementos, sub_sub_operador = _extrair_elementos_e_operador_sub({'label': 'PROGRAM', 'filhos': [sub_filho]}, tokens, idx)
                                elemento = {
                                    'subtipo': 'LINHA',
                                    'elementos': sub_sub_elementos,
                                    'operador': sub_sub_operador,
                                    'ast': {'elementos': sub_sub_elementos, 'operador': sub_sub_operador}
                                }
                                # Avançar até o ')' da subexpressão
                                while tokens and idx < len(tokens) and tokens[idx] != ')':
                                    idx += 1
                                if tokens and idx < len(tokens):
                                    idx += 1  # Pular ')'
                            elif sub_label in ['numero_inteiro', 'numero_real', 'identifier']:
                                # Folha terminal - pegar valor do token
                                if tokens and idx < len(tokens):
                                    # Para subexpressões simples, pular '(' se necessário
                                    if tokens[idx] == '(':
                                        idx += 1
                                    if tokens and idx < len(tokens):
                                        valor = tokens[idx]
                                        subtipo = 'numero_inteiro' if sub_label == 'numero_inteiro' else ('numero_real' if sub_label == 'numero_real' else 'variavel')
                                        elemento = {
                                            'subtipo': subtipo,
                                            'valor': valor
                                        }
                                        idx += 1
                                        # Pular ')' se existir
                                        if tokens and idx < len(tokens) and tokens[idx] == ')':
                                            idx += 1
                            elif sub_label == 'OPERANDO_OPCIONAL':
                                # Verificar RES
                                for neto in sub_filho.get('filhos', []):
                                    if isinstance(neto, dict) and neto.get('label') == 'res':
                                        has_res = True
                    
                    if elemento and has_res:
                        elemento['subtipo'] = elemento['subtipo'] + '_res'
                    
                    if elemento:
                        elementos.append(elemento)
                        
                elif label == 'SEQUENCIA_PRIME':
                    # Continuar processando
                    _processar_sequencia_sub(filho)
                    
                elif label == 'OPERADOR_FINAL':
                    # Extrair operador
                    operador = _extrair_operador_final(filho)
                    
            i += 1
    
    def _extrair_operador_final(op_final_node):
        """Extrai operador de OPERADOR_FINAL"""
        if not isinstance(op_final_node, dict):
            return ""
            
        for filho in op_final_node.get('filhos', []):
            if isinstance(filho, dict):
                label = filho.get('label', '')
                mapeamento_operadores = {
                    'ARITH_OP': {'+': '+', '-': '-', '*': '*', '/': '/', '%': '%', '^': '^', '|': '|'},
                    'COMP_OP': {'>': '>', '<': '<', '>=': '>=', '<=': '<=', '==': '==', '!=': '!='},
                    'LOGIC_OP': {'&&': '&&', '||': '||', '!': '!'},
                    'CONTROL_OP': {'ifelse': 'IFELSE', 'while': 'WHILE', 'for': 'FOR'}
                }
                
                for tipo_op, operadores in mapeamento_operadores.items():
                    if label == tipo_op:
                        for neto in filho.get('filhos', []):
                            if isinstance(neto, dict):
                                op_label = neto.get('label', '')
                                if op_label in operadores:
                                    return operadores[op_label]
                    elif label in operadores:
                        return operadores[label]
        
        return ""
    
    # Encontrar SEQUENCIA na árvore
    sequencia_node = None
    
    def _encontrar_sequencia(node):
        if isinstance(node, dict):
            if node.get('label') == 'SEQUENCIA':
                return node
            for filho in node.get('filhos', []):
                result = _encontrar_sequencia(filho)
                if result:
                    return result
        return None
    
    sequencia_node = _encontrar_sequencia(arvore)
    if sequencia_node:
        _processar_sequencia_sub(sequencia_node)
    
    return elementos, operador


def _extrair_elementos_e_operador(arvore: Dict[str, Any], tokens: List[str]) -> Tuple[List[Dict[str, Any]], str]:
    """
    Extrai elementos (operandos) e operador de uma linha da árvore sintática.
    
    Args:
        arvore: Árvore sintática JSON da linha (estrutura PROGRAM/LINHA)
        tokens: Lista de tokens da linha (usado apenas para compatibilidade)
        
    Returns:
        Tupla (elementos, operador) onde:
        - elementos: lista de dicionários com 'subtipo' e 'valor' ou subexpressões
        - operador: string representando o operador ou '' se não houver
    """
    # A árvore vem no formato PROGRAM -> LINHA -> SEQUENCIA
    # Precisamos extrair da parte LINHA
    linha_node = None
    
    # Encontrar o nó LINHA na árvore
    def _encontrar_linha(node):
        if isinstance(node, dict):
            if node.get('label') == 'LINHA':
                return node
            for filho in node.get('filhos', []):
                if isinstance(filho, dict):
                    result = _encontrar_linha(filho)
                    if result:
                        return result
        return None
    
    linha_node = _encontrar_linha(arvore)
    if not linha_node:
        return [], ""
    
    # Processar a SEQUENCIA dentro da LINHA
    sequencia_node = None
    for filho in linha_node.get('filhos', []):
        if isinstance(filho, dict) and filho.get('label') == 'SEQUENCIA':
            sequencia_node = filho
            break
    
    if not sequencia_node:
        return [], ""
    
    # Extrair elementos e operador da sequência
    elementos = []
    operador = ""
    indice_token = 1  # Pular o '(' inicial
    
    def _processar_operando(operando_node):
        """Processa um nó OPERANDO e retorna o elemento correspondente"""
        nonlocal indice_token
        if not isinstance(operando_node, dict):
            return None
            
        # Verificar se é uma subexpressão (LINHA)
        linha_interna = None
        for filho in operando_node.get('filhos', []):
            if isinstance(filho, dict) and filho.get('label') == 'LINHA':
                linha_interna = filho
                break
        
        if linha_interna:
            # É uma subexpressão - processar recursivamente
            # Para subexpressões, usar tokens com índice controlado
            sub_elementos, sub_operador = _extrair_elementos_e_operador_sub({'label': 'PROGRAM', 'filhos': [linha_interna]}, tokens, indice_token)
            sub_elemento = {
                'subtipo': 'LINHA',
                'elementos': sub_elementos,
                'operador': sub_operador,
                'ast': {'elementos': sub_elementos, 'operador': sub_operador}  # Definir chave 'ast'
            }
            # Avançar tokens consumidos pela subexpressão
            # Contar parênteses para saber quantos tokens pular
            parenteses = 0
            while indice_token < len(tokens):
                if tokens[indice_token] == '(':
                    parenteses += 1
                elif tokens[indice_token] == ')':
                    parenteses -= 1
                    if parenteses == 0:
                        indice_token += 1  # Consumir o ')'
                        break
                indice_token += 1
            return sub_elemento
        
        # Verificar se é um número ou identificador
        elemento = None
        has_res = False
        
        for filho in operando_node.get('filhos', []):
            if isinstance(filho, dict):
                label = filho.get('label', '')
                if label == 'numero_inteiro':
                    elemento = {
                        'subtipo': 'numero_inteiro',
                        'valor': tokens[indice_token] if indice_token < len(tokens) else 'unknown'
                    }
                    indice_token += 1
                elif label == 'numero_real':
                    elemento = {
                        'subtipo': 'numero_real',
                        'valor': tokens[indice_token] if indice_token < len(tokens) else 'unknown'
                    }
                    indice_token += 1
                elif label == 'identifier':
                    elemento = {
                        'subtipo': 'variavel',
                        'valor': tokens[indice_token] if indice_token < len(tokens) else 'unknown'
                    }
                    indice_token += 1
                elif label == 'OPERANDO_OPCIONAL':
                    # Verificar se tem RES
                    for neto in filho.get('filhos', []):
                        if isinstance(neto, dict) and neto.get('label') == 'res':
                            has_res = True
        
        # Se tem RES, modificar o subtipo
        if elemento and has_res:
            elemento['subtipo'] = elemento['subtipo'] + '_res'
        
        return elemento
    
    def _processar_operador_final(op_final_node):
        """Processa um nó OPERADOR_FINAL e retorna o operador"""
        nonlocal indice_token
        if not isinstance(op_final_node, dict):
            return ""
            
        for filho in op_final_node.get('filhos', []):
            if isinstance(filho, dict):
                label = filho.get('label', '')
                # Mapear labels para operadores
                mapeamento_operadores = {
                    'ARITH_OP': {'+': '+', '-': '-', '*': '*', '/': '/', '%': '%', '^': '^', '|': '|'},
                    'COMP_OP': {'>': '>', '<': '<', '>=': '>=', '<=': '<=', '==': '==', '!=': '!='},
                    'LOGIC_OP': {'&&': '&&', '||': '||', '!': '!'},
                    'CONTROL_OP': {'ifelse': 'IFELSE', 'while': 'WHILE', 'for': 'FOR'}
                }
                
                for tipo_op, operadores in mapeamento_operadores.items():
                    if label == tipo_op:
                        # Encontrar o operador específico
                        for neto in filho.get('filhos', []):
                            if isinstance(neto, dict):
                                op_label = neto.get('label', '')
                                if op_label in operadores:
                                    return operadores[op_label]
                    elif label in operadores:
                        return operadores[label]
        
        return ""
    
    # Processar a sequência recursivamente
    def _processar_sequencia(seq_node):
        nonlocal elementos, operador
        
        if not isinstance(seq_node, dict):
            return
            
        filhos = seq_node.get('filhos', [])
        i = 0
        while i < len(filhos):
            filho = filhos[i]
            if isinstance(filho, dict):
                label = filho.get('label', '')
                
                if label == 'OPERANDO':
                    elemento = _processar_operando(filho)
                    if elemento:
                        elementos.append(elemento)
                        
                elif label == 'SEQUENCIA_PRIME':
                    # Processar recursivamente
                    _processar_sequencia(filho)
                    
                elif label == 'OPERADOR_FINAL':
                    operador = _processar_operador_final(filho)
                    
            i += 1
    
    _processar_sequencia(sequencia_node)
    
    return elementos, operador








def _criar_seqs_map(arvore_convertida: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
    """
    Cria o seqs_map necessário para as funções de análise de memória e controle.
    
    Args:
        arvore_convertida: Árvore no formato convertido pelo analisador
        
    Returns:
        Dicionário mapeando número da linha para {'operador': str, 'elementos': List[Dict]}
    """
    seqs_map = {}
    
    for linha in arvore_convertida.get('linhas', []):
        if not isinstance(linha, dict):
            continue
            
        num_linha = linha.get('numero_linha')
        filhos = linha.get('filhos', [])
        
        if filhos and isinstance(filhos[0], dict):
            seq = filhos[0]  # Primeiro filho contém elementos e operador
            elementos = seq.get('elementos', [])
            # Filtrar elementos None e garantir que tenham estrutura válida
            elementos_validos = []
            for elem in elementos:
                if elem is not None and isinstance(elem, dict):
                    elementos_validos.append(elem)
            
            seqs_map[num_linha] = {
                'operador': seq.get('operador'),
                'elementos': elementos_validos
            }
        else:
            seqs_map[num_linha] = {
                'operador': None,
                'elementos': []
            }
    
    return seqs_map


# Função principal delega para a implementação em analisador_tipos.py
# analisarSemantica está implementada em analisador_tipos.py


def analisarSemanticaDaJsonRA2(json_data: Dict[str, Any]) -> Optional[List[str]]:
    """
    Função principal que coordena a análise semântica completa:
    1. Análise de tipos (analisarSemantica)
    2. Análise de memória (analisarSemanticaMemoria)
    3. Análise de controle (analisarSemanticaControle)
    
    Retorna:
        None se não há erros, ou uma lista de strings de erro no formato esperado.
    """
    try:
        # Converter árvore JSON para formato esperado pelo analisador
        arvore_convertida = _converter_arvore_json_para_analisador(json_data)
        
        # Executar análise de tipos
        resultado_tipos = analisarSemanticaTipos(arvore_convertida)
        erros_formatados = []
        
        if isinstance(resultado_tipos, dict):
            if not resultado_tipos.get('sucesso', False):
                # Retornar lista de erros já formatados
                if resultado_tipos.get('erros'):
                    for erro in resultado_tipos['erros']:
                        if isinstance(erro, dict):
                            # O erro já vem formatado da função analisarSemantica
                            erros_formatados.append(erro.get('erro', str(erro)))
                        else:
                            erros_formatados.append(str(erro))
                return erros_formatados if erros_formatados else None
            # Usar a árvore anotada para as próximas análises
            arvore_anotada = resultado_tipos.get('arvore_anotada', arvore_convertida)
            tabela = resultado_tipos.get('tabela_simbolos')
        else:
            # Se retornou string, é um erro
            if resultado_tipos:
                return [resultado_tipos]
            arvore_anotada = arvore_convertida
            tabela = TabelaSimbolos()
        
        # Executar análise de memória
        erros_memoria = analisarSemanticaMemoria(arvore_anotada, _criar_seqs_map(arvore_convertida), tabela)
        if erros_memoria:
            erros_formatados.extend([erro['erro'] for erro in erros_memoria])
        
        # Executar análise de controle
        erros_controle = analisarSemanticaControle(arvore_anotada, _criar_seqs_map(arvore_convertida), tabela)
        if erros_controle:
            erros_formatados.extend([erro['erro'] for erro in erros_controle])
        
        # Se há erros de memória ou controle, retornar todos os erros
        if erros_formatados:
            return erros_formatados
        
        return {'arvore_anotada': arvore_anotada, 'tabela_simbolos': tabela}  # Sucesso
        
    except Exception as e:
        return [f"ERRO INTERNO: {str(e)}"]