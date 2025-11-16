#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

from .configuracaoGramatica import GRAMATICA_RPN, SIMBOLO_INICIAL, mapear_gramatica_para_tokens_reais
from .calcularFirst import calcularFirst, calcular_first_da_sequencia

def calcularFollow():
    # Mapeia gramática teórica para tokens reais do projeto
    gramatica = mapear_gramatica_para_tokens_reais(GRAMATICA_RPN)
    simbolo_inicial = SIMBOLO_INICIAL
    nao_terminais = set(gramatica.keys())
    
    # Calcula FIRST primeiro (necessário para FOLLOW)
    FIRST = calcularFirst()
    
    # Inicialização
    FOLLOW = {nt: set() for nt in nao_terminais}
    
    # Regra 1: Adiciona $ ao FOLLOW do símbolo inicial
    FOLLOW[simbolo_inicial].add('$')
    
    mudou = True
    while mudou:
        mudou = False
        # Itera sobre cada produção da gramática
        for nt_head, producoes in gramatica.items():
            for producao in producoes:
                # Itera sobre cada símbolo da produção
                for i, simbolo in enumerate(producao):
                    if simbolo in nao_terminais:
                        beta = producao[i+1:]  # resto da produção após o símbolo
                        
                        # Regra 2.a: Adicionar FIRST(beta) a FOLLOW(simbolo)
                        if beta:
                            first_beta = calcular_first_da_sequencia(beta, FIRST, nao_terminais)
                            
                            tamanho_anterior = len(FOLLOW[simbolo])
                            FOLLOW[simbolo].update(first_beta - {'epsilon'})
                            if len(FOLLOW[simbolo]) > tamanho_anterior:
                                mudou = True

                            # Regra 2.b: Se beta é NULLABLE, adicionar FOLLOW(head) a FOLLOW(simbolo)
                            if 'epsilon' in first_beta:
                                tamanho_anterior = len(FOLLOW[simbolo])
                                FOLLOW[simbolo].update(FOLLOW[nt_head])
                                if len(FOLLOW[simbolo]) > tamanho_anterior:
                                    mudou = True
                        
                        # Regra 2.b (caso beta seja vazio): Adicionar FOLLOW(head) a FOLLOW(simbolo)
                        else:
                            tamanho_anterior = len(FOLLOW[simbolo])
                            FOLLOW[simbolo].update(FOLLOW[nt_head])
                            if len(FOLLOW[simbolo]) > tamanho_anterior:
                                mudou = True
    
    return FOLLOW
