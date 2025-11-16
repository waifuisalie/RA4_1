#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1

from typing import Dict, Any, List
from src.RA3.functions.python.tabela_simbolos import TabelaSimbolos
from src.RA3.functions.python import tipos
from src.RA3.functions.python.analisador_tipos import avaliar_seq_tipo, _parse_valor_literal, ErroSemantico


def analisarSemanticaMemoria(arvore_anotada_local: Dict[str, Any], seqs_map: Dict[int, Dict[str, Any]], tabela_local: TabelaSimbolos) -> List[Dict[str, Any]]:
    erros_m: List[Dict[str, Any]] = []
    mapa = {l['numero_linha']: l for l in arvore_anotada_local.get('linhas', [])}

    for linha in arvore_anotada_local.get('linhas', []):
        num = linha['numero_linha']
        seq = seqs_map.get(num)
        if not seq:
            continue
        operador = seq.get('operador')
        elementos = seq.get('elementos', [])

        if operador is None and len(elementos) == 2 and elementos[1].get('subtipo') == 'variavel':
            # Atribuição: primeiro elemento é a fonte, segundo é o destino
            fonte_tipo = None
            destino = elementos[1].get('valor')

            # Verificar se o primeiro elemento é uma subexpressão (LINHA)
            if elementos[0].get('subtipo') == 'LINHA':
                # Avaliar o tipo da subexpressão
                try:
                    fonte_tipo, _, _ = avaliar_seq_tipo(elementos[0].get('ast'), num, tabela_local)
                except ErroSemantico:
                    fonte_tipo = None
            else:
                # Primeiro elemento é um valor direto
                fonte_tipo = linha.get('tipo')

            if fonte_tipo is None:
                erros_m.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: Tipo da fonte desconhecido para armazenamento\nContexto: ({destino})"})
            else:
                try:
                    tabela_local.adicionarSimbolo(destino, fonte_tipo, inicializada=True, linha=num)
                    linha['tipo'] = fonte_tipo
                except ValueError as e:
                    erros_m.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: {str(e)}\nContexto: ({destino})"})
            continue

        if operador is None and len(elementos) == 1 and elementos[0].get('subtipo') == 'variavel':
            var = elementos[0].get('valor')
            if not tabela_local.existe(var) or not tabela_local.verificar_inicializacao(var):
                erros_m.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: Memória '{var}' utilizada sem inicialização\nContexto: ({var})"})
            else:
                linha['tipo'] = tabela_local.obter_tipo(var)
            continue

        if operador == 'RES' or (operador in [None, ''] and elementos and any(e.get('subtipo', '').endswith('_res') for e in elementos)):
            if not elementos:
                erros_m.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: Operando RES inválido\nContexto: RES"})
                continue
            oper = elementos[0]
            offset = None
            if oper.get('subtipo') in ['numero_real', 'numero_inteiro', 'numero_real_res', 'numero_inteiro_res']:
                val = _parse_valor_literal(oper)
                if not isinstance(val, int) or val < 1:
                    erros_m.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: Referência RES deve ter índice inteiro positivo\nContexto: RES"})
                    continue
                offset = val
            elif oper.get('subtipo') == 'variavel':
                var_name = oper.get('valor')
                if not tabela_local.existe(var_name) or not tabela_local.verificar_inicializacao(var_name):
                    erros_m.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: Variável '{var_name}' utilizada em RES sem inicialização\nContexto: RES"})
                    continue
                var_tipo = tabela_local.obter_tipo(var_name)
                if var_tipo != tipos.TYPE_INT:
                    erros_m.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: Variável em RES deve ser do tipo int\nContexto: RES"})
                    continue
                # Para implementação completa, precisaríamos do valor da variável
                # Por enquanto, assumimos que não podemos resolver o valor em tempo de análise
                erros_m.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: RES com variável como offset não suportado - requer avaliação em tempo de execução\nContexto: RES"})
                continue
            else:
                erros_m.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: Operando RES inválido\nContexto: RES"})
                continue
            
            if offset is not None:
                linha_ref = num - offset  # RES N significa resultado de N linhas para trás (linha atual - N)
                if linha_ref < 1:
                    erros_m.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: Referência RES aponta para linha inexistente\nContexto: RES"})
                    continue
                ref_l = mapa.get(linha_ref)
                if not ref_l or ref_l.get('tipo') is None:
                    erros_m.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: Referência RES aponta para linha sem tipo conhecido\nContexto: RES"})
                    continue
                linha['tipo'] = ref_l.get('tipo')
                continue

    return erros_m


def analisarSemanticaControle(arvore_anotada_local: Dict[str, Any], seqs_map: Dict[int, Dict[str, Any]], tabela_local: TabelaSimbolos) -> List[Dict[str, Any]]:
    erros_c: List[Dict[str, Any]] = []

    for linha in arvore_anotada_local.get('linhas', []):
        num = linha['numero_linha']
        seq = seqs_map.get(num)
        if not seq:
            continue
        operador = seq.get('operador')
        elementos = seq.get('elementos', [])

        if operador == 'IFELSE':
            if len(elementos) < 3:
                erros_c.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: IFELSE mal formado\nContexto: IFELSE"})
                continue

            # Buscar tipos na árvore anotada
            for linha_anotada in arvore_anotada_local.get('linhas', []):
                if linha_anotada.get('numero_linha') == num:
                    # Verificar tipos dos elementos diretamente
                    break

            # Verificar tipos dos elementos diretamente
            if elementos[0].get('subtipo') == 'LINHA':
                # Subexpressão - deve ter sido processada pelo analisador de tipos
                # Por enquanto, assumimos que expressões de comparação resultam em boolean
                cond_expr = elementos[0].get('ast', {})
                if cond_expr.get('operador') in ['>', '<', '>=', '<=', '==', '!=', '&&', '||']:
                    cond_tipo = tipos.TYPE_BOOLEAN
                else:
                    cond_tipo = None
            elif elementos[0].get('subtipo') == 'numero_real':
                v = _parse_valor_literal(elementos[0])
                cond_tipo = tipos.TYPE_INT if isinstance(v, int) else tipos.TYPE_REAL
            elif elementos[0].get('subtipo') == 'variavel':
                cond_tipo = tabela_local.obter_tipo(elementos[0].get('valor')) if tabela_local.existe(elementos[0].get('valor')) else None

            # Mesmo para os ramos true/false - assumimos que são expressões válidas
            # Em um analisador completo, verificaríamos consistência de tipos
            if not tipos.tipo_compativel_condicao(cond_tipo):
                erros_c.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: Condição IFELSE inválida (não convertível para boolean)\nContexto: IFELSE"})
                continue

            # IFELSE retorna o tipo do ramo executado (true ou false)
            # Para simplificar, assumimos que ambos os ramos têm o mesmo tipo
            # Em implementação completa, deveria verificar consistência
            if len(elementos) >= 3:
                # Verificar tipos dos ramos true e false
                true_branch = elementos[1]
                false_branch = elementos[2]
                
                true_type = None
                false_type = None
                
                # Determinar tipo do ramo true
                if true_branch.get('subtipo') == 'numero_real':
                    v = _parse_valor_literal(true_branch)
                    true_type = tipos.TYPE_INT if isinstance(v, int) else tipos.TYPE_REAL
                elif true_branch.get('subtipo') == 'variavel':
                    true_type = tabela_local.obter_tipo(true_branch.get('valor')) if tabela_local.existe(true_branch.get('valor')) else None
                elif true_branch.get('subtipo') == 'LINHA':
                    true_type, _, _ = avaliar_seq_tipo(true_branch.get('ast'), num, tabela_local)
                
                # Determinar tipo do ramo false
                if false_branch.get('subtipo') == 'numero_real':
                    v = _parse_valor_literal(false_branch)
                    false_type = tipos.TYPE_INT if isinstance(v, int) else tipos.TYPE_REAL
                elif false_branch.get('subtipo') == 'variavel':
                    false_type = tabela_local.obter_tipo(false_branch.get('valor')) if tabela_local.existe(false_branch.get('valor')) else None
                elif false_branch.get('subtipo') == 'LINHA':
                    false_type, _, _ = avaliar_seq_tipo(false_branch.get('ast'), num, tabela_local)
                
                # IFELSE retorna o tipo comum entre os ramos
                if true_type == false_type:
                    linha['tipo'] = true_type
                elif true_type in [tipos.TYPE_INT, tipos.TYPE_REAL] and false_type in [tipos.TYPE_INT, tipos.TYPE_REAL]:
                    # Promoção de tipos numéricos
                    linha['tipo'] = tipos.TYPE_REAL  # int + real = real
                else:
                    linha['tipo'] = true_type or false_type  # fallback
            else:
                linha['tipo'] = tipos.TYPE_REAL  # fallback para casos malformados

        if operador == 'WHILE':
            if len(elementos) < 2:
                erros_c.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: WHILE mal formado\nContexto: WHILE"})
                continue

            # Verificar condição do WHILE
            cond_tipo = None
            if elementos[0].get('subtipo') == 'LINHA':
                # Subexpressão - verificar se é operação de comparação
                cond_expr = elementos[0].get('ast', {})
                if cond_expr.get('operador') in ['>', '<', '>=', '<=', '==', '!=', '&&', '||']:
                    cond_tipo = tipos.TYPE_BOOLEAN
                else:
                    cond_tipo = None
            elif elementos[0].get('subtipo') == 'numero_real':
                v = _parse_valor_literal(elementos[0])
                cond_tipo = tipos.TYPE_INT if isinstance(v, int) else tipos.TYPE_REAL
            elif elementos[0].get('subtipo') == 'variavel':
                cond_tipo = tabela_local.obter_tipo(elementos[0].get('valor')) if tabela_local.existe(elementos[0].get('valor')) else None

            if not tipos.tipo_compativel_condicao(cond_tipo):
                erros_c.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: Condição WHILE inválida (não convertível para boolean)\nContexto: WHILE"})
                continue

            # WHILE retorna o tipo do corpo do loop (último valor calculado)
            if len(elementos) >= 2 and elementos[1].get('subtipo') == 'LINHA':
                body_type, _, _ = avaliar_seq_tipo(elementos[1].get('ast'), num, tabela_local)
                linha['tipo'] = body_type
            else:
                linha['tipo'] = None  # fallback para casos malformados

        if operador == 'FOR':
            if len(elementos) < 4:
                erros_c.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: FOR mal formado\nContexto: FOR"})
                continue
            def tipo_simples(el):
                if el.get('subtipo') == 'numero_real':
                    v = _parse_valor_literal(el)
                    return tipos.TYPE_INT if isinstance(v, int) else tipos.TYPE_REAL
                if el.get('subtipo') == 'variavel':
                    return tabela_local.obter_tipo(el.get('valor')) if tabela_local.existe(el.get('valor')) else None
                if el.get('subtipo') == 'LINHA':
                    t, _, _ = avaliar_seq_tipo(el.get('ast'), num, tabela_local)
                    return t
                return None

            init_t = tipo_simples(elementos[0])
            end_t = tipo_simples(elementos[1])
            step_t = tipo_simples(elementos[2])
            if init_t != tipos.TYPE_INT or end_t != tipos.TYPE_INT or step_t != tipos.TYPE_INT:
                erros_c.append({'linha': num, 'erro': f"ERRO SEMÂNTICO [Linha {num}]: FOR requer início, fim e passo inteiros\nContexto: FOR"})
                continue
            if elementos[3].get('subtipo') == 'LINHA':
                body_t, _, _ = avaliar_seq_tipo(elementos[3].get('ast'), num, tabela_local)
                linha['tipo'] = body_t

    return erros_c
