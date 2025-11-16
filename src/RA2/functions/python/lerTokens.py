#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

import sys
from typing import List, Optional
from src.RA1.functions.python.tokens import Tipo_de_Token, Token

def lerTokens(arquivo: str) -> List[Token]:

    tokens = []

    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            for linha_num, linha in enumerate(f, 1):
                linha = linha.strip()

                # Pular linhas vazias e comentários
                if not linha or linha.startswith('#'):
                    continue

                # Processar tokens da linha
                tokens_linha = processarLinha(linha, linha_num)
                tokens.extend(tokens_linha)

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de tokens não encontrado: {arquivo}")
    except Exception as e:
        raise ValueError(f"Erro ao ler arquivo de tokens: {e}")

    # Adicionar token de fim de arquivo
    tokens.append(Token(Tipo_de_Token.FIM, "$"))

    return tokens

def processarLinha(linha: str, linha_num: int) -> List[Token]:
    
    tokens = []
    
    # Usar análise caractere por caractere para capturar parênteses e elementos
    i = 0
    while i < len(linha):
        char = linha[i]
        
        # Pular espaços
        if char.isspace():
            i += 1
            continue
        
        # Processar parênteses individualmente
        if char == '(':
            token = reconhecerToken('(', linha_num)
            if token:
                tokens.append(token)
            i += 1
        elif char == ')':
            token = reconhecerToken(')', linha_num)
            if token:
                tokens.append(token)
            i += 1
        else:
            # Extrair elemento completo (número, variável, operador, palavra-chave)
            elemento = ''

            while i < len(linha) and not linha[i].isspace() and linha[i] not in '()':
                elemento += linha[i]
                i += 1
            
            if elemento:
                token = reconhecerToken(elemento, linha_num)
                if token:
                    tokens.append(token)
    
    return tokens

def reconhecerToken(elemento: str, linha: int) -> Optional[Token]:

    # Tratar elemento vazio
    if not elemento:
        return None
    
    # ===== SÍMBOLOS DE AGRUPAMENTO =====
    if elemento == '(':
        return Token(Tipo_de_Token.ABRE_PARENTESES, elemento)
    elif elemento == ')':
        return Token(Tipo_de_Token.FECHA_PARENTESES, elemento)
    
    # ===== ESTRUTURAS DE CONTROLE =====
    elif elemento == 'IFELSE':
        return Token(Tipo_de_Token.IFELSE, elemento)
    elif elemento == 'WHILE':
        return Token(Tipo_de_Token.WHILE, elemento)
    elif elemento == 'FOR':
        return Token(Tipo_de_Token.FOR, elemento)
    
    # ===== COMANDOS ESPECIAIS =====
    elif elemento == 'RES':
        return Token(Tipo_de_Token.RES, elemento)
    
    # ===== OPERADORES RELACIONAIS =====
    elif elemento == '>=':
        return Token(Tipo_de_Token.MAIOR_IGUAL, elemento)
    elif elemento == '<=':
        return Token(Tipo_de_Token.MENOR_IGUAL, elemento)
    elif elemento == '==':
        return Token(Tipo_de_Token.IGUAL, elemento)
    elif elemento == '!=':
        return Token(Tipo_de_Token.DIFERENTE, elemento)
    elif elemento == '||':
        return Token(Tipo_de_Token.OR, elemento)
    elif elemento == '&&':
        return Token(Tipo_de_Token.AND, elemento)
    elif elemento == '>':
        return Token(Tipo_de_Token.MAIOR, elemento)
    elif elemento == '<':
        return Token(Tipo_de_Token.MENOR, elemento)
    
    # ===== OPERADORES ARITMÉTICOS =====
    elif elemento == '+':
        return Token(Tipo_de_Token.SOMA, elemento)
    elif elemento == '-':
        return Token(Tipo_de_Token.SUBTRACAO, elemento)
    elif elemento == '*':
        return Token(Tipo_de_Token.MULTIPLICACAO, elemento)
    elif elemento == '/':
        return Token(Tipo_de_Token.DIVISAO_INTEIRA, elemento)
    elif elemento == '|':
        return Token(Tipo_de_Token.DIVISAO_REAL, elemento)
    elif elemento == '%':
        return Token(Tipo_de_Token.RESTO, elemento)
    elif elemento == '^':
        return Token(Tipo_de_Token.POTENCIA, elemento)
    
    # ===== OPERADORES LÓGICOS =====
    elif elemento == '!':
        return Token(Tipo_de_Token.NOT, elemento)
    
    # ===== NÚMEROS =====
    else:
        # Verificar se é número (inteiro ou real)
        try:
            # Primeiro verificar se tem ponto decimal
            if '.' in elemento:
                # É um número real
                float(elemento)  # Validar que é um float válido
                return Token(Tipo_de_Token.NUMERO_REAL, elemento)
            else:
                # É um número inteiro
                int(elemento)  # Validar que é um int válido
                return Token(Tipo_de_Token.NUMERO_INTEIRO, elemento)
        except ValueError:
            # Se não é número, então é uma variável
            # Qualquer coisa que não seja um token específico é considerada variável
            return Token(Tipo_de_Token.VARIAVEL, elemento)

def validarTokens(tokens: List[Token]) -> bool:
    if not tokens:
        return False

    # Verificar se há parênteses balanceados
    contador_parenteses = 0
    for token in tokens:
        if token.tipo == Tipo_de_Token.ABRE_PARENTESES:
            contador_parenteses += 1
        elif token.tipo == Tipo_de_Token.FECHA_PARENTESES:
            contador_parenteses -= 1
            if contador_parenteses < 0:
                return False

    if contador_parenteses != 0:
        return False

    return True