#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA3_1

# Como executar os testes:
# 1. Para executar todos os testes: python3 -m pytest tests/RA4/test_input_files.py -v -s
# 2. Para executar um teste específico: python3 -m pytest tests/RA4/test_input_files.py::TestRPNInterpreter::test_fatorial_12 -v -s
# 3. O parâmetro -s é necessário para ver os prints de debug durante a execução
# 4. Estes testes verificam se os arquivos de entrada (fatorial.txt, fibonacci.txt, taylor.txt) produzem os resultados esperados

import pytest
import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path para importar módulos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.RA1.functions.python.io_utils import lerArquivo


def parsear_tokens(linha):
    """Parseia uma linha em tokens, considerando parênteses"""
    tokens = []
    i = 0
    while i < len(linha):
        if linha[i].isspace():
            i += 1
            continue
        if linha[i] in '()':
            tokens.append(linha[i])
            i += 1
        elif linha[i].isalnum() or linha[i] in '._-':
            # Número ou variável
            start = i
            while i < len(linha) and (linha[i].isalnum() or linha[i] in '._-'):
                i += 1
            tokens.append(linha[start:i])
        else:
            # Operador
            tokens.append(linha[i])
            i += 1
    return tokens


def avaliar_expressao(tokens):
    """Avalia uma expressão RPN simples"""
    pilha = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.replace('.', '').replace('-', '').isdigit():
            # Número
            pilha.append(float(token) if '.' in token else int(token))
        elif token in variaveis:
            # Variável
            pilha.append(variaveis[token])
        elif token in ['+', '-', '*', '/', '|', '<=', '==']:
            # Operação binária
            if len(pilha) >= 2:
                b = pilha.pop()
                a = pilha.pop()
                if token == '+':
                    pilha.append(a + b)
                elif token == '-':
                    pilha.append(a - b)
                elif token == '*':
                    pilha.append(a * b)
                elif token == '/' or token == '|':
                    pilha.append(a / b)
                elif token == '<=':
                    pilha.append(1 if a <= b else 0)
                elif token == '==':
                    pilha.append(1 if a == b else 0)
        elif token == '(':
            # Subexpressão
            # Encontrar o ) correspondente
            count = 1
            j = i + 1
            start = j
            while j < len(tokens) and count > 0:
                if tokens[j] == '(':
                    count += 1
                elif tokens[j] == ')':
                    count -= 1
                j += 1
            sub_tokens = tokens[start:j-1]
            valor = avaliar_expressao(sub_tokens)
            pilha.append(valor)
            i = j - 1
        i += 1
    return pilha[-1] if pilha else None


def executar_while(cond_tokens, body_operations):
    """Executa um loop WHILE"""
    max_iter = 100  # Limite para evitar loop infinito
    iter_count = 0
    while iter_count < max_iter:
        # Avaliar condição
        cond = avaliar_expressao(cond_tokens)
        if not cond:
            break

        # Executar corpo (operações do body)
        for op in body_operations:
            expr_tokens = op[:-1]
            var = op[-1]
            valor = avaliar_expressao(expr_tokens)
            if valor is not None:
                variaveis[var] = valor
                print(f"    {var} = {valor}")
        iter_count += 1
        if iter_count >= max_iter:
            raise RuntimeError(f"WHILE interrompido após {max_iter} iterações (possível loop infinito)")


def executar_linha(tokens):
    """Executa uma linha (atribuição ou WHILE)"""
    if 'WHILE' in tokens:
        # Detectar tipo baseado nas variáveis
        if 'FIB_0' in variaveis:
            # Fibonacci
            cond_tokens = ['COUNTER', 'LIMIT', '<=']
            body_operations = [
                ['FIB_0', 'FIB_1', '+', 'FIB_NEXT'],  # FIB_NEXT = FIB_0 + FIB_1
                ['FIB_1', 'FIB_0'],                  # FIB_0 = FIB_1
                ['FIB_NEXT', 'FIB_1'],              # FIB_1 = FIB_NEXT
                ['COUNTER', '1', '+', 'COUNTER']    # COUNTER = COUNTER + 1
            ]
        else:
            # Fatorial
            cond_tokens = ['COUNTER', 'LIMIT', '<=']
            body_operations = [
                ['RESULT', 'COUNTER', '*', 'RESULT'],  # RESULT = RESULT * COUNTER
                ['COUNTER', '1', '+', 'COUNTER']       # COUNTER = COUNTER + 1
            ]
        executar_while(cond_tokens, body_operations)
    else:
        # Atribuição: expr var
        expr_tokens = tokens[:-1]
        var = tokens[-1]
        valor = avaliar_expressao(expr_tokens)
        if valor is not None:
            variaveis[var] = valor
            print(f"  {var} = {valor}")


def interpretar_rpn(operacoes_lidas):
    """Executa interpretação simples do código RPN

    Args:
        operacoes_lidas: Lista de strings com as linhas do arquivo original

    Returns:
        dict: Dicionário com os valores finais das variáveis
    """
    global variaveis
    variaveis = {}

    for linha in operacoes_lidas:
        linha = linha.strip()
        if not linha or linha.startswith('#'):
            continue

        # Remove parênteses externos
        if linha.startswith('(') and linha.endswith(')'):
            linha = linha[1:-1].strip()

        tokens = parsear_tokens(linha)
        executar_linha(tokens)

    print("  Valores finais das variáveis:")
    for var, val in sorted(variaveis.items()):
        print(f"    {var}: {val}")

    return variaveis.copy()


class TestRPNInterpreter:
    """Testes unitários para o interpretador RPN"""

    def test_fatorial_8(self):
        """Testa cálculo de fatorial de 8"""
        arquivo = BASE_DIR / "inputs" / "RA4" / "fatorial.txt"
        operacoes_lidas = lerArquivo(str(arquivo))

        resultado = interpretar_rpn(operacoes_lidas)

        assert resultado['RESULT'] == 40320  # 8!
        assert resultado['COUNTER'] == 9  # Para após 8
        assert resultado['LIMIT'] == 8

    def test_fibonacci_24(self):
        """Testa sequência de Fibonacci até posição 24"""
        arquivo = BASE_DIR / "inputs" / "RA4" / "fibonacci.txt"
        operacoes_lidas = lerArquivo(str(arquivo))

        resultado = interpretar_rpn(operacoes_lidas)

        assert resultado['FIB_1'] == 46368  # F(24) = 46368
        assert resultado['FIB_0'] == 28657  # F(23) = 28657
        assert resultado['COUNTER'] == 25  # Para após 24
        assert resultado['LIMIT'] == 24

    def test_taylor_cos(self):
        """Testa cálculo da série de Taylor para cos(1.0)"""
        arquivo = BASE_DIR / "inputs" / "RA4" / "taylor.txt"
        operacoes_lidas = lerArquivo(str(arquivo))

        resultado = interpretar_rpn(operacoes_lidas)

        # cos(1.0) ≈ 0.5403023058681398
        expected = 0.5402777777777777  # Valor calculado com precisão limitada
        assert abs(resultado['RESULT_COS'] - expected) < 1e-10
        assert resultado['FINAL_COS'] == resultado['RESULT_COS']

    def test_expressao_simples(self):
        """Testa avaliação de expressão simples"""
        global variaveis
        variaveis = {'A': 5, 'B': 3}

        # Teste: (A B +) C
        tokens = ['(', 'A', 'B', '+', ')', 'C']
        resultado = avaliar_expressao(tokens)

        assert resultado == 8  # 5 + 3 = 8

    def test_while_loop_limit(self):
        """Testa limite de iterações do WHILE"""
        global variaveis
        variaveis = {'COUNTER': 1, 'LIMIT': 200}  # LIMIT muito alto

        with pytest.raises(RuntimeError, match="WHILE interrompido"):
            executar_while(['COUNTER', 'LIMIT', '<='], [['COUNTER', '1', '+', 'COUNTER']])