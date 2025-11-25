#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

from .configuracaoGramatica import GRAMATICA_RPN, mapear_gramatica_para_tokens_reais
from .calcularFirst import calcularFirst, calcular_first_da_sequencia
from .calcularFollow import calcularFollow

class ConflictError(Exception):
    pass

def construirTabelaLL1():
    # Usa gramática teórica diretamente
    gramatica = GRAMATICA_RPN
    nao_terminais = set(gramatica.keys())
    
    # Identifica todos os terminais
    todos_simbolos = set(nao_terminais)
    for producoes in gramatica.values():
        for producao in producoes:
            todos_simbolos.update(producao)
    terminais = sorted(list(todos_simbolos - nao_terminais - {'epsilon'})) + ['$']
    
    # Calcula conjuntos FIRST e FOLLOW
    FIRST = calcularFirst()
    FOLLOW = calcularFollow()
    
    # Inicializa tabela
    tabela = {nt: {t: None for t in terminais} for nt in nao_terminais}
    
    # Preenche a tabela conforme algoritmo da referência
    for nt_head, producoes in gramatica.items():
        for producao in producoes:
            first_producao = calcular_first_da_sequencia(producao, FIRST, nao_terminais)
            
            # Regra 1: FIRST
            for terminal in first_producao - {'epsilon'}:
                if tabela[nt_head][terminal] is not None:
                    raise ConflictError(
                        f"Conflito FIRST/FIRST em [{nt_head}, {terminal}]! "
                        f"Produção existente: {tabela[nt_head][terminal]}, "
                        f"Nova produção: {producao}"
                    )
                tabela[nt_head][terminal] = producao

            # Regra 2: FOLLOW (se a produção pode derivar epsilon)
            if 'epsilon' in first_producao:
                for terminal in FOLLOW[nt_head]:
                    if tabela[nt_head][terminal] is not None:
                        raise ConflictError(
                            f"Conflito FIRST/FOLLOW em [{nt_head}, {terminal}]! "
                            f"Produção existente: {tabela[nt_head][terminal]}, "
                            f"Nova produção: {producao}"
                        )
                    tabela[nt_head][terminal] = producao

    return tabela

