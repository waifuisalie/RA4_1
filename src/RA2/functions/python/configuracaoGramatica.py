#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA3_1

# Símbolo inicial da gramática corrigida
SIMBOLO_INICIAL = 'PROGRAM'

GRAMATICA_RPN = {
    'PROGRAM': [['LINHA', 'PROGRAM_PRIME']],
    'PROGRAM_PRIME': [['LINHA', 'PROGRAM_PRIME'], ['epsilon']],
    'LINHA': [['abre_parenteses', 'SEQUENCIA', 'fecha_parenteses']],
    'SEQUENCIA': [['OPERANDO', 'SEQUENCIA_PRIME']],
    'SEQUENCIA_PRIME': [
        ['OPERANDO', 'SEQUENCIA_PRIME'],
        ['OPERADOR_FINAL'],
        ['epsilon']
    ],
    'OPERANDO': [
        ['numero_inteiro', 'OPERANDO_OPCIONAL'],
        ['numero_real', 'OPERANDO_OPCIONAL'],
        ['variavel', 'OPERANDO_OPCIONAL'],
        ['LINHA']
    ],
    'OPERANDO_OPCIONAL': [['res'], ['epsilon']],
    'OPERADOR_FINAL': [
        ['ARITH_OP'], 
        ['COMP_OP'], 
        ['LOGIC_OP'],
        ['CONTROL_OP']
    ],
    'CONTROL_OP': [['for'], ['while'], ['ifelse']],
    'ARITH_OP': [['soma'], ['subtracao'], ['multiplicacao'], ['divisao_inteira'], ['divisao_real'], ['resto'], ['potencia']],
    'COMP_OP': [['menor'], ['maior'], ['igual'], ['menor_igual'], ['maior_igual'], ['diferente']],
    'LOGIC_OP': [['and'], ['or'], ['not']]
}

# Mapeamento dos tokens teóricos para tokens reais do projeto (em minúsculas)
MAPEAMENTO_TOKENS = {
    'numero_inteiro': 'numero_inteiro',
    'numero_real': 'numero_real',
    'variavel': 'identifier', 
    'abre_parenteses': '(',
    'fecha_parenteses': ')',
    'soma': '+',
    'subtracao': '-',
    'multiplicacao': '*',
    'divisao_inteira': '/',
    'divisao_real': '|',
    'resto': '%',
    'potencia': '^',
    'menor': '<',
    'maior': '>',
    'igual': '==',
    'menor_igual': '<=',
    'maior_igual': '>=',
    'diferente': '!=',
    'and': '&&',
    'or': '||',
    'not': '!',
    'for': 'for',
    'while': 'while',
    'ifelse': 'ifelse',
    'res': 'res'
}


# ============================================================================
# FUNÇÕES DE MAPEAMENTO - Centralizadas para evitar duplicação
# ============================================================================

def mapear_gramatica_para_tokens_reais(gramatica_teorica):
    """Converte gramática com tokens teóricos para tokens reais do projeto"""
    gramatica_real = {}
    
    for nt, producoes in gramatica_teorica.items():
        gramatica_real[nt] = []
        for producao in producoes:
            producao_real = []
            for simbolo in producao:
                # Se é um token teórico, mapeia para o real
                if simbolo in MAPEAMENTO_TOKENS:
                    producao_real.append(MAPEAMENTO_TOKENS[simbolo])
                else:
                    producao_real.append(simbolo)
            gramatica_real[nt].append(producao_real)
    
    return gramatica_real

def mapear_tokens_reais_para_teoricos(conjunto_ou_dict):
    """Converte tokens reais de volta para tokens teóricos para exibição"""
    # Cria mapeamento inverso
    mapeamento_inverso = {v: k for k, v in MAPEAMENTO_TOKENS.items()}
    
    if isinstance(conjunto_ou_dict, set):
        # Para conjuntos FIRST/FOLLOW
        return {mapeamento_inverso.get(token, token) for token in conjunto_ou_dict}
    elif isinstance(conjunto_ou_dict, dict):
        # Para tabela LL(1) 
        resultado = {}
        for nt, terminais_dict in conjunto_ou_dict.items():
            resultado[nt] = {}
            for terminal, producao in terminais_dict.items():
                terminal_teorico = mapeamento_inverso.get(terminal, terminal)
                if producao is not None:
                    # Mapear tokens na produção de volta para teóricos
                    producao_teorica = [mapeamento_inverso.get(simbolo, simbolo) for simbolo in producao]
                    resultado[nt][terminal_teorico] = producao_teorica
                else:
                    resultado[nt][terminal_teorico] = None
        return resultado
    else:
        return conjunto_ou_dict
