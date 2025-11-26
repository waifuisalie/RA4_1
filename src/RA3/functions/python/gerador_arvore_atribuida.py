#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1


import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from src.RA3.functions.python.gramatica_atributos import obter_regra
from src.RA3.functions.python import tipos

# Caminhos de saída (relativos à raiz do projeto)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
OUT_ARVORE_ATRIBUIDA_JSON = OUTPUTS_DIR / "RA3" / "arvore_atribuida.json"
ROOT_ARVORE_ATRIBUIDA_JSON = OUTPUTS_DIR /"RA3" / "arvore_atribuida.json"
OUT_RELATORIOS_DIR = OUTPUTS_DIR / "RA3" / "relatorios"
ROOT_RELATORIOS_DIR = PROJECT_ROOT / "relatorios"

def gerarArvoreAtribuida(arvoreAnotada: Dict[str, Any], tabela_simbolos=None) -> Dict[str, Any]:
    """
    Constrói a árvore sintática abstrata atribuída final a partir da árvore anotada.

    Args:
        arvoreAnotada: Árvore sintática anotada pela análise semântica
        tabela_simbolos: Tabela de símbolos para consultar tipos de variáveis

    Returns:
        Árvore sintática abstrata atribuída final
    """
    if not arvoreAnotada or 'linhas' not in arvoreAnotada:
        return {'arvore_atribuida': []}

    arvore_atribuida = []

    for linha in arvoreAnotada['linhas']:
        numero_linha = linha.get('numero_linha', 0)
        tipo = linha.get('tipo')

        # Construir a estrutura completa da árvore atribuída para esta linha
        raiz_linha = _construir_no_atribuido(linha, numero_linha, tabela_simbolos)
        arvore_atribuida.append(raiz_linha)

    return {'arvore_atribuida': arvore_atribuida}


def _construir_no_atribuido(no: Dict[str, Any], numero_linha: int, tabela_simbolos=None) -> Dict[str, Any]:
    """
    Constrói recursivamente um nó da árvore atribuída.

    Args:
        no: Nó da árvore anotada
        numero_linha: Número da linha para referência
        tabela_simbolos: Tabela de símbolos para consultar tipos de variáveis

    Returns:
        Nó da árvore atribuída com tipo, filhos, etc.
    """
    # Determinar tipo do vértice baseado na estrutura
    tipo_vertice = "LINHA"  # Padrão para nó raiz da linha

    # Se tem operador, é um nó operador
    operador = no.get('operador')
    if operador:
        if operador in ['+', '-', '*', '/', '%', '^', '|']:
            tipo_vertice = "ARITH_OP"
        elif operador in ['>', '<', '>=', '<=', '==', '!=']:
            tipo_vertice = "COMP_OP"
        elif operador in ['&&', '||', '!']:
            tipo_vertice = "LOGIC_OP"
        elif operador in ['IFELSE', 'WHILE', 'FOR']:
            tipo_vertice = "CONTROL_OP"
        elif operador == 'RES':
            tipo_vertice = "RES"
        else:
            tipo_vertice = "OPERADOR_FINAL"

    # Tipo inferido (do resultado da análise semântica)
    tipo_inferido = no.get('tipo')

    # Filhos
    filhos = []

    # Se tem filhos diretos (estrutura de árvore)
    if 'filhos' in no and no['filhos']:
        for filho in no['filhos']:
            filhos.append(_construir_no_atribuido(filho, numero_linha, tabela_simbolos))
    # Se tem elementos (estrutura convertida)
    elif 'elementos' in no:
        for elemento in no['elementos']:
            # Cada elemento pode ser um operando simples ou uma subexpressão LINHA
            if isinstance(elemento, dict):
                if elemento.get('subtipo') == 'LINHA':
                    # É uma subexpressão - criar um nó recursivamente com sua estrutura
                    no_subexpressao = {
                        'numero_linha': numero_linha,
                        'elementos': elemento.get('elementos', []),
                        'operador': elemento.get('operador')
                    }
                    filhos.append(_construir_no_atribuido(no_subexpressao, numero_linha, tabela_simbolos))
                else:
                    # Operando simples
                    no_elemento = {
                        'numero_linha': numero_linha,
                        'tipo': elemento.get('tipo'),
                        'subtipo': elemento.get('subtipo'),
                        'valor': elemento.get('valor')
                    }
                    filhos.append(_construir_no_atribuido(no_elemento, numero_linha, tabela_simbolos))
            else:
                # Elemento não-dicionário (fallback)
                filhos.append(_construir_no_atribuido({'valor': str(elemento)}, numero_linha, tabela_simbolos))

    # Valor se for terminal
    valor = no.get('valor')

    # Inferir tipo para literais e variáveis (nós LINHA com valor mas sem operador)
    subtipo = no.get('subtipo')
    if tipo_vertice == 'LINHA' and valor is not None and not operador and tipo_inferido is None:
        # Este é um literal - inferir tipo do subtipo
        if subtipo in ['numero_inteiro', 'numero_inteiro_res']:
            tipo_inferido = tipos.TYPE_INT
        elif subtipo in ['numero_real', 'numero_real_res']:
            tipo_inferido = tipos.TYPE_REAL
        # Consultar tabela de símbolos para variáveis
        elif subtipo == 'variavel' and tabela_simbolos:
            try:
                if tabela_simbolos.existe(valor):
                    tipo_inferido = tabela_simbolos.obter_tipo(valor)
            except Exception:
                pass  # Manter tipo_inferido como None se houver erro

    # Inferir tipo para operações baseado nos filhos (quando tipo_inferido não foi preenchido)
    if tipo_inferido is None and filhos and operador:
        tipos_filhos = [f.get('tipo_inferido') for f in filhos if f.get('tipo_inferido')]
        if tipos_filhos:
            if tipo_vertice == "ARITH_OP":
                # Operações aritméticas: real se algum operando for real, senão int
                if tipos.TYPE_REAL in tipos_filhos:
                    tipo_inferido = tipos.TYPE_REAL
                elif all(t == tipos.TYPE_INT for t in tipos_filhos):
                    tipo_inferido = tipos.TYPE_INT
            elif tipo_vertice in ["COMP_OP", "LOGIC_OP"]:
                # Operações de comparação e lógicas sempre retornam boolean
                tipo_inferido = tipos.TYPE_BOOLEAN

    # Construir o nó atribuído
    no_atribuido = {
        'tipo_vertice': tipo_vertice,
        'tipo_inferido': tipo_inferido,
        'numero_linha': numero_linha,
        'filhos': filhos
    }

    if operador:
        no_atribuido['operador'] = operador

    if valor is not None:
        no_atribuido['valor'] = valor

    # Adicionar subtipo se existir (para operandos)
    if subtipo:
        no_atribuido['subtipo'] = subtipo

    return no_atribuido


def salvarArvoreAtribuida(arvoreAtribuida: Dict[str, Any]) -> None:
    """
    Salva a árvore atribuída em formato JSON.

    Args:
        arvoreAtribuida: Árvore sintática abstrata atribuída
    """
    OUT_ARVORE_ATRIBUIDA_JSON.parent.mkdir(parents=True, exist_ok=True)

    with open(OUT_ARVORE_ATRIBUIDA_JSON, 'w', encoding='utf-8') as f:
        json.dump(arvoreAtribuida, f, indent=2, ensure_ascii=False)

    # Também salvar uma cópia no diretório raiz
    with open(ROOT_ARVORE_ATRIBUIDA_JSON, 'w', encoding='utf-8') as f:
        json.dump(arvoreAtribuida, f, indent=2, ensure_ascii=False)


def gerarRelatoriosMarkdown(arvoreAtribuida: Dict[str, Any], errosSemanticos: Optional[List[str]],
                          tabelaSimbolos, caminhoSaida: Path) -> None:
    """
    Gera os relatórios em markdown: árvore atribuída, julgamento de tipos e erros semânticos.

    Args:
        arvoreAtribuida: Árvore sintática abstrata atribuída
        errosSemanticos: Lista de erros semânticos (ou None se não há erros)
        tabelaSimbolos: Tabela de símbolos da análise semântica
        caminhoSaida: Diretório onde salvar os relatórios
    """
    # Gerar relatórios no diretório especificado
    _gerar_relatorios_em_diretorio(arvoreAtribuida, errosSemanticos, tabelaSimbolos, caminhoSaida)

    # Também gerar na pasta raiz do projeto
    _gerar_relatorios_em_diretorio(arvoreAtribuida, errosSemanticos, tabelaSimbolos, ROOT_RELATORIOS_DIR)


def _gerar_relatorios_em_diretorio(arvoreAtribuida: Dict[str, Any], errosSemanticos: Optional[List[str]],
                                 tabelaSimbolos, caminhoSaida: Path) -> None:
    """
    Gera os relatórios em um diretório específico.
    """
    caminhoSaida.mkdir(parents=True, exist_ok=True)

    # 1. Relatório da Árvore Atribuída
    _gerar_relatorio_arvore_atribuida(arvoreAtribuida, caminhoSaida / "arvore_atribuida.md")

    # 2. Relatório de Julgamento de Tipos
    _gerar_relatorio_julgamento_tipos(arvoreAtribuida, caminhoSaida / "julgamento_tipos.md", tabelaSimbolos)

    # 3. Relatório de Erros Semânticos
    _gerar_relatorio_erros_sematicos(errosSemanticos, caminhoSaida / "erros_sematicos.md")

    # 4. Relatório da Tabela de Símbolos
    _gerar_relatorio_tabela_simbolos(tabelaSimbolos, caminhoSaida / "tabela_simbolos.md")


def _gerar_relatorio_arvore_atribuida(arvoreAtribuida: Dict[str, Any], caminhoArquivo: Path) -> None:
    """Gera relatório da árvore atribuída em markdown."""
    with open(caminhoArquivo, 'w', encoding='utf-8') as f:
        f.write("# Árvore Sintática Abstrata Atribuída\n\n")
        f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        arvore = arvoreAtribuida.get('arvore_atribuida', [])

        f.write("## Resumo\n\n")
        f.write(f"- **Total de linhas:** {len(arvore)}\n")
        f.write(f"- **Linhas com tipo definido:** {sum(1 for entrada in arvore if entrada.get('tipo_inferido') is not None)}\n")
        f.write(f"- **Linhas sem tipo definido:** {sum(1 for entrada in arvore if entrada.get('tipo_inferido') is None)}\n\n")

        # Detalhes da árvore por linha
        f.write("## Detalhes da Árvore Atribuída por Linha\n\n")

        for i, raiz_linha in enumerate(arvore, 1):
            f.write(f"### Linha {raiz_linha.get('numero_linha', i)}\n\n")
            f.write(f"**Tipo Resultado:** `{raiz_linha.get('tipo_inferido', 'N/A')}`\n\n")
            f.write("**Estrutura da Árvore:**\n\n")
            f.write("```\n")
            f.write(_formatar_arvore(raiz_linha, 0))
            f.write("```\n\n")

        f.write("\n---\n*Relatório gerado automaticamente pelo Compilador RA3_1*")


def _formatar_arvore(no: Dict[str, Any], nivel: int) -> str:
    """Formata um nó da árvore para exibição textual."""
    indent = "  " * nivel
    tipo_vertice = no.get('tipo_vertice', 'UNKNOWN')
    tipo_inferido = no.get('tipo_inferido')
    operador = no.get('operador', '')
    valor = no.get('valor', '')
    subtipo = no.get('subtipo', '')

    linha = f"{indent}{tipo_vertice}"
    if operador:
        linha += f" ({operador})"
    if tipo_inferido:
        linha += f" : {tipo_inferido}"
    if valor:
        linha += f" [{valor}]"
    if subtipo:
        linha += f" {{{subtipo}}}"

    linha += "\n"

    for filho in no.get('filhos', []):
        linha += _formatar_arvore(filho, nivel + 1)

    return linha


# ============================================================================
# FUNÇÕES AUXILIARES PARA JULGAMENTO DE TIPOS
# ============================================================================

def _reconstruir_expressao(no: Dict[str, Any]) -> str:
    """
    Reconstrói a expressão original em notação RPN a partir do nó da árvore.

    Args:
        no: Nó da árvore atribuída

    Returns:
        String com a expressão reconstruída (ex: "(5 3 +)")
    """
    try:
        tipo_vertice = no.get('tipo_vertice', '')
        filhos = no.get('filhos', [])
        valor = no.get('valor')
        operador = no.get('operador')

        # Se é nó LINHA raiz, processar o primeiro filho
        if tipo_vertice == 'LINHA' and not valor and filhos:
            primeiro_filho = filhos[0]
            filho_tipo = primeiro_filho.get('tipo_vertice', '')

            # Se o primeiro filho é um operador, reconstruir com operador
            if filho_tipo in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP', 'CONTROL_OP']:
                filho_operador = primeiro_filho.get('operador')
                filho_filhos = primeiro_filho.get('filhos', [])

                partes = []
                for operando in filho_filhos:
                    partes.append(_reconstruir_expressao(operando))

                partes.append(filho_operador)
                return f"({' '.join(partes)})"

            # Se o primeiro filho é LINHA, pode ser armazenamento ou epsilon
            elif filho_tipo == 'LINHA':
                filho_filhos = primeiro_filho.get('filhos', [])

                # Se a LINHA tem valor direto, usar esse valor
                filho_valor = primeiro_filho.get('valor')
                if filho_valor is not None:
                    return f"({filho_valor})"

                # Caso contrário, reconstruir dos filhos
                partes = []
                for sub in filho_filhos:
                    sub_expr = _reconstruir_expressao(sub)
                    if sub_expr:
                        partes.append(sub_expr)

                # Se conseguiu alguma parte, retornar
                if partes:
                    return f"({' '.join(partes)})"

                # Se não tem partes mas tem filhos, buscar valor nos filhos
                if filho_filhos:
                    for sub in filho_filhos:
                        sub_valor = sub.get('valor')
                        if sub_valor is not None:
                            return f"({sub_valor})"

                return "()"

        # Nó com operador direto (operador como nó)
        if operador and tipo_vertice in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP', 'CONTROL_OP']:
            partes = []
            for filho in filhos:
                partes.append(_reconstruir_expressao(filho))
            partes.append(operador)
            return f"({' '.join(partes)})"

        # Nó terminal com valor
        if valor is not None:
            return str(valor)

        # Nó LINHA com filhos mas sem operador - processar filhos
        if filhos:
            partes = []
            for filho in filhos:
                sub = _reconstruir_expressao(filho)
                if sub:
                    partes.append(sub)
            if partes:
                if len(partes) == 1:
                    return partes[0]
                return ' '.join(partes)

        return ""
    except Exception:
        return "(?)"


def _extrair_operandos_e_tipos(no: Dict[str, Any], tabelaSimbolos=None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Extrai os operandos com seus tipos e o operador de um nó.

    Args:
        no: Nó da árvore atribuída (raiz LINHA)

    Returns:
        Tupla (lista de operandos, operador)
        Cada operando é um dict com 'valor', 'tipo', 'eh_subexpressao'
    """
    operandos = []
    operador = None

    tipo_vertice = no.get('tipo_vertice', '')
    filhos = no.get('filhos', [])

    # Se é nó LINHA raiz, processar o primeiro filho
    if tipo_vertice == 'LINHA' and filhos:
        primeiro_filho = filhos[0]
        filho_tipo = primeiro_filho.get('tipo_vertice', '')

        # Se o primeiro filho é um operador
        if filho_tipo in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP', 'CONTROL_OP']:
            operador = primeiro_filho.get('operador')
            filho_filhos = primeiro_filho.get('filhos', [])

            # Extrair cada operando
            for operando_node in filho_filhos:
                tipo_vertice_operando = operando_node.get('tipo_vertice', '')
                valor = operando_node.get('valor')
                tipo = operando_node.get('tipo_inferido')
                subtipo = operando_node.get('subtipo', '')
                operando_filhos = operando_node.get('filhos', [])

                # Verificar se o operando É UMA LINHA (pode ter tipo inferido diretamente)
                if tipo_vertice_operando == 'LINHA':
                    # Para LINHA, primeiro tentar pegar o tipo inferido do nó
                    tipo_linha = operando_node.get('tipo_inferido')
                    if not tipo_linha:
                        # Se não tem tipo_inferido, buscar recursivamente nos filhos
                        def _buscar_tipo_recursivo(node):
                            """Busca recursivamente o tipo em uma estrutura LINHA aninhada"""
                            ti = node.get('tipo_inferido')
                            if ti:
                                return ti

                            # Verificar se o próprio nó tem valor e subtipo
                            nv = node.get('valor')
                            nst = node.get('subtipo', '')
                            if nv is not None and nst:
                                if nst in ['numero_inteiro', 'numero_inteiro_res']:
                                    return tipos.TYPE_INT
                                elif nst in ['numero_real', 'numero_real_res']:
                                    return tipos.TYPE_REAL
                                elif nst == 'variavel' and tabelaSimbolos:
                                    try:
                                        if tabelaSimbolos.existe(nv):
                                            return tabelaSimbolos.obter_tipo(nv)
                                    except:
                                        pass

                            tv = node.get('tipo_vertice', '')
                            if tv in ['COMP_OP', 'LOGIC_OP']:
                                return tipos.TYPE_BOOLEAN
                            elif tv == 'ARITH_OP':
                                # Inferir tipo aritmético
                                filhos_n = node.get('filhos', [])
                                if len(filhos_n) >= 2:
                                    tipos_n = []
                                    for fn in filhos_n:
                                        tn = _buscar_tipo_recursivo(fn)
                                        if tn is None:
                                            # Tentar inferir de subtipo
                                            stn = fn.get('subtipo', '')
                                            if stn in ['numero_inteiro', 'numero_inteiro_res']:
                                                tn = tipos.TYPE_INT
                                            elif stn in ['numero_real', 'numero_real_res']:
                                                tn = tipos.TYPE_REAL
                                            elif stn == 'variavel' and tabelaSimbolos:
                                                vn = fn.get('valor')
                                                if vn and tabelaSimbolos.existe(vn):
                                                    try:
                                                        tn = tabelaSimbolos.obter_tipo(vn)
                                                    except:
                                                        pass
                                        tipos_n.append(tn)
                                    if len(tipos_n) >= 2 and tipos_n[0] and tipos_n[1]:
                                        try:
                                            return tipos.tipo_resultado_aritmetica(tipos_n[0], tipos_n[1], node.get('operador'))
                                        except:
                                            pass
                            # Buscar nos filhos
                            for child in node.get('filhos', []):
                                tr = _buscar_tipo_recursivo(child)
                                if tr:
                                    return tr
                            return None

                        tipo_linha = _buscar_tipo_recursivo(operando_node)

                    if tipo_linha:
                        tipo = tipo_linha
                        eh_subexpr = True
                        expr_texto = _reconstruir_expressao(operando_node)
                        operandos.append({
                            'valor': expr_texto,
                            'tipo': tipo,
                            'eh_subexpressao': True,
                            'filhos': [operando_node]
                        })
                        continue

                # Verificar se o operando É UM OPERADOR (comum em operadores lógicos)
                if tipo_vertice_operando in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP', 'CONTROL_OP']:
                    # O operando é diretamente um nó operador (subexpressão)
                    eh_subexpr = True
                    expr_texto = _reconstruir_expressao(operando_node)
                    # O tipo é o tipo_inferido do próprio nó operador
                    tipo = operando_node.get('tipo_inferido')

                    # Se não tem tipo_inferido, inferir pela categoria do operador
                    if tipo is None:
                        if tipo_vertice_operando in ['COMP_OP', 'LOGIC_OP']:
                            tipo = tipos.TYPE_BOOLEAN
                        elif tipo_vertice_operando == 'ARITH_OP':
                            # Para aritmético, inferir pelos operandos
                            op_operador = operando_node.get('operador')
                            op_filhos = operando_node.get('filhos', [])

                            if op_filhos and len(op_filhos) >= 2:
                                # Extrair tipos dos operandos
                                tipos_ops = []
                                for op_f in op_filhos:
                                    tipo_op = op_f.get('tipo_inferido')
                                    subtipo_op = op_f.get('subtipo', '')
                                    valor_op = op_f.get('valor')
                                    tipo_vertice_op_f = op_f.get('tipo_vertice', '')

                                    # Se o operando é outro operador (nested), inferir seu tipo recursivamente
                                    if tipo_op is None and tipo_vertice_op_f in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP']:
                                        if tipo_vertice_op_f in ['COMP_OP', 'LOGIC_OP']:
                                            # Comparação e lógica sempre retornam boolean
                                            tipo_op = tipos.TYPE_BOOLEAN
                                        elif tipo_vertice_op_f == 'ARITH_OP':
                                            # Recursivamente inferir tipo aritmético
                                            nested_op = op_f.get('operador')
                                            nested_filhos = op_f.get('filhos', [])
                                            if len(nested_filhos) >= 2:
                                                nested_tipos = []
                                                for nf in nested_filhos:
                                                    nt = nf.get('tipo_inferido')
                                                    nst = nf.get('subtipo', '')
                                                    nv = nf.get('valor')
                                                    if nt is None and nst:
                                                        if nst in ['numero_inteiro', 'numero_inteiro_res']:
                                                            nt = tipos.TYPE_INT
                                                        elif nst in ['numero_real', 'numero_real_res']:
                                                            nt = tipos.TYPE_REAL
                                                        elif nst == 'variavel' and tabelaSimbolos and nv:
                                                            try:
                                                                if tabelaSimbolos.existe(nv):
                                                                    nt = tabelaSimbolos.obter_tipo(nv)
                                                            except:
                                                                pass
                                                    nested_tipos.append(nt)
                                                if len(nested_tipos) >= 2 and nested_tipos[0] and nested_tipos[1]:
                                                    try:
                                                        tipo_op = tipos.tipo_resultado_aritmetica(nested_tipos[0], nested_tipos[1], nested_op)
                                                    except:
                                                        pass

                                    if tipo_op is None and subtipo_op:
                                        if subtipo_op in ['numero_inteiro', 'numero_inteiro_res']:
                                            tipo_op = tipos.TYPE_INT
                                        elif subtipo_op in ['numero_real', 'numero_real_res']:
                                            tipo_op = tipos.TYPE_REAL
                                        elif subtipo_op == 'variavel' and tabelaSimbolos and valor_op:
                                            try:
                                                if tabelaSimbolos.existe(valor_op):
                                                    tipo_op = tabelaSimbolos.obter_tipo(valor_op)
                                            except:
                                                pass
                                    tipos_ops.append(tipo_op)

                                # Aplicar regras de tipo para o operador
                                if len(tipos_ops) >= 2 and tipos_ops[0] and tipos_ops[1]:
                                    try:
                                        tipo = tipos.tipo_resultado_aritmetica(tipos_ops[0], tipos_ops[1], op_operador)
                                    except:
                                        pass

                    operandos.append({
                        'valor': expr_texto,
                        'tipo': tipo,
                        'eh_subexpressao': True,
                        'filhos': [operando_node]  # Envolver o nó operador
                    })
                    continue

                # Inferir tipo a partir do subtipo se tipo_inferido não estiver disponível
                if tipo is None and subtipo:
                    if subtipo in ['numero_inteiro', 'numero_inteiro_res']:
                        tipo = tipos.TYPE_INT
                    elif subtipo in ['numero_real', 'numero_real_res']:
                        tipo = tipos.TYPE_REAL
                    elif subtipo == 'variavel' and tabelaSimbolos:
                        # Consultar tabela de símbolos para variáveis
                        try:
                            if tabelaSimbolos.existe(valor):
                                tipo = tabelaSimbolos.obter_tipo(valor)
                        except:
                            pass

                # Verificar se é uma subexpressão (tem filhos com operador)
                eh_subexpr = False
                no_operador_filho = None
                if operando_filhos:
                    for sub in operando_filhos:
                        tipo_vertice_sub = sub.get('tipo_vertice', '')
                        if tipo_vertice_sub in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP', 'CONTROL_OP']:
                            eh_subexpr = True
                            no_operador_filho = sub
                            # Se é subexpressão com operador, pegar o tipo do resultado do operador
                            if tipo is None:
                                tipo = sub.get('tipo_inferido')
                                # Se ainda None, inferir pela categoria do operador
                                if tipo is None:
                                    if tipo_vertice_sub in ['COMP_OP', 'LOGIC_OP']:
                                        tipo = tipos.TYPE_BOOLEAN
                                    elif tipo_vertice_sub == 'ARITH_OP':
                                        # Inferir tipo aritmético pelos operandos
                                        sub_operador = sub.get('operador')
                                        sub_filhos = sub.get('filhos', [])
                                        if len(sub_filhos) >= 2:
                                            sub_tipos = []
                                            for sf in sub_filhos:
                                                st = sf.get('tipo_inferido')
                                                sst = sf.get('subtipo', '')
                                                sv = sf.get('valor')
                                                stv = sf.get('tipo_vertice', '')

                                                # Verificar se é um operador aninhado
                                                if st is None and stv in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP']:
                                                    if stv in ['COMP_OP', 'LOGIC_OP']:
                                                        st = tipos.TYPE_BOOLEAN
                                                    elif stv == 'ARITH_OP':
                                                        # Inferir recursivamente para operador aninhado
                                                        nested_op = sf.get('operador')
                                                        nested_filhos = sf.get('filhos', [])
                                                        if len(nested_filhos) >= 2:
                                                            nested_tipos = []
                                                            for nf in nested_filhos:
                                                                nt = nf.get('tipo_inferido')
                                                                nst = nf.get('subtipo', '')
                                                                nv = nf.get('valor')
                                                                if nt is None and nst:
                                                                    if nst in ['numero_inteiro', 'numero_inteiro_res']:
                                                                        nt = tipos.TYPE_INT
                                                                    elif nst in ['numero_real', 'numero_real_res']:
                                                                        nt = tipos.TYPE_REAL
                                                                    elif nst == 'variavel' and tabelaSimbolos and nv:
                                                                        try:
                                                                            if tabelaSimbolos.existe(nv):
                                                                                nt = tabelaSimbolos.obter_tipo(nv)
                                                                        except:
                                                                            pass
                                                                nested_tipos.append(nt)
                                                            if len(nested_tipos) >= 2 and nested_tipos[0] and nested_tipos[1]:
                                                                try:
                                                                    st = tipos.tipo_resultado_aritmetica(nested_tipos[0], nested_tipos[1], nested_op)
                                                                except:
                                                                    pass

                                                if st is None and sst:
                                                    if sst in ['numero_inteiro', 'numero_inteiro_res']:
                                                        st = tipos.TYPE_INT
                                                    elif sst in ['numero_real', 'numero_real_res']:
                                                        st = tipos.TYPE_REAL
                                                    elif sst == 'variavel' and tabelaSimbolos and sv:
                                                        try:
                                                            if tabelaSimbolos.existe(sv):
                                                                st = tabelaSimbolos.obter_tipo(sv)
                                                        except:
                                                            pass
                                                sub_tipos.append(st)
                                            if len(sub_tipos) >= 2 and sub_tipos[0] and sub_tipos[1]:
                                                try:
                                                    tipo = tipos.tipo_resultado_aritmetica(sub_tipos[0], sub_tipos[1], sub_operador)
                                                except:
                                                    pass
                                # Se ainda None após tudo, tentar buscar no nó raiz do operando
                                if tipo is None:
                                    tipo = operando_node.get('tipo_inferido')
                            break

                if valor is not None and not eh_subexpr:
                    # Operando simples (literal ou variável)
                    operandos.append({
                        'valor': valor,
                        'tipo': tipo,
                        'eh_subexpressao': False,
                        'subtipo': subtipo
                    })
                else:
                    # Subexpressão
                    expr_texto = _reconstruir_expressao(operando_node)

                    # Corrigir expressões epsilon vazias
                    if expr_texto == '()' or expr_texto == '':
                        # Buscar valor real dentro do epsilon
                        for filho in operando_filhos:
                            val = filho.get('valor')
                            if val is not None:
                                expr_texto = f"({val})"
                                if tipo is None and filho.get('subtipo'):
                                    st = filho.get('subtipo')
                                    if st in ['numero_inteiro', 'numero_inteiro_res']:
                                        tipo = tipos.TYPE_INT
                                    elif st in ['numero_real', 'numero_real_res']:
                                        tipo = tipos.TYPE_REAL
                                break

                    operandos.append({
                        'valor': expr_texto,
                        'tipo': tipo,
                        'eh_subexpressao': True,
                        'filhos': operando_filhos
                    })

        # Se o primeiro filho é LINHA (armazenamento ou epsilon)
        elif filho_tipo == 'LINHA':
            filho_filhos = primeiro_filho.get('filhos', [])
            for sub_node in filho_filhos:
                tipo_vertice_sub = sub_node.get('tipo_vertice', '')
                valor = sub_node.get('valor')
                tipo = sub_node.get('tipo_inferido')
                subtipo = sub_node.get('subtipo', '')
                sub_filhos = sub_node.get('filhos', [])

                # Verificar se É um nó operador diretamente
                if tipo_vertice_sub in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP', 'CONTROL_OP']:
                    expr_texto = _reconstruir_expressao(sub_node)
                    tipo = sub_node.get('tipo_inferido')

                    # Inferir tipo pela categoria se necessário
                    if tipo is None:
                        if tipo_vertice_sub in ['COMP_OP', 'LOGIC_OP']:
                            tipo = tipos.TYPE_BOOLEAN
                        elif tipo_vertice_sub == 'ARITH_OP':
                            # Inferir tipo aritmético pelos operandos
                            op_operador = sub_node.get('operador')
                            op_filhos = sub_node.get('filhos', [])

                            if op_filhos and len(op_filhos) >= 2:
                                tipos_ops = []
                                for op_f in op_filhos:
                                    tipo_op = op_f.get('tipo_inferido')
                                    subtipo_op = op_f.get('subtipo', '')
                                    valor_op = op_f.get('valor')
                                    tipo_vertice_op_f = op_f.get('tipo_vertice', '')

                                    # Se o operando é outro operador (nested), inferir seu tipo recursivamente
                                    if tipo_op is None and tipo_vertice_op_f in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP']:
                                        if tipo_vertice_op_f in ['COMP_OP', 'LOGIC_OP']:
                                            # Comparação e lógica sempre retornam boolean
                                            tipo_op = tipos.TYPE_BOOLEAN
                                        elif tipo_vertice_op_f == 'ARITH_OP':
                                            # Recursivamente inferir tipo aritmético
                                            nested_op = op_f.get('operador')
                                            nested_filhos = op_f.get('filhos', [])
                                            if len(nested_filhos) >= 2:
                                                nested_tipos = []
                                                for nf in nested_filhos:
                                                    nt = nf.get('tipo_inferido')
                                                    nst = nf.get('subtipo', '')
                                                    nv = nf.get('valor')
                                                    if nt is None and nst:
                                                        if nst in ['numero_inteiro', 'numero_inteiro_res']:
                                                            nt = tipos.TYPE_INT
                                                        elif nst in ['numero_real', 'numero_real_res']:
                                                            nt = tipos.TYPE_REAL
                                                        elif nst == 'variavel' and tabelaSimbolos and nv:
                                                            try:
                                                                if tabelaSimbolos.existe(nv):
                                                                    nt = tabelaSimbolos.obter_tipo(nv)
                                                            except:
                                                                pass
                                                    nested_tipos.append(nt)
                                                if len(nested_tipos) >= 2 and nested_tipos[0] and nested_tipos[1]:
                                                    try:
                                                        tipo_op = tipos.tipo_resultado_aritmetica(nested_tipos[0], nested_tipos[1], nested_op)
                                                    except:
                                                        pass

                                    if tipo_op is None and subtipo_op:
                                        if subtipo_op in ['numero_inteiro', 'numero_inteiro_res']:
                                            tipo_op = tipos.TYPE_INT
                                        elif subtipo_op in ['numero_real', 'numero_real_res']:
                                            tipo_op = tipos.TYPE_REAL
                                        elif subtipo_op == 'variavel' and tabelaSimbolos and valor_op:
                                            try:
                                                if tabelaSimbolos.existe(valor_op):
                                                    tipo_op = tabelaSimbolos.obter_tipo(valor_op)
                                            except:
                                                pass
                                    tipos_ops.append(tipo_op)

                                if len(tipos_ops) >= 2 and tipos_ops[0] and tipos_ops[1]:
                                    try:
                                        tipo = tipos.tipo_resultado_aritmetica(tipos_ops[0], tipos_ops[1], op_operador)
                                    except:
                                        pass

                    operandos.append({
                        'valor': expr_texto,
                        'tipo': tipo,
                        'eh_subexpressao': True,
                        'filhos': [sub_node]
                    })
                    continue

                # Inferir tipo a partir do subtipo se tipo_inferido não estiver disponível
                if tipo is None and subtipo:
                    if subtipo in ['numero_inteiro', 'numero_inteiro_res']:
                        tipo = tipos.TYPE_INT
                    elif subtipo in ['numero_real', 'numero_real_res']:
                        tipo = tipos.TYPE_REAL
                    elif subtipo == 'variavel' and tabelaSimbolos:
                        # Consultar tabela de símbolos para variáveis
                        try:
                            if tabelaSimbolos.existe(valor):
                                tipo = tabelaSimbolos.obter_tipo(valor)
                        except:
                            pass

                # Verificar se é subexpressão
                eh_subexpr = False
                if sub_filhos:
                    for f in sub_filhos:
                        if f.get('tipo_vertice') in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP', 'CONTROL_OP']:
                            eh_subexpr = True
                            if tipo is None:
                                tipo = f.get('tipo_inferido')
                            break

                if valor is not None and not eh_subexpr:
                    operandos.append({
                        'valor': valor,
                        'tipo': tipo,
                        'eh_subexpressao': False,
                        'subtipo': subtipo
                    })
                else:
                    expr_texto = _reconstruir_expressao(sub_node)
                    operandos.append({
                        'valor': expr_texto,
                        'tipo': tipo,
                        'eh_subexpressao': True,
                        'filhos': sub_filhos
                    })

    return operandos, operador


def _detectar_promocao_tipo(operandos: List[Dict[str, Any]], tipo_resultado: str) -> Optional[str]:
    """
    Detecta se houve promoção de tipo na expressão.

    Args:
        operandos: Lista de operandos com tipos
        tipo_resultado: Tipo do resultado

    Returns:
        Mensagem explicando a promoção ou None
    """
    if not operandos or not tipo_resultado:
        return None

    # Verificar se há operandos int e resultado real
    tipos_operandos = [op.get('tipo') for op in operandos if op.get('tipo')]

    if tipo_resultado == tipos.TYPE_REAL and tipos.TYPE_INT in tipos_operandos:
        # Houve promoção de int para real
        if tipos.TYPE_REAL in tipos_operandos:
            return "Tipo promovido de `int` para `real` devido a operando `real`."
        else:
            return "Operação resulta em `real` por definição do operador."

    return None


def _formatar_regra_semantica(operador: str, tipos_operandos: List[str], tipo_resultado: str) -> str:
    """
    Formata a regra semântica com notação formal Γ ⊢.

    Args:
        operador: Símbolo do operador
        tipos_operandos: Lista de tipos dos operandos
        tipo_resultado: Tipo do resultado

    Returns:
        String formatada com a regra semântica
    """
    if not operador or not tipo_resultado:
        return "N/A"

    # Buscar a regra na gramática
    regra = obter_regra(operador)

    if regra and regra.get('regra_formal'):
        # Usar a regra formal definida na gramática
        regra_texto = regra['regra_formal'].strip()

        # Substituir placeholders genéricos pelos tipos reais
        if len(tipos_operandos) >= 2:
            regra_texto = regra_texto.replace('T₁', tipos_operandos[0])
            regra_texto = regra_texto.replace('T₂', tipos_operandos[1])
            regra_texto = regra_texto.replace('T₁, T₂ ∈ {int, real}', f'{tipos_operandos[0]}, {tipos_operandos[1]}')
        elif len(tipos_operandos) == 1:
            regra_texto = regra_texto.replace('T', tipos_operandos[0])

        regra_texto = regra_texto.replace('promover_tipo(T₁, T₂)', tipo_resultado)

        return regra_texto

    # Regra genérica se não encontrada na gramática
    if len(tipos_operandos) >= 2:
        premissas = f"Γ ⊢ e₁ : {tipos_operandos[0]}    Γ ⊢ e₂ : {tipos_operandos[1]}"
        linha_sep = "─" * max(len(premissas), 40)
        conclusao = f"Γ ⊢ e₁ {operador} e₂ : {tipo_resultado}"
        return f"{premissas}\n{linha_sep}\n{conclusao.center(len(linha_sep))}"
    elif len(tipos_operandos) == 1:
        premissa = f"Γ ⊢ e : {tipos_operandos[0]}"
        linha_sep = "─" * max(len(premissa), 30)
        conclusao = f"Γ ⊢ ({operador} e) : {tipo_resultado}"
        return f"{premissa}\n{linha_sep}\n{conclusao.center(len(linha_sep))}"

    return "N/A"


def _analisar_subexpressao(operando: Dict[str, Any], nivel: int = 0, tabelaSimbolos=None) -> List[str]:
    """
    Analisa recursivamente uma subexpressão, gerando linhas de análise detalhada.

    Args:
        operando: Operando que contém uma subexpressão
        nivel: Nível de indentação
        tabelaSimbolos: Tabela de símbolos para consulta

    Returns:
        Lista de strings com a análise completa (operandos, operador, resultado)
    """
    linhas = []
    indent = "  " * nivel

    if not operando.get('eh_subexpressao'):
        return linhas

    filhos = operando.get('filhos', [])

    # Procurar nó operador
    no_operador = None
    operador_str = None
    tipo_resultado = None

    for filho in filhos:
        tipo_vertice = filho.get('tipo_vertice', '')
        if tipo_vertice in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP', 'CONTROL_OP']:
            no_operador = filho
            operador_str = filho.get('operador')
            tipo_resultado = filho.get('tipo_inferido')
            break

    if no_operador:
        # Extrair operandos do operador
        operandos_filhos = no_operador.get('filhos', [])

        for i, op_filho in enumerate(operandos_filhos, 1):
            valor = op_filho.get('valor')
            tipo = op_filho.get('tipo_inferido')
            subtipo = op_filho.get('subtipo', '')

            # Inferir tipo se não disponível
            if tipo is None and subtipo:
                if subtipo in ['numero_inteiro', 'numero_inteiro_res']:
                    tipo = tipos.TYPE_INT
                elif subtipo in ['numero_real', 'numero_real_res']:
                    tipo = tipos.TYPE_REAL
                elif subtipo == 'variavel' and tabelaSimbolos and valor:
                    try:
                        if tabelaSimbolos.existe(valor):
                            tipo = tabelaSimbolos.obter_tipo(valor)
                    except:
                        pass

            # Verificar se é outra subexpressão aninhada
            op_filhos = op_filho.get('filhos', [])
            eh_sub = any(f.get('tipo_vertice') in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP', 'CONTROL_OP'] for f in op_filhos)

            if valor is not None and not eh_sub:
                linhas.append(f"{indent}- `{valor}` : `{tipo if tipo else 'N/A'}`")
            elif eh_sub:
                sub_expr = _reconstruir_expressao(op_filho)
                # Buscar tipo da subexpressão
                for f in op_filhos:
                    if f.get('tipo_vertice') in ['ARITH_OP', 'COMP_OP', 'LOGIC_OP', 'CONTROL_OP']:
                        tipo = f.get('tipo_inferido')
                        break
                linhas.append(f"{indent}- `{sub_expr}` : `{tipo if tipo else 'N/A'}`")
                # Analisar recursivamente
                sub_linhas = _analisar_subexpressao(
                    {'eh_subexpressao': True, 'filhos': op_filhos, 'tipo': tipo},
                    nivel + 1,
                    tabelaSimbolos
                )
                linhas.extend(sub_linhas)

        # Adicionar operador e resultado
        if operador_str:
            linhas.append(f"{indent}- Operador: `{operador_str}`")
        if tipo_resultado:
            linhas.append(f"{indent}- Resultado: `{tipo_resultado}`")
    else:
        # Sem operador - pode ser epsilon ou literal simples
        for filho in filhos:
            valor = filho.get('valor')
            tipo = filho.get('tipo_inferido')
            subtipo = filho.get('subtipo', '')

            if tipo is None and subtipo:
                if subtipo in ['numero_inteiro', 'numero_inteiro_res']:
                    tipo = tipos.TYPE_INT
                elif subtipo in ['numero_real', 'numero_real_res']:
                    tipo = tipos.TYPE_REAL

            if valor is not None:
                linhas.append(f"{indent}- `{valor}` : `{tipo if tipo else 'N/A'}`")

    return linhas


def _gerar_relatorio_julgamento_tipos(arvoreAtribuida: Dict[str, Any], caminhoArquivo: Path, tabelaSimbolos=None) -> None:
    """
    Gera relatório detalhado de julgamento de tipos em markdown.
    Conforme especificado no issue #7 da rubrica.

    Args:
        arvoreAtribuida: Árvore sintática abstrata atribuída
        caminhoArquivo: Caminho do arquivo de saída
        tabelaSimbolos: Tabela de símbolos para consulta de tipos de variáveis
    """
    with open(caminhoArquivo, 'w', encoding='utf-8') as f:
        # Cabeçalho com informações
        f.write("# Julgamento de Tipos\n\n")
        f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        arvore = arvoreAtribuida.get('arvore_atribuida', [])
        f.write(f"**Total de expressões analisadas:** {len(arvore)}\n\n")
        f.write("---\n\n")

        # Contadores para estatísticas
        contador_promocoes = 0
        tipos_encontrados = {}  # tipo -> contagem

        # Análise detalhada linha por linha
        for raiz_linha in arvore:
            numero_linha = raiz_linha.get('numero_linha', '')
            tipo_resultado = raiz_linha.get('tipo_inferido')

            # Reconstruir expressão original
            expressao = _reconstruir_expressao(raiz_linha)

            # Título da seção
            f.write(f"## Linha {numero_linha}: `{expressao}`\n\n")

            # Extrair operandos e operador
            operandos, operador = _extrair_operandos_e_tipos(raiz_linha, tabelaSimbolos)

            # Seção: Análise de Tipos
            f.write("### Análise de Tipos:\n")

            if operandos:
                for i, op in enumerate(operandos, 1):
                    valor = op.get('valor', '?')
                    tipo = op.get('tipo', 'N/A')

                    if op.get('eh_subexpressao'):
                        tipo_op = op.get('tipo', 'N/A')
                        f.write(f"- **Operando {i}:** `{valor}` → tipo: `{tipo_op}`\n")
                        # Analisar subexpressão recursivamente
                        sub_linhas = _analisar_subexpressao(op, nivel=1, tabelaSimbolos=tabelaSimbolos)
                        for linha in sub_linhas:
                            f.write(f"  {linha}\n")
                    else:
                        f.write(f"- **Operando {i}:** `{valor}` → tipo: `{tipo}`\n")

            if operador:
                f.write(f"- **Operador:** `{operador}`\n")
            elif not operandos:
                # Pode ser um literal simples ou variável
                f.write(f"- Expressão de identidade (epsilon)\n")

            f.write("\n")

            # Seção: Regra Aplicada (somente se houver operador)
            if operador and tipo_resultado:
                f.write("### Regra Aplicada:\n\n")
                tipos_ops = [op.get('tipo', 'N/A') for op in operandos if op.get('tipo')]
                regra_formal = _formatar_regra_semantica(operador, tipos_ops, tipo_resultado)
                f.write("```\n")
                f.write(regra_formal)
                f.write("\n```\n\n")

            # Seção: Tipo Resultante
            f.write(f"### Tipo Resultante: `{tipo_resultado if tipo_resultado else 'N/A'}`\n\n")

            # Seção: Observações (se houver promoção ou algo especial)
            if operandos and tipo_resultado:
                promocao_msg = _detectar_promocao_tipo(operandos, tipo_resultado)
                if promocao_msg:
                    f.write("### Observação:\n")
                    f.write(f"{promocao_msg}\n\n")
                    contador_promocoes += 1

                # Observações sobre operadores especiais
                if operador == '|':
                    f.write("### Observação:\n")
                    f.write("Divisão real: resultado sempre `real`, independente dos tipos dos operandos.\n\n")
                elif operador == '/':
                    f.write("### Observação:\n")
                    f.write("Divisão inteira: ambos operandos devem ser `int`, resultado é `int`.\n\n")
                elif operador == '%':
                    f.write("### Observação:\n")
                    f.write("Resto da divisão: ambos operandos devem ser `int`, resultado é `int`.\n\n")
                elif operador == '^':
                    f.write("### Observação:\n")
                    f.write("Potenciação: expoente deve ser `int` positivo, resultado tem tipo da base.\n\n")
                elif operador in ['>', '<', '>=', '<=', '==', '!=']:
                    f.write("### Observação:\n")
                    f.write("Operador de comparação: resultado sempre `boolean`.\n\n")
                elif operador in ['&&', '||', '!']:
                    f.write("### Observação:\n")
                    f.write("Operador lógico: resultado sempre `boolean`. Modo permissivo aceita conversão via truthiness.\n\n")

            # Atualizar contadores
            if tipo_resultado:
                tipos_encontrados[tipo_resultado] = tipos_encontrados.get(tipo_resultado, 0) + 1

            f.write("---\n\n")

        # Seção: Resumo Final
        f.write("## Resumo de Tipos\n\n")

        f.write("### Estatísticas\n")
        total = len(arvore)
        com_tipo = sum(1 for r in arvore if r.get('tipo_inferido') is not None)
        sem_tipo = total - com_tipo
        f.write(f"- **Total de expressões:** {total}\n")
        f.write(f"- **Com tipo definido:** {com_tipo}\n")
        f.write(f"- **Sem tipo definido:** {sem_tipo}\n")
        f.write(f"- **Promoções de tipo:** {contador_promocoes}\n\n")

        if tipos_encontrados:
            f.write("### Distribuição de Tipos\n")
            for tipo, contagem in sorted(tipos_encontrados.items()):
                percentual = (contagem / total * 100) if total > 0 else 0
                f.write(f"- `{tipo}`: {contagem} expressões ({percentual:.1f}%)\n")
            f.write("\n")

            f.write("### Tipos Utilizados\n")
            for tipo in sorted(tipos_encontrados.keys()):
                f.write(f"- `{tipo}`\n")

        f.write("\n---\n")
        f.write("*Relatório gerado automaticamente pelo Compilador RA3_1*\n")


def _gerar_relatorio_erros_sematicos(erros: Optional[List[str]], caminhoArquivo: Path) -> None:
    """Gera relatório de erros semânticos em markdown."""
    with open(caminhoArquivo, 'w', encoding='utf-8') as f:
        f.write("# Relatório de Erros Semânticos\n\n")
        f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        if not erros:
            f.write("##  Nenhum Erro Encontrado\n\n")
            f.write("A análise semântica foi concluída com sucesso sem nenhum erro detectado.\n")
        else:
            f.write(f"##  Erros Encontrados ({len(erros)})\n\n")

            for i, erro in enumerate(erros, 1):
                f.write(f"### Erro {i}\n")
                # Se erro é um dicionário, extrair a mensagem
                if isinstance(erro, dict):
                    mensagem_erro = erro.get('erro', str(erro))
                else:
                    mensagem_erro = str(erro)
                f.write(f"```\n{mensagem_erro}\n```\n\n")

            f.write("## Resumo\n\n")
            f.write(f"- **Total de erros:** {len(erros)}\n")
            f.write("- **Status:** Análise semântica falhou\n")

        f.write("\n---\n*Relatório gerado automaticamente pelo Compilador RA3_1*")


def _gerar_relatorio_tabela_simbolos(tabela, caminhoArquivo: Path) -> None:
    """Gera relatório da tabela de símbolos em markdown."""
    with open(caminhoArquivo, 'w', encoding='utf-8') as f:
        f.write("# Tabela de Símbolos\n\n")
        f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        try:
            simbolos = tabela.listar_simbolos() if hasattr(tabela, 'listar_simbolos') else []
        except:
            simbolos = []

        if not simbolos:
            f.write("##   Tabela Vazia\n\n")
            f.write("Nenhum símbolo foi registrado durante a análise.\n")
        else:
            f.write(f"## Símbolos Registrados ({len(simbolos)})\n\n")
            f.write("| Nome | Tipo | Inicializado | Linha | Usos |\n")
            f.write("|------|------|--------------|-------|------|\n")

            for simbolo in simbolos:
                nome = simbolo.nome
                tipo = simbolo.tipo
                inicializado = "  Sim" if simbolo.inicializada else "  Não"
                linha = simbolo.linha_declaracao if simbolo.linha_declaracao else 'N/A'
                usos = tabela.obter_numero_usos(nome) if hasattr(tabela, 'obter_numero_usos') else 0

                f.write(f"| `{nome}` | `{tipo}` | {inicializado} | {linha} | {usos} |\n")

        f.write("\n---\n*Relatório gerado automaticamente pelo Compilador RA3_1*")


# ============================================================================
# FUNÇÃO DE INTEGRAÇÃO - CHAMADA PELO COMPILAR.PY
# ============================================================================

def executar_geracao_arvore_atribuida(resultado_semantico: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função principal chamada pelo compilar.py para gerar a árvore atribuída.

    Args:
        resultado_semantico: Resultado da análise semântica completa

    Returns:
        Dicionário com árvore atribuída e informações dos relatórios gerados
    """
    try:
        # Extrair dados do resultado semântico
        arvore_anotada = resultado_semantico.get('arvore_anotada', {})
        erros_sematicos = resultado_semantico.get('erros', [])
        tabela_simbolos = resultado_semantico.get('tabela_simbolos')

        # Gerar árvore atribuída (passando tabela de símbolos para propagar tipos de variáveis)
        arvore_atribuida = gerarArvoreAtribuida(arvore_anotada, tabela_simbolos)

        # Salvar árvore atribuída
        salvarArvoreAtribuida(arvore_atribuida)

        # Gerar relatórios
        gerarRelatoriosMarkdown(
            arvore_atribuida,
            erros_sematicos,
            tabela_simbolos,
            OUT_RELATORIOS_DIR
        )

        return {
            'sucesso': True,
            'arvore_atribuida': arvore_atribuida,
            'relatorios_gerados': [
                str(OUT_RELATORIOS_DIR / "arvore_atribuida.md"),
                str(OUT_RELATORIOS_DIR / "julgamento_tipos.md"),
                str(OUT_RELATORIOS_DIR / "erros_sematicos.md"),
                str(OUT_RELATORIOS_DIR / "tabela_simbolos.md"),
                str(ROOT_RELATORIOS_DIR / "arvore_atribuida.md"),
                str(ROOT_RELATORIOS_DIR / "julgamento_tipos.md"),
                str(ROOT_RELATORIOS_DIR / "erros_sematicos.md"),
                str(ROOT_RELATORIOS_DIR / "tabela_simbolos.md")
            ],
            'arquivo_arvore_json': str(OUT_ARVORE_ATRIBUIDA_JSON),
            'arquivo_arvore_json_raiz': str(ROOT_ARVORE_ATRIBUIDA_JSON)
        }

    except Exception as e:
        return {
            'sucesso': False,
            'erro': f"Erro na geração da árvore atribuída: {str(e)}",
            'arvore_atribuida': None,
            'relatorios_gerados': []
        }
