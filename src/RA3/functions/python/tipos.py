#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1

"""
Sistema de Tipos para o Analisador Semântico RPN

Este módulo define os tipos primitivos da linguagem e implementa as regras
de promoção de tipos, conversão de truthiness e verificação de compatibilidade
de tipos para todos os operadores.

Tipos Suportados:
    - int: Números inteiros
    - real: Números de ponto flutuante (IEEE 754)
    - boolean: Valores booleanos (resultado de comparações e operações lógicas)

Hierarquia de Tipos:
    int < real (int pode ser promovido a real)
    boolean - separado (sem promoção automática)
"""

# ============================================================================
# CONSTANTES DE TIPO
# ============================================================================

TYPE_INT = 'int'
"""Tipo inteiro - números inteiros"""

TYPE_REAL = 'real'
"""Tipo real - números de ponto flutuante"""

TYPE_BOOLEAN = 'boolean'
"""Tipo booleano - resultado de operações relacionais e lógicas"""

# Conjunto de todos os tipos válidos
TIPOS_VALIDOS = {TYPE_INT, TYPE_REAL, TYPE_BOOLEAN}

# Tipos numéricos (aceitam operações aritméticas)
TIPOS_NUMERICOS = {TYPE_INT, TYPE_REAL}

# Tipos que podem ser convertidos para booleano (truthiness)
TIPOS_TRUTHY = {TYPE_INT, TYPE_REAL, TYPE_BOOLEAN}


# ============================================================================
# FUNÇÕES DE PROMOÇÃO E CONVERSÃO DE TIPOS
# ============================================================================

def promover_tipo(tipo1: str, tipo2: str) -> str:
    """
    Promove tipos numéricos segundo a hierarquia int < real.

    Regras de Promoção:
        int + int → int
        int + real → real
        real + int → real
        real + real → real

    Args:
        tipo1: Primeiro tipo ('int' ou 'real')
        tipo2: Segundo tipo ('int' ou 'real')

    Returns:
        Tipo promovido ('int' ou 'real')

    Raises:
        ValueError: Se algum tipo não for numérico

    Examples:
        >>> promover_tipo('int', 'int')
        'int'
        >>> promover_tipo('int', 'real')
        'real'
        >>> promover_tipo('real', 'int')
        'real'
    """
    # Validação de entrada
    if tipo1 not in TIPOS_NUMERICOS or tipo2 not in TIPOS_NUMERICOS:
        raise ValueError(
            f"Promoção de tipo requer tipos numéricos. "
            f"Recebido: {tipo1}, {tipo2}"
        )

    # Promoção: se qualquer um é real, resultado é real
    if tipo1 == TYPE_REAL or tipo2 == TYPE_REAL:
        return TYPE_REAL

    # Ambos são int
    return TYPE_INT


def para_booleano(valor, tipo: str) -> bool:
    """
    Converte um valor de qualquer tipo para booleano usando regras de truthiness.

    Regras de Truthiness (Permissive Mode):
        - boolean: uso direto
        - int: 0 = false, qualquer outro = true
        - real: 0.0 = false, qualquer outro = true

    Args:
        valor: O valor a ser convertido
        tipo: O tipo do valor ('int', 'real', 'boolean')

    Returns:
        Valor booleano correspondente

    Raises:
        ValueError: Se o tipo não puder ser convertido para booleano

    Examples:
        >>> para_booleano(True, 'boolean')
        True
        >>> para_booleano(5, 'int')
        True
        >>> para_booleano(0, 'int')
        False
        >>> para_booleano(3.14, 'real')
        True
        >>> para_booleano(0.0, 'real')
        False
    """
    if tipo not in TIPOS_TRUTHY:
        raise ValueError(
            f"Tipo '{tipo}' não pode ser convertido para booleano. "
            f"Tipos permitidos: {TIPOS_TRUTHY}"
        )

    # Boolean: uso direto
    if tipo == TYPE_BOOLEAN:
        return bool(valor)

    # Numéricos: 0/0.0 = false, resto = true
    if tipo in TIPOS_NUMERICOS:
        return valor != 0

    # Não deveria chegar aqui devido à validação, mas por segurança
    raise ValueError(f"Conversão não implementada para tipo '{tipo}'")



# ============================================================================
# FUNÇÕES DE VERIFICAÇÃO DE COMPATIBILIDADE DE TIPOS
# ============================================================================

def tipos_compativeis_aritmetica(tipo1: str, tipo2: str) -> bool:
    """
    Verifica se dois tipos são compatíveis para operações aritméticas básicas.

    Operadores: +, -, *, | (divisão real)
    Aceita: int, real (com promoção automática)

    Args:
        tipo1: Tipo do primeiro operando
        tipo2: Tipo do segundo operando

    Returns:
        True se os tipos são compatíveis, False caso contrário

    Examples:
        >>> tipos_compativeis_aritmetica('int', 'int')
        True
        >>> tipos_compativeis_aritmetica('int', 'real')
        True
        >>> tipos_compativeis_aritmetica('boolean', 'int')
        False
    """
    return tipo1 in TIPOS_NUMERICOS and tipo2 in TIPOS_NUMERICOS


def tipos_compativeis_divisao_inteira(tipo1: str, tipo2: str) -> bool:
    """
    Verifica se dois tipos são compatíveis para divisão inteira ou módulo.

    Operadores: / (divisão inteira), % (módulo)
    Aceita: APENAS int + int
    Rejeita: real em qualquer operando

    Args:
        tipo1: Tipo do primeiro operando
        tipo2: Tipo do segundo operando

    Returns:
        True se ambos são int, False caso contrário

    Examples:
        >>> tipos_compativeis_divisao_inteira('int', 'int')
        True
        >>> tipos_compativeis_divisao_inteira('int', 'real')
        False
        >>> tipos_compativeis_divisao_inteira('real', 'real')
        False
    """
    return tipo1 == TYPE_INT and tipo2 == TYPE_INT


def tipos_compativeis_potencia(tipo_base: str, tipo_expoente: str) -> bool:
    """
    Verifica se os tipos são compatíveis para operação de potência.

    Operador: ^ (potência)
    Base: int ou real
    Expoente: DEVE ser int (verificação adicional de > 0 feita em tempo de execução)
    Resultado: mesmo tipo da base

    Args:
        tipo_base: Tipo da base (A em A^B)
        tipo_expoente: Tipo do expoente (B em A^B)

    Returns:
        True se base é numérica e expoente é int, False caso contrário

    Examples:
        >>> tipos_compativeis_potencia('int', 'int')
        True
        >>> tipos_compativeis_potencia('real', 'int')
        True
        >>> tipos_compativeis_potencia('int', 'real')
        False
    """
    return tipo_base in TIPOS_NUMERICOS and tipo_expoente == TYPE_INT


def tipos_compativeis_comparacao(tipo1: str, tipo2: str) -> bool:
    """
    Verifica se dois tipos são compatíveis para operações de comparação.

    Operadores: >, <, >=, <=, ==, !=
    Aceita: int, real (qualquer combinação)
    Retorna: SEMPRE boolean

    Args:
        tipo1: Tipo do primeiro operando
        tipo2: Tipo do segundo operando

    Returns:
        True se ambos são numéricos, False caso contrário

    Examples:
        >>> tipos_compativeis_comparacao('int', 'int')
        True
        >>> tipos_compativeis_comparacao('int', 'real')
        True
        >>> tipos_compativeis_comparacao('boolean', 'int')
        False
    """
    return tipo1 in TIPOS_NUMERICOS and tipo2 in TIPOS_NUMERICOS


def tipos_compativeis_logico(tipo1: str, tipo2: str) -> bool:
    """
    Verifica se dois tipos são compatíveis para operações lógicas binárias.

    Operadores: && (AND), || (OR)
    Aceita: boolean, int, real (modo permissivo com truthiness)
    Retorna: SEMPRE boolean

    Nota: Modo permissivo permite int/real através de conversão truthiness.

    Args:
        tipo1: Tipo do primeiro operando
        tipo2: Tipo do segundo operando

    Returns:
        True se ambos podem ser convertidos para boolean, False caso contrário

    Examples:
        >>> tipos_compativeis_logico('boolean', 'boolean')
        True
        >>> tipos_compativeis_logico('int', 'boolean')
        True
        >>> tipos_compativeis_logico('int', 'int')
        True
    """
    return tipo1 in TIPOS_TRUTHY and tipo2 in TIPOS_TRUTHY


def tipo_compativel_logico_unario(tipo: str) -> bool:
    """
    Verifica se um tipo é compatível para operação lógica unária (NOT).

    Operador: ! (NOT)
    Aceita: boolean, int, real (modo permissivo com truthiness)
    Retorna: SEMPRE boolean

    Args:
        tipo: Tipo do operando

    Returns:
        True se o tipo pode ser convertido para boolean, False caso contrário

    Examples:
        >>> tipo_compativel_logico_unario('boolean')
        True
        >>> tipo_compativel_logico_unario('int')
        True
    """
    return tipo in TIPOS_TRUTHY


def tipo_compativel_condicao(tipo: str) -> bool:
    """
    Verifica se um tipo é compatível para uso como condição em estruturas de controle.

    Estruturas: IFELSE, WHILE, FOR
    Aceita: boolean, int, real (modo permissivo com truthiness)

    Args:
        tipo: Tipo da condição

    Returns:
        True se o tipo pode ser usado como condição, False caso contrário

    Examples:
        >>> tipo_compativel_condicao('boolean')
        True
        >>> tipo_compativel_condicao('int')
        True
    """
    return tipo in TIPOS_TRUTHY


def tipo_compativel_armazenamento(tipo: str) -> bool:
    """
    Verifica se um tipo pode ser armazenado em memória (MEM).

    Restrição Crítica: Boolean NÃO pode ser armazenado em memória!
    Aceita: int, real
    Rejeita: boolean

    Args:
        tipo: Tipo a ser armazenado

    Returns:
        True se o tipo pode ser armazenado, False caso contrário

    Examples:
        >>> tipo_compativel_armazenamento('int')
        True
        >>> tipo_compativel_armazenamento('real')
        True
        >>> tipo_compativel_armazenamento('boolean')
        False
    """
    return tipo in TIPOS_NUMERICOS


# ============================================================================
# FUNÇÕES DE INFERÊNCIA DE TIPO RESULTANTE
# ============================================================================

def tipo_resultado_aritmetica(tipo1: str, tipo2: str, operador: str) -> str:
    """
    Determina o tipo resultante de uma operação aritmética.

    Regras:
        +, -, *: promover_tipo(tipo1, tipo2)
        |: SEMPRE real (divisão real)
        /, %: SEMPRE int (divisão inteira/módulo)
        ^: tipo da base (potência)

    Args:
        tipo1: Tipo do primeiro operando
        tipo2: Tipo do segundo operando
        operador: Símbolo do operador (+, -, *, |, /, %, ^)

    Returns:
        Tipo do resultado da operação

    Raises:
        ValueError: Se os tipos não são compatíveis para a operação

    Examples:
        >>> tipo_resultado_aritmetica('int', 'int', '+')
        'int'
        >>> tipo_resultado_aritmetica('int', 'real', '+')
        'real'
        >>> tipo_resultado_aritmetica('int', 'int', '|')
        'real'
        >>> tipo_resultado_aritmetica('real', 'int', '^')
        'real'
    """
    # Divisão real: sempre retorna real
    if operador == '|':
        if not tipos_compativeis_aritmetica(tipo1, tipo2):
            raise ValueError(
                f"Operador '|' requer operandos numéricos. "
                f"Recebido: {tipo1}, {tipo2}"
            )
        return TYPE_REAL

    # Divisão inteira e módulo: requer int, retorna int
    if operador in ['/', '%']:
        if not tipos_compativeis_divisao_inteira(tipo1, tipo2):
            raise ValueError(
                f"Operador '{operador}' requer operandos inteiros. "
                f"Recebido: {tipo1}, {tipo2}"
            )
        return TYPE_INT

    # Potência: retorna tipo da base
    if operador == '^':
        if not tipos_compativeis_potencia(tipo1, tipo2):
            raise ValueError(
                f"Operador '^' requer base numérica e expoente inteiro. "
                f"Recebido: base={tipo1}, expoente={tipo2}"
            )
        return tipo1  # Retorna o tipo da base

    # Operadores com promoção: +, -, *
    if operador in ['+', '-', '*']:
        if not tipos_compativeis_aritmetica(tipo1, tipo2):
            raise ValueError(
                f"Operador '{operador}' requer operandos numéricos. "
                f"Recebido: {tipo1}, {tipo2}"
            )
        return promover_tipo(tipo1, tipo2)

    # Operador desconhecido
    raise ValueError(f"Operador aritmético desconhecido: '{operador}'")


def tipo_resultado_comparacao(tipo1: str, tipo2: str) -> str:
    """
    Determina o tipo resultante de uma operação de comparação.

    Operadores: >, <, >=, <=, ==, !=
    Retorna: SEMPRE boolean

    Args:
        tipo1: Tipo do primeiro operando
        tipo2: Tipo do segundo operando

    Returns:
        TYPE_BOOLEAN

    Raises:
        ValueError: Se os tipos não são compatíveis para comparação

    Examples:
        >>> tipo_resultado_comparacao('int', 'int')
        'boolean'
        >>> tipo_resultado_comparacao('int', 'real')
        'boolean'
    """
    if not tipos_compativeis_comparacao(tipo1, tipo2):
        raise ValueError(
            f"Operadores de comparação requerem operandos numéricos. "
            f"Recebido: {tipo1}, {tipo2}"
        )
    return TYPE_BOOLEAN


def tipo_resultado_logico(tipo1: str, tipo2: str) -> str:
    """
    Determina o tipo resultante de uma operação lógica binária.

    Operadores: && (AND), || (OR)
    Retorna: SEMPRE boolean
    Modo: Permissivo (aceita int/real via truthiness)

    Args:
        tipo1: Tipo do primeiro operando
        tipo2: Tipo do segundo operando

    Returns:
        TYPE_BOOLEAN

    Raises:
        ValueError: Se os tipos não podem ser convertidos para boolean

    Examples:
        >>> tipo_resultado_logico('boolean', 'boolean')
        'boolean'
        >>> tipo_resultado_logico('int', 'int')
        'boolean'
    """
    if not tipos_compativeis_logico(tipo1, tipo2):
        raise ValueError(
            f"Operadores lógicos requerem operandos convertíveis para boolean. "
            f"Recebido: {tipo1}, {tipo2}"
        )
    return TYPE_BOOLEAN


def tipo_resultado_logico_unario(tipo: str) -> str:
    """
    Determina o tipo resultante de uma operação lógica unária.

    Operador: ! (NOT)
    Retorna: SEMPRE boolean
    Modo: Permissivo (aceita int/real via truthiness)

    Args:
        tipo: Tipo do operando

    Returns:
        TYPE_BOOLEAN

    Raises:
        ValueError: Se o tipo não pode ser convertido para boolean

    Examples:
        >>> tipo_resultado_logico_unario('boolean')
        'boolean'
        >>> tipo_resultado_logico_unario('int')
        'boolean'
    """
    if not tipo_compativel_logico_unario(tipo):
        raise ValueError(
            f"Operador '!' requer operando convertível para boolean. "
            f"Recebido: {tipo}"
        )
    return TYPE_BOOLEAN


# ============================================================================
# UTILIDADES
# ============================================================================

def descricao_tipo(tipo: str) -> str:
    """
    Retorna uma descrição legível de um tipo.

    Args:
        tipo: Nome do tipo

    Returns:
        Descrição do tipo em português

    Examples:
        >>> descricao_tipo('int')
        'inteiro'
        >>> descricao_tipo('boolean')
        'booleano'
    """
    descricoes = {
        TYPE_INT: 'inteiro',
        TYPE_REAL: 'real (ponto flutuante)',
        TYPE_BOOLEAN: 'booleano'
    }
    return descricoes.get(tipo, f'tipo desconhecido ({tipo})')


if __name__ == '__main__':
    # Testes básicos
    import doctest
    doctest.testmod()

    print("✅ Módulo tipos.py carregado com sucesso!")
    print(f"Tipos válidos: {TIPOS_VALIDOS}")
    print(f"Tipos numéricos: {TIPOS_NUMERICOS}")
    print(f"Tipos truthy: {TIPOS_TRUTHY}")
