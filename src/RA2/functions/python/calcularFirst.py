#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

from .configuracaoGramatica import GRAMATICA_RPN, mapear_gramatica_para_tokens_reais

def calcularFirst():
    # Usa gramática teórica diretamente
    gramatica = GRAMATICA_RPN
    
    # Identifica não-terminais
    nao_terminais = set(gramatica.keys())
    
    # Inicialização
    FIRST = {nt: set() for nt in nao_terminais}
    
    # Adiciona ε ao FIRST de todos os não-terminais que são NULLABLE
    # (Integrado no loop principal conforme referência)
    
    mudou = True
    while mudou:
        mudou = False
        for nt_head, producoes in gramatica.items():
            for producao in producoes:
                # Produção vazia
                if producao == ['epsilon']:
                    if 'epsilon' not in FIRST[nt_head]:
                        FIRST[nt_head].add('epsilon')
                        mudou = True
                    continue
                
                for simbolo in producao:
                    # Se o símbolo é um terminal
                    if simbolo not in nao_terminais:
                        if simbolo not in FIRST[nt_head]:
                            FIRST[nt_head].add(simbolo)
                            mudou = True
                        break  # interrompe a análise aqui
                    
                    # Se o símbolo é um não-terminal
                    else:
                        tamanho_anterior = len(FIRST[nt_head])
                        FIRST[nt_head].update(FIRST[simbolo] - {'epsilon'})
                        if len(FIRST[nt_head]) > tamanho_anterior:
                            mudou = True

                        if 'epsilon' not in FIRST[simbolo]:
                            break  # interrompe a análise aqui
    
    return FIRST


def calcular_first_da_sequencia(sequencia, FIRST, nao_terminais):
    first_seq = set()

    for simbolo in sequencia:
        if simbolo not in nao_terminais:  # É terminal
            first_seq.add(simbolo)
            return first_seq
        else:  # É não-terminal
            first_seq.update(FIRST[simbolo] - {'epsilon'})
            if 'epsilon' not in FIRST[simbolo]:
                return first_seq

    # Se chegou aqui, todos os símbolos da sequência são NULLABLE
    first_seq.add('epsilon')
    return first_seq
