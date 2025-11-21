#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1

from typing import Dict, Any, List, Optional, Tuple
from src.RA3.functions.python import tipos
from src.RA3.functions.python.tabela_simbolos import TabelaSimbolos, inicializarTabelaSimbolos
from src.RA3.functions.python.gramatica_atributos import obter_regra, definirGramaticaAtributos


class ErroSemantico(Exception):
    def __init__(self, linha: int, mensagem: str, contexto: Optional[str] = None):
        self.linha = linha
        self.mensagem = mensagem
        self.contexto = contexto
        super().__init__(f"ERRO SEMÂNTICO [Linha {linha}]: {mensagem}\nContexto: {contexto}")


def _construir_contexto_expressao(linha_ou_seq: Dict[str, Any]) -> str:
    """
    Constrói um contexto mais informativo para mensagens de erro,
    mostrando a expressão completa ao invés de apenas o operador.
    Aceita tanto uma linha da árvore sintática quanto uma seq.
    """
    try:
        # Verificar se é uma linha da árvore (tem 'filhos') ou uma seq direta
        if 'filhos' in linha_ou_seq:
            # É uma linha da árvore sintática
            filhos = linha_ou_seq.get('filhos', [])
            if filhos:
                seq = filhos[0]  # Primeiro filho contém elementos e operador
            else:
                return "(linha vazia)"
        else:
            # É uma seq direta
            seq = linha_ou_seq
        
        operador = seq.get('operador', '')
        elementos = seq.get('elementos', [])
        
        # Construir representação da expressão
        partes = []
        for elem in elementos:
            if isinstance(elem, dict):
                subtipo = elem.get('subtipo', '')
                if subtipo in ['numero_real', 'numero_inteiro', 'numero_real_res', 'numero_inteiro_res']:
                    partes.append(str(elem.get('valor', '')))
                elif subtipo == 'variavel':
                    partes.append(str(elem.get('valor', '')))
                elif subtipo == 'LINHA':
                    partes.append('(subexpressão)')
                else:
                    partes.append(str(elem.get('valor', '?')))
            else:
                partes.append(str(elem))
        
        if operador and partes:
            # Para operadores binários
            if len(partes) >= 2:
                return f"({partes[0]} {operador} {partes[1]})"
            # Para operadores unários
            elif len(partes) == 1:
                if operador in ['!', '-']:
                    return f"({operador}{partes[0]})"
                else:
                    return f"({partes[0]} {operador})"
            else:
                return f"({operador})"
        elif partes:
            # Sem operador, apenas operandos
            return f"({' '.join(partes)})"
        else:
            return "(expressão vazia)"
    except Exception:
        # Fallback para casos onde a estrutura não é a esperada
        return "(estrutura não reconhecida)"


def _parse_valor_literal(token: Dict[str, Any]) -> Any:
    if token.get('subtipo') not in ['numero_real', 'numero_inteiro', 'numero_real_res', 'numero_inteiro_res']:
        return None
    raw = token.get('valor')
    if raw is None:
        return None
    try:
        # Para numero_inteiro e numero_inteiro_res, sempre retorna int
        if token.get('subtipo') in ['numero_inteiro', 'numero_inteiro_res']:
            return int(raw)
        # Para numero_real e numero_real_res, sempre retorna float
        elif token.get('subtipo') in ['numero_real', 'numero_real_res']:
            return float(raw)
        # Fallback: tentar float
        return float(raw)
    except Exception:
        try:
            return float(raw)
        except Exception:
            return None


def _avaliar_operando(operando: Dict[str, Any], tabela: TabelaSimbolos, historico_tipos: Dict[int, str], linha_atual: int) -> Dict[str, Any]:
    if operando.get('subtipo') in ['numero_real', 'numero_inteiro', 'numero_real_res', 'numero_inteiro_res']:
        valor = _parse_valor_literal(operando)
        tipo = tipos.TYPE_INT if isinstance(valor, int) else tipos.TYPE_REAL
        return {'tipo': tipo, 'valor': valor}

    if operando.get('subtipo') == 'variavel':
        nome = operando.get('valor')
        if not tabela.existe(nome):
            # Variável não existe - erro semântico
            raise ErroSemantico(linha_atual, f"Variável '{nome}' não declarada", f"({nome})")
        if not tabela.verificar_inicializacao(nome):
            # Não lançar erro aqui - deixar para o analisador de memória
            return {'tipo': None, 'valor': None, 'variavel': nome}
        tipo = tabela.obter_tipo(nome)
        return {'tipo': tipo, 'valor': None, 'variavel': nome}

    if operando.get('subtipo') == 'LINHA':
        # Avaliar subexpressão LINHA recursivamente
        elementos_sub = operando.get('elementos', [])
        operador_sub = operando.get('operador')
        
        # Avaliar operandos da subexpressão
        operandos_sub_av = []
        for op_sub in elementos_sub:
            try:
                aval_sub = _avaliar_operando(op_sub, tabela, historico_tipos, linha_atual)
                operandos_sub_av.append(aval_sub)
            except ErroSemantico:
                operandos_sub_av.append({'tipo': None, 'valor': None})
        
        # Determinar tipo da subexpressão baseado no operador
        if operador_sub:
            if operador_sub in ['+', '-', '*', '/', '%', '^', '|']:
                # Operador aritmético
                if len(operandos_sub_av) >= 2:
                    left, right = operandos_sub_av[0], operandos_sub_av[1]
                    if left['tipo'] is not None and right['tipo'] is not None:
                        try:
                            tipo_sub = tipos.tipo_resultado_aritmetica(left['tipo'], right['tipo'], operador_sub)
                        except ValueError as ve:
                            raise ErroSemantico(linha_atual, str(ve), f"({left['tipo']} {operador_sub} {right['tipo']})")
                    else:
                        tipo_sub = None
                else:
                    tipo_sub = operandos_sub_av[0]['tipo'] if operandos_sub_av else None
            elif operador_sub in ['>', '<', '>=', '<=', '==', '!=']:
                # Operador de comparação
                if len(operandos_sub_av) >= 2:
                    left, right = operandos_sub_av[0], operandos_sub_av[1]
                    if left['tipo'] is not None and right['tipo'] is not None:
                        try:
                            tipo_sub = tipos.tipo_resultado_comparacao(left['tipo'], right['tipo'])
                        except ValueError as ve:
                            raise ErroSemantico(linha_atual, str(ve), f"({left['tipo']} {operador_sub} {right['tipo']})")
                    else:
                        tipo_sub = None
                else:
                    tipo_sub = None
            elif operador_sub in ['&&', '||']:
                # Operador lógico binário
                if len(operandos_sub_av) >= 2:
                    left, right = operandos_sub_av[0], operandos_sub_av[1]
                    if left['tipo'] is not None and right['tipo'] is not None:
                        try:
                            tipo_sub = tipos.tipo_resultado_logico(left['tipo'], right['tipo'])
                        except ValueError as ve:
                            raise ErroSemantico(linha_atual, str(ve), f"({left['tipo']} {operador_sub} {right['tipo']})")
                    else:
                        tipo_sub = None
                else:
                    tipo_sub = None
            elif operador_sub == '!':
                # Operador lógico unário
                if len(operandos_sub_av) >= 1:
                    operando = operandos_sub_av[0]
                    if operando['tipo'] is not None:
                        try:
                            tipo_sub = tipos.tipo_resultado_logico_unario(operando['tipo'])
                        except ValueError as ve:
                            raise ErroSemantico(linha_atual, str(ve), f"(!{operando['tipo']})")
                    else:
                        tipo_sub = None
                else:
                    tipo_sub = None
            else:
                tipo_sub = None
        else:
            # Sem operador - apenas um operando
            tipo_sub = operandos_sub_av[0]['tipo'] if operandos_sub_av else None
        
        return {'tipo': tipo_sub, 'valor': None}

    if operando.get('tipo'):
        return {'tipo': operando.get('tipo'), 'valor': operando.get('valor')}

    raise ErroSemantico(linha_atual, f"Operando desconhecido ou inválido: {operando}")


def avaliar_seq_tipo(seq: Dict[str, Any], linha_atual: int, tabela: TabelaSimbolos) -> Tuple[Optional[str], List[Optional[str]], List[Any]]:
    operador = seq.get('operador')
    elementos = seq.get('elementos', [])

    # Normalizar operador vazio para None
    if operador == "":
        operador = None

    def eval_oper(op):
        if op.get('subtipo') in ['numero_real', 'numero_inteiro', 'numero_real_res', 'numero_inteiro_res']:
            v = _parse_valor_literal(op)
            return (tipos.TYPE_INT if isinstance(v, int) else tipos.TYPE_REAL, v)
        if op.get('subtipo') == 'variavel':
            nome = op.get('valor')
            if tabela.existe(nome):
                return (tabela.obter_tipo(nome), None)
            return (None, None)
        if op.get('subtipo') == 'LINHA':
            # Avaliar subexpressão LINHA recursivamente
            ast_sub = op.get('ast')
            if ast_sub:
                t, _, _ = avaliar_seq_tipo(ast_sub, linha_atual, tabela)
                return (t, None)
            return (None, None)
        raise ErroSemantico(linha_atual, f"Operando desconhecido: {op}")

    tipos_ops = []
    vals = []
    for op in elementos:
        if isinstance(op, dict) and op.get('subtipo') == 'operador_token':
            continue
        t, v = eval_oper(op)
        tipos_ops.append(t)
        vals.append(v)

    if operador is None and len(tipos_ops) == 2 and elementos[1].get('subtipo') == 'variavel':
        return (tipos_ops[0], tipos_ops, vals)

    if operador is not None and operador != "":
        regra = obter_regra(operador)
        if regra is None:
            raise ErroSemantico(linha_atual, f"Operador desconhecido: {operador}", _construir_contexto_expressao(seq))
        cat = regra.get('categoria')

        if cat == 'aritmetico':
            if operador == '-' and len(tipos_ops) == 1:
                return (tipos_ops[0], tipos_ops, vals)
            if len(tipos_ops) < 2:
                raise ErroSemantico(linha_atual, 'Operador aritmético com aridade inválida', _construir_contexto_expressao(seq))
            left, right = tipos_ops[0], tipos_ops[1]
            if left is None or right is None:
                return (None, tipos_ops, vals)
            try:
                tipo_resultado = tipos.tipo_resultado_aritmetica(left, right, operador)
                return (tipo_resultado, tipos_ops, vals)
            except ValueError as ve:
                raise ErroSemantico(linha_atual, str(ve), _construir_contexto_expressao(seq))

        if cat == 'comparacao':
            left, right = tipos_ops[0], tipos_ops[1]
            if left is None or right is None:
                return (None, tipos_ops, vals)
            try:
                tipo_resultado = tipos.tipo_resultado_comparacao(left, right)
                return (tipo_resultado, tipos_ops, vals)
            except ValueError as ve:
                raise ErroSemantico(linha_atual, str(ve), _construir_contexto_expressao(seq))

        if cat == 'logico':
            if operador in ['&&', '||']:
                a, b = tipos_ops[0], tipos_ops[1]
                if a is None or b is None:
                    return (None, tipos_ops, vals)
                try:
                    tipo_resultado = tipos.tipo_resultado_logico(a, b)
                    return (tipo_resultado, tipos_ops, vals)
                except ValueError as ve:
                    raise ErroSemantico(linha_atual, str(ve), _construir_contexto_expressao(seq))
            if operador == '!':
                a = tipos_ops[0]
                if a is None:
                    return (None, tipos_ops, vals)
                try:
                    tipo_resultado = tipos.tipo_resultado_logico_unario(a)
                    return (tipo_resultado, tipos_ops, vals)
                except ValueError as ve:
                    raise ErroSemantico(linha_atual, str(ve), _construir_contexto_expressao(seq))

    if operador is None and len(tipos_ops) == 1:
        return (tipos_ops[0], tipos_ops, vals)

    raise ErroSemantico(linha_atual, 'Estrutura da linha não reconhecida ou suporte incompleto', str(seq))


def analisarSemantica(arvoreSintatica: Dict[str, Any], gramatica: Optional[Dict] = None, tabela: Optional[TabelaSimbolos] = None) -> Dict[str, Any]:
    if gramatica is None:
        gramatica = definirGramaticaAtributos()
    if tabela is None:
        tabela = inicializarTabelaSimbolos()

    erros: List[Dict[str, Any]] = []
    linhas = arvoreSintatica.get('linhas', [])
    arvore_anotada = {'linhas': []}
    historico_tipos: Dict[int, Optional[str]] = {}

    for linha_ast in linhas:
        num = linha_ast.get('numero_linha', None)
        try:
            # Usar a estrutura convertida: cada linha tem 'filhos' com 'elementos' e 'operador'
            filhos = linha_ast.get('filhos', [])
            if not filhos:
                continue
                
            seq = filhos[0]  # Primeiro filho contém elementos e operador
            elementos = seq.get('elementos', [])
            operador = seq.get('operador', None)

            # Verificar se é armazenamento (valor variável) ANTES de avaliar operandos
            if (operador is None or operador == "") and len(elementos) == 2:
                if elementos[1].get('subtipo') == 'variavel':
                    nome_var = elementos[1].get('valor')
                    # Avaliar apenas o primeiro operando (o valor)
                    try:
                        fonte = _avaliar_operando(elementos[0], tabela, historico_tipos, num)
                        tipo_res = fonte['tipo']
                        if tipo_res is not None:
                            if not tipos.tipo_compativel_armazenamento(tipo_res):
                                raise ErroSemantico(num, f"Tipo '{tipo_res}' não pode ser armazenado em memória. Apenas tipos numéricos são permitidos", _construir_contexto_expressao(linha_ast))
                            tabela.adicionarSimbolo(nome_var, tipo_res, inicializada=True, linha=num)
                    except ErroSemantico:
                        # Se o valor não puder ser avaliado ou armazenado, não declarar a variável
                        pass
                    historico_tipos[num] = tipo_res
                    nova_linha = dict(linha_ast)
                    nova_linha['tipo'] = tipo_res
                    arvore_anotada['linhas'].append(nova_linha)
                    continue

            # Para outras operações, avaliar todos os operandos
            operandos_av = []
            for op in elementos:
                aval = _avaliar_operando(op, tabela, historico_tipos, num)
                operandos_av.append(aval)

            if operador is not None and operador != "":
                regra = obter_regra(operador)
                if regra is None:
                    raise ErroSemantico(num, f"Operador desconhecido: {operador}", _construir_contexto_expressao(linha_ast))
                cat = regra.get('categoria')

                if cat == 'aritmetico':
                    if len(operandos_av) == 1 and operador == '-':
                        a = operandos_av[0]
                        tipo_res = a['tipo']
                        # Propagate type to operation node
                        seq['tipo'] = tipo_res
                        historico_tipos[num] = tipo_res
                        nova_linha = dict(linha_ast)
                        nova_linha['tipo'] = tipo_res
                        arvore_anotada['linhas'].append(nova_linha)
                        continue
                    if len(operandos_av) < 2:
                        raise ErroSemantico(num, 'Operador aritmético com aridade inválida', _construir_contexto_expressao(linha_ast))
                    left, right = operandos_av[0], operandos_av[1]
                    if left['tipo'] is None or right['tipo'] is None:
                        tipo_res = None
                    else:
                        try:
                            tipo_res = tipos.tipo_resultado_aritmetica(left['tipo'], right['tipo'], operador)
                        except ValueError as ve:
                            raise ErroSemantico(num, str(ve), _construir_contexto_expressao(linha_ast))

                    # Propagate type to operation node
                    seq['tipo'] = tipo_res
                    historico_tipos[num] = tipo_res
                    nova_linha = dict(linha_ast)
                    nova_linha['tipo'] = tipo_res
                    arvore_anotada['linhas'].append(nova_linha)
                    continue

                if cat == 'comparacao':
                    left, right = operandos_av[0], operandos_av[1]
                    if left['tipo'] is None or right['tipo'] is None:
                        tipo_res = None
                    else:
                        try:
                            tipo_res = tipos.tipo_resultado_comparacao(left['tipo'], right['tipo'])
                        except ValueError as ve:
                            raise ErroSemantico(num, str(ve), _construir_contexto_expressao(linha_ast))
                    # Propagate type to operation node
                    seq['tipo'] = tipo_res
                    historico_tipos[num] = tipo_res
                    nova_linha = dict(linha_ast)
                    nova_linha['tipo'] = tipo_res
                    arvore_anotada['linhas'].append(nova_linha)
                    continue

                if cat == 'logico':
                    if operador in ['&&', '||']:
                        if len(operandos_av) < 2:
                            raise ErroSemantico(num, f'Operador lógico binário "{operador}" requer 2 operandos', _construir_contexto_expressao(linha_ast))
                        a, b = operandos_av[0], operandos_av[1]
                        if a['tipo'] is None or b['tipo'] is None:
                            tipo_res = None
                        else:
                            try:
                                tipo_res = tipos.tipo_resultado_logico(a['tipo'], b['tipo'])
                            except ValueError as ve:
                                raise ErroSemantico(num, str(ve), _construir_contexto_expressao(linha_ast))
                        # Propagate type to operation node
                        seq['tipo'] = tipo_res
                        historico_tipos[num] = tipo_res
                        nova_linha = dict(linha_ast)
                        nova_linha['tipo'] = tipo_res
                        arvore_anotada['linhas'].append(nova_linha)
                        continue
                    if operador == '!':
                        if len(operandos_av) < 1:
                            raise ErroSemantico(num, 'Operador lógico unário "!" requer 1 operando', _construir_contexto_expressao(linha_ast))
                        a = operandos_av[0]
                        if a['tipo'] is None:
                            tipo_res = None
                        else:
                            try:
                                tipo_res = tipos.tipo_resultado_logico_unario(a['tipo'])
                            except ValueError as ve:
                                raise ErroSemantico(num, str(ve), _construir_contexto_expressao(linha_ast))
                        # Propagate type to operation node
                        seq['tipo'] = tipo_res
                        historico_tipos[num] = tipo_res
                        nova_linha = dict(linha_ast)
                        nova_linha['tipo'] = tipo_res
                        arvore_anotada['linhas'].append(nova_linha)
                        continue

                # Não rejeitar - deixar para o analisador de memória/controle
                if operador in ['RES', 'IFELSE', 'WHILE', 'FOR']:
                    historico_tipos[num] = None  # Tipo será determinado pelo analisador_memoria_controle
                    nova_linha = dict(linha_ast)
                    nova_linha['tipo'] = None
                    arvore_anotada['linhas'].append(nova_linha)
                    continue

                historico_tipos[num] = None
                nova_linha = dict(linha_ast)
                nova_linha['tipo'] = None
                arvore_anotada['linhas'].append(nova_linha)
                continue

            if (operador is None or operador == "") and len(elementos) == 1:
                op = elementos[0]
                try:
                    aval = _avaliar_operando(op, tabela, historico_tipos, num)
                    tipo_v = aval.get('tipo')
                    # Verificar se é RES (resultado)
                    if op.get('subtipo', '').endswith('_res'):
                        # Operação RES - não produz tipo, apenas indica armazenamento de resultado
                        tipo_v = None
                    # Verificar se é variável não inicializada
                    elif aval.get('variavel') and tipo_v is None:
                        raise ErroSemantico(num, f"Variável '{aval['variavel']}' utilizada sem inicialização", f"({aval['variavel']})")
                except ErroSemantico:
                    tipo_v = None
                    raise  # Re-lançar o erro
                historico_tipos[num] = tipo_v
                nova_linha = dict(linha_ast)
                nova_linha['tipo'] = tipo_v
                arvore_anotada['linhas'].append(nova_linha)
                continue

            raise ErroSemantico(num, 'Estrutura da linha não reconhecida ou suporte incompleto', _construir_contexto_expressao(linha_ast))

        except ErroSemantico as e:
            erros.append({'linha': num, 'erro': str(e), 'contexto': f"Linha {num}"})
            arvore_anotada['linhas'].append(dict(linha_ast))

    sucesso = len(erros) == 0
    return {'sucesso': sucesso, 'erros': erros, 'arvore_anotada': arvore_anotada, 'tabela_simbolos': tabela}
