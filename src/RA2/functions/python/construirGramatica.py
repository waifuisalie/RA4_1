#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

from .configuracaoGramatica import GRAMATICA_RPN, SIMBOLO_INICIAL, mapear_tokens_reais_para_teoricos
from .calcularFirst import calcularFirst
from .calcularFollow import calcularFollow
from .construirTabelaLL1 import construirTabelaLL1, ConflictError

def imprimir_gramatica_completa():
    # Função simplificada que faz tudo inline para exibição
    gramatica_teorica = GRAMATICA_RPN
    simbolo_inicial = SIMBOLO_INICIAL
    
    # Extrai terminais e não-terminais
    nao_terminais = set(gramatica_teorica.keys())
    terminais = set()
    
    for producoes in gramatica_teorica.values():
        for producao in producoes:
            for simbolo in producao:
                if simbolo not in nao_terminais and simbolo != 'epsilon':
                    terminais.add(simbolo)
    
    # Calcular conjuntos
    conjuntos_first_reais = calcularFirst()
    conjuntos_follow_reais = calcularFollow()
    
    conjuntos_first = {nt: mapear_tokens_reais_para_teoricos(conjunto) 
                      for nt, conjunto in conjuntos_first_reais.items()}
    conjuntos_follow = {nt: mapear_tokens_reais_para_teoricos(conjunto) 
                       for nt, conjunto in conjuntos_follow_reais.items()}
    
    # Tabela LL1
    tabela_ll1_teorica = None
    conflitos = []

    try:
        tabela_ll1_reais = construirTabelaLL1()
        tabela_ll1_teorica = mapear_tokens_reais_para_teoricos(tabela_ll1_reais)
    except ConflictError as e:
        conflitos = [str(e)]
    
    # Produções para exibição
    producoes_lista = []
    for nt, producoes in gramatica_teorica.items():
        for producao in producoes:
            if producao == ['epsilon']:
                producoes_lista.append(f"{nt} -> epsilon")
            else:
                producoes_lista.append(f"{nt} -> {' '.join(producao)}")
    
    print(f"\n---- Estrutura da Gramática ----")
    print(f"\n- Símbolo Inicial: \n  {simbolo_inicial}")
    
    print(f"\n- Símbolos Não-Terminais:")
    non_terminals_sorted = sorted(list(nao_terminais))
    print(f"  {{{', '.join(non_terminals_sorted)}}}")
    
    print(f"\n- Símbolos Terminais:")
    terminais_sorted = sorted(list(terminais))
    print(f"  {{{', '.join(terminais_sorted)}}}")
    
    print(f"\n- Regras de Produção:")
    for i, producao in enumerate(producoes_lista, 1):
        print(f"{i:2}. {producao}")
    
    print(f"\n- Conjuntos First:")
    for nt in sorted(conjuntos_first.keys()):
        first_set = conjuntos_first[nt]
        symbols = sorted(list(first_set)) if first_set else ['∅']
        print(f"FIRST({nt}) = {{{', '.join(symbols)}}}")
    
    print(f"\n- Conjuntos Follow:")
    for nt in sorted(conjuntos_follow.keys()):
        follow_set = conjuntos_follow[nt]
        symbols = sorted(list(follow_set)) if follow_set else ['∅']
        print(f"FOLLOW({nt}) = {{{', '.join(symbols)}}}")
    
    print(f"\n- Tabela LL1:")
    if tabela_ll1_teorica:
        
        # Mostrar TODAS as entradas da tabela LL(1)
        table = tabela_ll1_teorica
        total_entries = 0
        
        for nt in sorted(table.keys()):
            for terminal in sorted(table[nt].keys()):
                if table[nt][terminal] is not None:
                    production = ' '.join(table[nt][terminal])
                    print(f"M[{nt}, {terminal}] = {nt} -> {production}")
                    total_entries += 1
        
        print(f"\nTotal de entradas na tabela: {total_entries}")
    else:
        print("Erro na construção da Tabela LL(1)")
    
    if conflitos:
        print(f"\nCONFLITOS LL(1) DETECTADOS:")
        for i, conflito in enumerate(conflitos, 1):
            print(f"{i}. {conflito}")

