#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1

"""
Gramática de Atributos para o Analisador Semântico RPN

Este módulo define a gramática de atributos completa da linguagem RPN,
especificando as regras semânticas para todos os operadores, estruturas de
controle e comandos especiais.

A gramática de atributos associa regras semânticas a cada produção da gramática
sintática, permitindo:
    - Verificação de tipos
    - Inferência de tipos
    - Coerção de tipos (int → real)
    - Validação de restrições semânticas
    - Geração de AST atribuída

Estrutura de uma Regra Semântica:
    {
        'categoria': str,           # 'aritmetico', 'comparacao', etc.
        'operador': str,            # Símbolo do operador
        'aridade': int,             # 1 (unário) ou 2 (binário)
        'tipos_operandos': list,    # Tipos aceitos para cada operando
        'tipo_resultado': str/callable,  # Tipo do resultado ou função
        'restricoes': list,         # Restrições adicionais
        'acao_semantica': callable, # Função que aplica a regra
        'descricao': str            # Descrição legível
    }
"""

from typing import Dict, List, Any, Optional
from src.RA3.functions.python import tipos
from src.RA3.functions.python.tabela_simbolos import TabelaSimbolos


# ============================================================================
# TIPO ALIASES
# ============================================================================

RegraSemantica = Dict[str, Any]


# ============================================================================
# GRAMÁTICA DE ATRIBUTOS - OPERADORES ARITMÉTICOS
# ============================================================================

def definir_regras_aritmeticas() -> Dict[str, RegraSemantica]:
    """
    Define regras semânticas para operadores aritméticos.

    Operadores: +, -, *, |, /, %, ^

    Returns:
        Dicionário mapeando operador → regra semântica
    """
    regras = {}

    # Operadores com promoção de tipos: +, -, *
    for op_simbolo, op_nome in [('+', 'soma'), ('-', 'subtracao'), ('*', 'multiplicacao')]:
        regras[op_simbolo] = {
            'categoria': 'aritmetico',
            'operador': op_simbolo,
            'nome': op_nome,
            'aridade': 2,
            'tipos_operandos': [tipos.TIPOS_NUMERICOS, tipos.TIPOS_NUMERICOS],
            'tipo_resultado': lambda op1, op2: tipos.promover_tipo(op1['tipo'], op2['tipo']),
            'restricoes': [
                'Ambos operandos devem ser numéricos (int ou real)',
                'Resultado promovido para real se qualquer operando é real'
            ],
            'acao_semantica': lambda op1, op2, tabela: {
                'tipo': tipos.promover_tipo(op1['tipo'], op2['tipo']),
                'valor': None,  # Valor calculado em tempo de execução
                'operandos': [op1, op2]
            },
            'descricao': f'Operador {op_nome} com promoção de tipos',
            'regra_formal': f'Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {{int, real}})\n'
                          f'───────────────────────────────────────────────────────\n'
                          f'    Γ ⊢ (e₁ e₂ {op_simbolo}) : promover_tipo(T₁, T₂)'
        }

    # Divisão real: sempre retorna real
    regras['|'] = {
        'categoria': 'aritmetico',
        'operador': '|',
        'nome': 'divisao_real',
        'aridade': 2,
        'tipos_operandos': [tipos.TIPOS_NUMERICOS, tipos.TIPOS_NUMERICOS],
        'tipo_resultado': lambda op1, op2: tipos.TYPE_REAL,
        'restricoes': [
            'Ambos operandos devem ser numéricos',
            'Resultado SEMPRE é real, mesmo se ambos operandos são int'
        ],
        'acao_semantica': lambda op1, op2, tabela: {
            'tipo': tipos.TYPE_REAL,
            'valor': None,
            'operandos': [op1, op2]
        },
        'descricao': 'Divisão real - sempre retorna real',
        'regra_formal': 'Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})\n'
                       '───────────────────────────────────────────────────────\n'
                       '           Γ ⊢ (e₁ e₂ |) : real'
    }

    # Divisão inteira e módulo: requerem int
    for op_simbolo, op_nome in [('/', 'divisao_inteira'), ('%', 'resto')]:
        regras[op_simbolo] = {
            'categoria': 'aritmetico',
            'operador': op_simbolo,
            'nome': op_nome,
            'aridade': 2,
            'tipos_operandos': [{tipos.TYPE_INT}, {tipos.TYPE_INT}],
            'tipo_resultado': lambda op1, op2: tipos.TYPE_INT,
            'restricoes': [
                'AMBOS operandos DEVEM ser inteiros',
                'Erro semântico se qualquer operando for real'
            ],
            'acao_semantica': lambda op1, op2, tabela: {
                'tipo': tipos.TYPE_INT,
                'valor': None,
                'operandos': [op1, op2],
                'validacao': tipos.tipos_compativeis_divisao_inteira(op1['tipo'], op2['tipo'])
            },
            'descricao': f'Operador {op_nome} - apenas inteiros',
            'regra_formal': f'Γ ⊢ e₁ : int    Γ ⊢ e₂ : int\n'
                          f'─────────────────────────────\n'
                          f'    Γ ⊢ (e₁ e₂ {op_simbolo}) : int'
        }

    # Potência: expoente deve ser int positivo
    regras['^'] = {
        'categoria': 'aritmetico',
        'operador': '^',
        'nome': 'potencia',
        'aridade': 2,
        'tipos_operandos': [tipos.TIPOS_NUMERICOS, {tipos.TYPE_INT}],
        'tipo_resultado': lambda op1, op2: op1['tipo'],  # Tipo da base
        'restricoes': [
            'Base pode ser int ou real',
            'Expoente DEVE ser int',
            'Expoente DEVE ser positivo (> 0) - verificado em runtime'
        ],
        'acao_semantica': lambda op1, op2, tabela: {
            'tipo': op1['tipo'],  # Resultado tem tipo da base
            'valor': None,
            'operandos': [op1, op2],
            'validacao_tipo': tipos.tipos_compativeis_potencia(op1['tipo'], op2['tipo']),
            'validacao_valor': lambda: op2.get('valor', 1) > 0  # Se valor conhecido, deve ser > 0
        },
        'descricao': 'Potenciação - expoente deve ser int positivo',
        'regra_formal': 'Γ ⊢ e₁ : T    Γ ⊢ e₂ : int    e₂ > 0    (T ∈ {int, real})\n'
                       '──────────────────────────────────────────────────────────\n'
                       '               Γ ⊢ (e₁ e₂ ^) : T'
    }

    return regras


# ============================================================================
# GRAMÁTICA DE ATRIBUTOS - OPERADORES DE COMPARAÇÃO
# ============================================================================

def definir_regras_comparacao() -> Dict[str, RegraSemantica]:
    """
    Define regras semânticas para operadores de comparação.

    Operadores: >, <, >=, <=, ==, !=
    Retornam SEMPRE boolean

    Returns:
        Dicionário mapeando operador → regra semântica
    """
    regras = {}

    operadores = [
        ('>', 'maior'),
        ('<', 'menor'),
        ('>=', 'maior_igual'),
        ('<=', 'menor_igual'),
        ('==', 'igual'),
        ('!=', 'diferente')
    ]

    for op_simbolo, op_nome in operadores:
        regras[op_simbolo] = {
            'categoria': 'comparacao',
            'operador': op_simbolo,
            'nome': op_nome,
            'aridade': 2,
            'tipos_operandos': [tipos.TIPOS_NUMERICOS, tipos.TIPOS_NUMERICOS],
            'tipo_resultado': lambda op1, op2: tipos.TYPE_BOOLEAN,
            'restricoes': [
                'Operandos devem ser numéricos (int ou real)',
                'Resultado SEMPRE é boolean'
            ],
            'acao_semantica': lambda op1, op2, tabela: {
                'tipo': tipos.TYPE_BOOLEAN,
                'valor': None,
                'operandos': [op1, op2]
            },
            'descricao': f'Comparação {op_nome} - retorna boolean',
            'regra_formal': f'Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {{int, real}})\n'
                          f'─────────────────────────────────────────────────────\n'
                          f'          Γ ⊢ (e₁ e₂ {op_simbolo}) : boolean'
        }

    return regras


# ============================================================================
# GRAMÁTICA DE ATRIBUTOS - OPERADORES LÓGICOS
# ============================================================================

def definir_regras_logicas() -> Dict[str, RegraSemantica]:
    """
    Define regras semânticas para operadores lógicos.

    Operadores: && (AND), || (OR), ! (NOT)
    Modo Permissivo: aceita int/real via truthiness

    Returns:
        Dicionário mapeando operador → regra semântica
    """
    regras = {}

    # Operadores binários: AND, OR
    for op_simbolo, op_nome in [('&&', 'and'), ('||', 'or')]:
        regras[op_simbolo] = {
            'categoria': 'logico',
            'operador': op_simbolo,
            'nome': op_nome,
            'aridade': 2,
            'tipos_operandos': [tipos.TIPOS_TRUTHY, tipos.TIPOS_TRUTHY],
            'tipo_resultado': lambda op1, op2: tipos.TYPE_BOOLEAN,
            'restricoes': [
                'Operandos podem ser boolean, int ou real (modo permissivo)',
                'Valores numéricos convertidos via truthiness (0 = false)',
                'Resultado SEMPRE é boolean'
            ],
            'acao_semantica': lambda op1, op2, tabela: {
                'tipo': tipos.TYPE_BOOLEAN,
                'valor': None,
                'operandos': [op1, op2],
                'conversao_op1': tipos.para_booleano(op1.get('valor'), op1['tipo']) if op1.get('valor') is not None else None,
                'conversao_op2': tipos.para_booleano(op2.get('valor'), op2['tipo']) if op2.get('valor') is not None else None
            },
            'descricao': f'Operador lógico {op_nome} - modo permissivo com truthiness',
            'regra_formal': f'Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {{int, real, boolean}})\n'
                          f'──────────────────────────────────────────────────────────────\n'
                          f'           Γ ⊢ (e₁ e₂ {op_simbolo}) : boolean'
        }

    # Operador unário: NOT
    regras['!'] = {
        'categoria': 'logico',
        'operador': '!',
        'nome': 'not',
        'aridade': 1,
        'tipos_operandos': [tipos.TIPOS_TRUTHY],
        'tipo_resultado': lambda op1: tipos.TYPE_BOOLEAN,
        'restricoes': [
            'Operando pode ser boolean, int ou real (modo permissivo)',
            'Sintaxe: (operando !) - unário postfix',
            'Resultado SEMPRE é boolean'
        ],
        'acao_semantica': lambda op1, tabela: {
            'tipo': tipos.TYPE_BOOLEAN,
            'valor': None,
            'operandos': [op1],
            'conversao': tipos.para_booleano(op1.get('valor'), op1['tipo']) if op1.get('valor') is not None else None
        },
        'descricao': 'Operador NOT unário - modo permissivo',
        'regra_formal': 'Γ ⊢ e : T    (T ∈ {int, real, boolean})\n'
                       '───────────────────────────────────────\n'
                       '       Γ ⊢ (e !) : boolean'
    }

    return regras


# ============================================================================
# GRAMÁTICA DE ATRIBUTOS - ESTRUTURAS DE CONTROLE
# ============================================================================

def definir_regras_controle() -> Dict[str, RegraSemantica]:
    """
    Define regras semânticas para estruturas de controle.

    Estruturas: IFELSE, WHILE, FOR
    Retornam tipo da última expressão do corpo

    Returns:
        Dicionário mapeando estrutura → regra semântica
    """
    regras = {}

    # IFELSE: (condição blocoTrue blocoFalse IFELSE)
    regras['IFELSE'] = {
        'categoria': 'controle',
        'operador': 'IFELSE',
        'nome': 'ifelse',
        'aridade': 3,
        'tipos_operandos': [
            tipos.TIPOS_TRUTHY,  # Condição
            None,                # BlocoTrue (qualquer tipo T)
            None                 # BlocoFalse (qualquer tipo T)
        ],
        'tipo_resultado': lambda cond, true_b, false_b: true_b['tipo'] if true_b['tipo'] == false_b['tipo'] else 'ERROR',
        'restricoes': [
            'Condição deve ser convertível para boolean (modo permissivo)',
            'Ambos os ramos (true e false) DEVEM ter o MESMO tipo',
            'Resultado tem o tipo dos ramos'
        ],
        'acao_semantica': lambda cond, true_branch, false_branch, tabela: {
            'tipo': true_branch['tipo'] if true_branch['tipo'] == false_branch['tipo'] else None,
            'erro': None if true_branch['tipo'] == false_branch['tipo'] else 'Ramos do IFELSE devem ter o mesmo tipo',
            'valor': None,
            'operandos': [cond, true_branch, false_branch]
        },
        'descricao': 'Estrutura condicional IFELSE - ramos devem ter mesmo tipo',
        'regra_formal': 'Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ true : T    Γ ⊢ false : T\n'
                       '────────────────────────────────────────────────────────────────\n'
                       '           Γ ⊢ (cond true false IFELSE) : T'
    }

    # WHILE: (condição corpo WHILE)
    regras['WHILE'] = {
        'categoria': 'controle',
        'operador': 'WHILE',
        'nome': 'while',
        'aridade': 2,
        'tipos_operandos': [
            tipos.TIPOS_TRUTHY,  # Condição
            None                 # Corpo (qualquer tipo T)
        ],
        'tipo_resultado': lambda cond, corpo: corpo['tipo'],
        'restricoes': [
            'Condição deve ser convertível para boolean',
            'Corpo pode ter qualquer tipo',
            'Resultado tem tipo da última expressão do corpo'
        ],
        'acao_semantica': lambda cond, corpo, tabela: {
            'tipo': corpo['tipo'],
            'valor': None,
            'operandos': [cond, corpo]
        },
        'descricao': 'Laço WHILE - retorna tipo do corpo',
        'regra_formal': 'Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ corpo : T\n'
                       '──────────────────────────────────────────────────\n'
                       '         Γ ⊢ (cond corpo WHILE) : T'
    }

    # FOR: (inicio fim passo corpo FOR)
    regras['FOR'] = {
        'categoria': 'controle',
        'operador': 'FOR',
        'nome': 'for',
        'aridade': 4,
        'tipos_operandos': [
            {tipos.TYPE_INT},  # Inicio
            {tipos.TYPE_INT},  # Fim
            {tipos.TYPE_INT},  # Passo
            None               # Corpo
        ],
        'tipo_resultado': lambda init, end, step, corpo: corpo['tipo'],
        'restricoes': [
            'Inicio, fim e passo DEVEM ser inteiros',
            'Corpo pode ter qualquer tipo',
            'Resultado tem tipo da última expressão do corpo'
        ],
        'acao_semantica': lambda init, end, step, corpo, tabela: {
            'tipo': corpo['tipo'],
            'valor': None,
            'operandos': [init, end, step, corpo],
            'validacao': init['tipo'] == tipos.TYPE_INT and
                        end['tipo'] == tipos.TYPE_INT and
                        step['tipo'] == tipos.TYPE_INT
        },
        'descricao': 'Laço FOR - contador inteiro, retorna tipo do corpo',
        'regra_formal': 'Γ ⊢ init : int    Γ ⊢ end : int    Γ ⊢ step : int    Γ ⊢ corpo : T\n'
                       '────────────────────────────────────────────────────────────────\n'
                       '              Γ ⊢ (init end step corpo FOR) : T'
    }

    return regras


# ============================================================================
# GRAMÁTICA DE ATRIBUTOS - COMANDOS ESPECIAIS
# ============================================================================

def definir_regras_comandos() -> Dict[str, RegraSemantica]:
    """
    Define regras semânticas para comandos especiais.

    Comandos: MEM (armazenamento/recuperação), RES (referência)

    Returns:
        Dicionário mapeando comando → regra semântica
    """
    regras = {}

    # MEM Store: (valor VARIAVEL) - armazena valor em memória
    regras['MEM_STORE'] = {
        'categoria': 'comando',
        'operador': 'MEM',
        'nome': 'mem_store',
        'aridade': 2,  # valor + nome_variavel
        'tipos_operandos': [tipos.TIPOS_NUMERICOS, None],
        'tipo_resultado': lambda val, var: val['tipo'],
        'restricoes': [
            'Valor DEVE ser int ou real',
            'Boolean NÃO pode ser armazenado (erro semântico)',
            'Variável é marcada como inicializada na tabela de símbolos'
        ],
        'acao_semantica': lambda valor, variavel, tabela: {
            'tipo': valor['tipo'],
            'valor': valor.get('valor'),
            'variavel': variavel,
            'operacao': 'armazenamento',
            'efeito_tabela': tabela.adicionarSimbolo(variavel, valor['tipo'], inicializada=True)
        },
        'descricao': 'Armazenamento em memória - apenas int/real',
        'regra_formal': 'Γ ⊢ e : T    T ∈ {int, real}    Γ[x ↦ (T, initialized)] ⊢ ...\n'
                       '───────────────────────────────────────────────────────────\n'
                       '            Γ ⊢ (e x MEM) : T'
    }

    # MEM Load: (VARIAVEL) - recupera valor da memória
    regras['MEM_LOAD'] = {
        'categoria': 'comando',
        'operador': 'MEM',
        'nome': 'mem_load',
        'aridade': 1,
        'tipos_operandos': [None],  # Nome da variável (string)
        'tipo_resultado': lambda var, tabela: tabela.obter_tipo(var) if tabela.existe(var) else None,
        'restricoes': [
            'Variável DEVE estar inicializada (erro se não)',
            'Retorna tipo armazenado na variável'
        ],
        'acao_semantica': lambda variavel, tabela: {
            'tipo': tabela.obter_tipo(variavel),
            'variavel': variavel,
            'operacao': 'recuperacao',
            'inicializada': tabela.verificar_inicializacao(variavel),
            'erro': None if tabela.verificar_inicializacao(variavel)
                    else f"Variável '{variavel}' usada sem inicialização"
        },
        'descricao': 'Recuperação de memória - erro se não inicializada',
        'regra_formal': 'Γ(x) = (T, initialized)\n'
                       '───────────────────────\n'
                       '    Γ ⊢ (x) : T'
    }

    # RES: (N RES) - referencia resultado N linhas atrás
    # Suporta tanto literal inteiro quanto variável contendo offset
    regras['RES'] = {
        'categoria': 'comando',
        'operador': 'RES',
        'nome': 'res',
        'aridade': 1,
        'tipos_operandos': [{tipos.TYPE_INT}],  # Aceita int (literal ou variável)
        'tipo_resultado': None,  # Depende da linha referenciada
        'restricoes': [
            'Operando deve ser inteiro (literal ou variável)',
            'Se variável, deve estar inicializada',
            'Valor deve ser não negativo (N ≥ 0)',
            'Linha referenciada deve existir (linha_atual - N ≥ 1)',
            'Pode referenciar resultados boolean (diferente de MEM)'
        ],
        'acao_semantica': lambda operando, linha_atual, historico_tipos, tabela: {
            # Operando pode ser literal ou variável
            # Se for variável, valor já foi resolvido pela análise semântica
            'tipo': historico_tipos.get(linha_atual - operando.get('valor', 0))
                    if operando.get('valor') is not None else None,
            'linha_referencia': linha_atual - operando.get('valor', 0),
            'operacao': 'referencia',
            'operando_tipo': operando.get('operando_tipo', 'literal'),  # 'literal' ou 'variavel'
            'erro': None if (operando.get('valor') is not None and
                           operando['valor'] >= 0 and
                           linha_atual - operando['valor'] >= 1)
                    else (f"Offset inválido: {operando.get('valor')}" if operando.get('valor', -1) < 0
                          else f"Referência inválida: linha {linha_atual - operando.get('valor', 0)}")
        },
        'descricao': 'Referência a resultado anterior - aceita literal ou variável - aceita boolean',
        'regra_formal':
            '# Caso 1: Literal inteiro\n'
            'Γ ⊢ N : int    N ≥ 0    linha_atual - N ≥ 1    tipo_linha(atual - N) = T\n'
            '──────────────────────────────────────────────────────────────────────────\n'
            '                      Γ ⊢ (N RES) : T\n\n'
            '# Caso 2: Variável contendo offset\n'
            'Γ(VAR) = (int, initialized)    VAR ≥ 0    linha_atual - VAR ≥ 1    tipo_linha(atual - VAR) = T\n'
            '───────────────────────────────────────────────────────────────────────────────────────────────\n'
            '                               Γ ⊢ (VAR RES) : T'
    }

    # EPSILON (Identidade): (valor) - expressão com operando único sem operador
    # Suporta: (5), (VAR), ((A B +))
    regras['EPSILON'] = {
        'categoria': 'comando',
        'operador': 'EPSILON',
        'nome': 'identidade',
        'aridade': 1,
        'tipos_operandos': [tipos.TIPOS_VALIDOS],  # Aceita qualquer tipo
        'tipo_resultado': lambda operando: operando['tipo'],  # Função identidade
        'restricoes': [
            'Nenhuma restrição de tipo',
            'Retorna o operando inalterado (função identidade)'
        ],
        'acao_semantica': lambda operando, tabela: {
            'tipo': operando['tipo'],
            'valor': operando.get('valor'),
            'operando': operando,
            'operacao': 'identidade'
        },
        'descricao': 'Expressão de identidade - retorna operando sem modificação',
        'regra_formal':
            'Γ ⊢ e : T\n'
            '─────────────\n'
            ' Γ ⊢ (e) : T\n\n'
            '# Casos de uso:\n'
            '# - Carga de memória: (VAR)\n'
            '# - Literal direto: (5), (3.14)\n'
            '# - Expressão aninhada: ((A B +))'
    }

    return regras


# ============================================================================
# FUNÇÃO PRINCIPAL: DEFINIR GRAMÁTICA COMPLETA
# ============================================================================

def definirGramaticaAtributos() -> Dict[str, Dict[str, RegraSemantica]]:
    """
    Define a gramática de atributos completa para a linguagem RPN.

    Combina todas as categorias de regras semânticas:
        - Operadores aritméticos
        - Operadores de comparação
        - Operadores lógicos
        - Estruturas de controle
        - Comandos especiais

    Returns:
        Dicionário organizado por categoria, contendo todas as regras semânticas

    Example:
        >>> gramatica = definirGramaticaAtributos()
        >>> 'aritmetico' in gramatica
        True
        >>> '+' in gramatica['aritmetico']
        True
    """
    gramatica = {
        'aritmetico': definir_regras_aritmeticas(),
        'comparacao': definir_regras_comparacao(),
        'logico': definir_regras_logicas(),
        'controle': definir_regras_controle(),
        'comando': definir_regras_comandos()
    }

    return gramatica


def inicializar_sistema_semantico() -> tuple[Dict, TabelaSimbolos]:
    """
    Inicializa o sistema semântico completo.

    Returns:
        Tupla (gramática_atributos, tabela_simbolos)

    Example:
        >>> gramatica, tabela = inicializar_sistema_semantico()
        >>> len(gramatica)
        5
        >>> isinstance(tabela, TabelaSimbolos)
        True
    """
    from src.RA3.functions.python.tabela_simbolos import inicializarTabelaSimbolos

    gramatica = definirGramaticaAtributos()
    tabela = inicializarTabelaSimbolos()

    return gramatica, tabela


# ============================================================================
# UTILIDADES E HELPERS
# ============================================================================

def obter_regra(operador: str, categoria: Optional[str] = None) -> Optional[RegraSemantica]:
    """
    Busca a regra semântica de um operador.

    Args:
        operador: Símbolo do operador
        categoria: Categoria (opcional, acelera busca)

    Returns:
        RegraSemantica se encontrada, None caso contrário
    """
    gramatica = definirGramaticaAtributos()

    if categoria and categoria in gramatica:
        return gramatica[categoria].get(operador)

    # Busca em todas as categorias
    for cat_regras in gramatica.values():
        if operador in cat_regras:
            return cat_regras[operador]

    return None


if __name__ == '__main__':
    print("✅ Módulo gramatica_atributos.py carregado com sucesso!\n")

    # Exibir estatísticas
    gramatica = definirGramaticaAtributos()

    print("=" * 70)
    print("GRAMÁTICA DE ATRIBUTOS - ESTATÍSTICAS")
    print("=" * 70)

    total_regras = 0
    for categoria, regras in gramatica.items():
        print(f"\n{categoria.upper()}: {len(regras)} regras")
        for op, regra in regras.items():
            print(f"  - {op:10s} ({regra['nome']:20s}) - {regra['aridade']} operandos")
            total_regras += 1

    print("\n" + "=" * 70)
    print(f"TOTAL: {total_regras} regras semânticas definidas")
    print("=" * 70)

    # Testar sistema
    print("\nTestando inicialização do sistema...")
    gram, tab = inicializar_sistema_semantico()
    print(f"✅ Sistema inicializado: {len(gram)} categorias, tabela vazia ({len(tab)} símbolos)")
