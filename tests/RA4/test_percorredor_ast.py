"""
Testes Unitários para Percorredor AST

Testa a classe PercorredorAST para geração TAC a partir de AST atribuída.

Execute com: pytest tests/RA4/test_percorredor_ast.py -v
"""

import sys
import os
import pytest

# Adiciona raiz do projeto ao Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from src.RA4.functions.python.gerenciador_tac import GerenciadorTAC
from src.RA4.functions.python.percorredor_ast import PercorredorAST
from src.RA4.functions.python.instrucoes_tac import (
    TACAtribuicao,
    TACOperacaoBinaria,
)


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def criar_no_literal(valor: str, subtipo: str, numero_linha: int = 1):
    """Auxiliar para criar um nó literal."""
    return {
        "tipo_vertice": "LINHA",
        "tipo_inferido": None,
        "numero_linha": numero_linha,
        "filhos": [],
        "valor": valor,
        "subtipo": subtipo
    }


def criar_no_op_arit(operador: str, esquerdo, direito, numero_linha: int = 1):
    """Auxiliar para criar um nó de operação aritmética."""
    return {
        "tipo_vertice": "ARITH_OP",
        "tipo_inferido": None,
        "numero_linha": numero_linha,
        "filhos": [esquerdo, direito],
        "operador": operador
    }


def criar_no_linha(filho, numero_linha: int = 1, tipo_inferido: str = "int"):
    """Auxiliar para criar um nó wrapper LINHA."""
    return {
        "tipo_vertice": "LINHA",
        "tipo_inferido": tipo_inferido,
        "numero_linha": numero_linha,
        "filhos": [filho] if not isinstance(filho, list) else filho
    }


# ============================================================================
# TESTES DE FUNCIONALIDADE BÁSICA
# ============================================================================

def test_inicializacao_percorredor():
    """Testa que PercorredorAST inicializa corretamente."""
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    assert percorredor.gerenciador is gerenciador
    assert percorredor.instrucoes == []


def test_ast_vazia():
    """Testa processamento de AST vazia."""
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    ast = {"arvore_atribuida": []}
    instrucoes = percorredor.gerar_tac(ast)

    assert instrucoes == []


def test_linha_vazia():
    """Testa processamento de nó LINHA sem filhos."""
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    ast = {
        "arvore_atribuida": [
            {
                "tipo_vertice": "LINHA",
                "tipo_inferido": None,
                "numero_linha": 1,
                "filhos": []
            }
        ]
    }

    instrucoes = percorredor.gerar_tac(ast)
    assert instrucoes == []


# ============================================================================
# TESTES DE TRATAMENTO DE LITERAIS
# ============================================================================

def test_literal_inteiro_unico():
    """Testa processamento de um único literal inteiro."""
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    no_literal = criar_no_literal("5", "numero_inteiro", 1)
    no_linha = criar_no_linha(no_literal, 1, "int")

    ast = {"arvore_atribuida": [no_linha]}
    instrucoes = percorredor.gerar_tac(ast)

    assert len(instrucoes) == 1
    assert isinstance(instrucoes[0], TACAtribuicao)
    assert instrucoes[0].destino == "t0"
    assert instrucoes[0].origem == "5"
    assert instrucoes[0].linha == 1
    assert instrucoes[0].tipo_dado == "int"


def test_literal_real_unico():
    """Testa processamento de um único literal real (float)."""
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    no_literal = criar_no_literal("10.5", "numero_real", 2)
    no_linha = criar_no_linha(no_literal, 2, "real")

    ast = {"arvore_atribuida": [no_linha]}
    instrucoes = percorredor.gerar_tac(ast)

    assert len(instrucoes) == 1
    assert isinstance(instrucoes[0], TACAtribuicao)
    assert instrucoes[0].destino == "t0"
    assert instrucoes[0].origem == "10.5"
    assert instrucoes[0].tipo_dado == "real"


def test_referencia_variavel():
    """Testa que referências a variáveis não geram TAC de atribuição."""
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    no_var = criar_no_literal("X", "variavel", 1)

    resultado = percorredor._tratar_literal(no_var)

    # Referências a variáveis devem apenas retornar o nome da variável
    assert resultado == "X"
    # Nenhuma instrução TAC deve ser gerada
    assert len(percorredor.instrucoes) == 0


# ============================================================================
# TESTES DE OPERAÇÕES ARITMÉTICAS
# ============================================================================

def test_adicao_simples():
    """
    Testa adição simples: (5 3 +)

    TAC esperado:
        t0 = 5
        t1 = 3
        t2 = t0 + t1
    """
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    # Constrói AST para (5 3 +)
    esquerdo = criar_no_literal("5", "numero_inteiro", 1)
    direito = criar_no_literal("3", "numero_inteiro", 1)
    op_arit = criar_no_op_arit("+", esquerdo, direito, 1)
    linha = criar_no_linha(op_arit, 1, "int")

    ast = {"arvore_atribuida": [linha]}
    instrucoes = percorredor.gerar_tac(ast)

    assert len(instrucoes) == 3

    # t0 = 5
    assert isinstance(instrucoes[0], TACAtribuicao)
    assert instrucoes[0].destino == "t0"
    assert instrucoes[0].origem == "5"

    # t1 = 3
    assert isinstance(instrucoes[1], TACAtribuicao)
    assert instrucoes[1].destino == "t1"
    assert instrucoes[1].origem == "3"

    # t2 = t0 + t1
    assert isinstance(instrucoes[2], TACOperacaoBinaria)
    assert instrucoes[2].resultado == "t2"
    assert instrucoes[2].operando1 == "t0"
    assert instrucoes[2].operador == "+"
    assert instrucoes[2].operando2 == "t1"


@pytest.mark.parametrize("operador,val_esq,val_dir", [
    ("+", "5", "3"),
    ("-", "10", "7"),
    ("*", "4", "6"),
    ("/", "15", "3"),
    ("|", "10.0", "2.0"),  # Divisão real
    ("%", "23", "5"),  # Módulo
    ("^", "2", "8"),  # Potência
])
def test_todos_operadores_aritmeticos(operador, val_esq, val_dir):
    """Testa todos os operadores aritméticos: +, -, *, /, |, %, ^"""
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    # Determina subtipo baseado nos valores
    subtipo = "numero_real" if "." in val_esq else "numero_inteiro"

    esquerdo = criar_no_literal(val_esq, subtipo, 1)
    direito = criar_no_literal(val_dir, subtipo, 1)
    op_arit = criar_no_op_arit(operador, esquerdo, direito, 1)
    linha = criar_no_linha(op_arit, 1)

    ast = {"arvore_atribuida": [linha]}
    instrucoes = percorredor.gerar_tac(ast)

    assert len(instrucoes) == 3

    # Verifica se operação binária tem operador correto
    assert isinstance(instrucoes[2], TACOperacaoBinaria)
    assert instrucoes[2].operador == operador


def test_multiplicacao_numeros_reais():
    """
    Testa multiplicação com números reais: (10.5 2.0 *)

    TAC esperado:
        t0 = 10.5
        t1 = 2.0
        t2 = t0 * t1
    """
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    esquerdo = criar_no_literal("10.5", "numero_real", 2)
    direito = criar_no_literal("2.0", "numero_real", 2)
    op_arit = criar_no_op_arit("*", esquerdo, direito, 2)
    linha = criar_no_linha(op_arit, 2, "real")

    ast = {"arvore_atribuida": [linha]}
    instrucoes = percorredor.gerar_tac(ast)

    assert len(instrucoes) == 3
    assert instrucoes[0].tipo_dado == "real"
    assert instrucoes[1].tipo_dado == "real"
    assert instrucoes[2].operador == "*"


# ============================================================================
# TESTES DE VARIÁVEIS EM EXPRESSÕES
# ============================================================================

def test_adicao_com_variavel():
    """
    Testa adição com variável: (X 5 +)

    TAC esperado:
        # X é apenas referenciado, sem atribuição
        t0 = 5
        t1 = X + t0
    """
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    esquerdo = criar_no_literal("X", "variavel", 13)
    direito = criar_no_literal("5", "numero_inteiro", 13)
    op_arit = criar_no_op_arit("+", esquerdo, direito, 13)
    linha = criar_no_linha(op_arit, 13, "int")

    ast = {"arvore_atribuida": [linha]}
    instrucoes = percorredor.gerar_tac(ast)

    # Apenas 2 instruções: t0 = 5, depois t1 = X + t0
    assert len(instrucoes) == 2

    # t0 = 5
    assert isinstance(instrucoes[0], TACAtribuicao)
    assert instrucoes[0].origem == "5"

    # t1 = X + t0
    assert isinstance(instrucoes[1], TACOperacaoBinaria)
    assert instrucoes[1].operando1 == "X"
    assert instrucoes[1].operador == "+"
    assert instrucoes[1].operando2 == "t0"


def test_subtracao_com_variaveis():
    """
    Testa subtração com duas variáveis: (A X -)

    TAC esperado:
        t0 = A - X
    """
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    esquerdo = criar_no_literal("A", "variavel", 14)
    direito = criar_no_literal("X", "variavel", 14)
    op_arit = criar_no_op_arit("-", esquerdo, direito, 14)
    linha = criar_no_linha(op_arit, 14, "int")

    ast = {"arvore_atribuida": [linha]}
    instrucoes = percorredor.gerar_tac(ast)

    # Apenas 1 instrução: t0 = A - X
    assert len(instrucoes) == 1

    assert isinstance(instrucoes[0], TACOperacaoBinaria)
    assert instrucoes[0].operando1 == "A"
    assert instrucoes[0].operador == "-"
    assert instrucoes[0].operando2 == "X"


# ============================================================================
# TESTES DE EXPRESSÕES ANINHADAS
# ============================================================================

def test_expressao_aninhada():
    """
    Testa expressão aninhada: ((5 3 +) (2 4 *) *)

    Representa: (5+3) * (2*4)

    TAC esperado:
        t0 = 5
        t1 = 3
        t2 = t0 + t1
        t3 = 2
        t4 = 4
        t5 = t3 * t4
        t6 = t2 * t5
    """
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    # Constrói (5 3 +)
    esq_esq = criar_no_literal("5", "numero_inteiro", 22)
    esq_dir = criar_no_literal("3", "numero_inteiro", 22)
    esq_add = criar_no_op_arit("+", esq_esq, esq_dir, 22)

    # Constrói (2 4 *)
    dir_esq = criar_no_literal("2", "numero_inteiro", 22)
    dir_dir = criar_no_literal("4", "numero_inteiro", 22)
    dir_mul = criar_no_op_arit("*", dir_esq, dir_dir, 22)

    # Constrói multiplicação de nível superior
    topo_mul = criar_no_op_arit("*", esq_add, dir_mul, 22)
    linha = criar_no_linha(topo_mul, 22, "int")

    ast = {"arvore_atribuida": [linha]}
    instrucoes = percorredor.gerar_tac(ast)

    assert len(instrucoes) == 7

    # Verifica sequência
    assert instrucoes[0].destino == "t0"  # t0 = 5
    assert instrucoes[1].destino == "t1"  # t1 = 3
    assert instrucoes[2].resultado == "t2"  # t2 = t0 + t1
    assert instrucoes[3].destino == "t3"  # t3 = 2
    assert instrucoes[4].destino == "t4"  # t4 = 4
    assert instrucoes[5].resultado == "t5"  # t5 = t3 * t4
    assert instrucoes[6].resultado == "t6"  # t6 = t2 * t5

    # Verifica operação final
    assert instrucoes[6].operando1 == "t2"
    assert instrucoes[6].operador == "*"
    assert instrucoes[6].operando2 == "t5"


# ============================================================================
# TESTES DE MÚLTIPLAS LINHAS
# ============================================================================

def test_multiplas_linhas():
    """
    Testa processamento de múltiplas linhas em sequência.

    Linha 1: (5 3 +)
    Linha 2: (10 2 *)
    """
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    # Linha 1: (5 3 +)
    l1_esq = criar_no_literal("5", "numero_inteiro", 1)
    l1_dir = criar_no_literal("3", "numero_inteiro", 1)
    l1_op = criar_no_op_arit("+", l1_esq, l1_dir, 1)
    linha1 = criar_no_linha(l1_op, 1, "int")

    # Linha 2: (10 2 *)
    l2_esq = criar_no_literal("10", "numero_inteiro", 2)
    l2_dir = criar_no_literal("2", "numero_inteiro", 2)
    l2_op = criar_no_op_arit("*", l2_esq, l2_dir, 2)
    linha2 = criar_no_linha(l2_op, 2, "int")

    ast = {"arvore_atribuida": [linha1, linha2]}
    instrucoes = percorredor.gerar_tac(ast)

    # Linha 1 gera 3 instruções, Linha 2 gera 3 instruções
    assert len(instrucoes) == 6

    # Verifica números de linha preservados
    assert instrucoes[0].linha == 1
    assert instrucoes[1].linha == 1
    assert instrucoes[2].linha == 1
    assert instrucoes[3].linha == 2
    assert instrucoes[4].linha == 2
    assert instrucoes[5].linha == 2


# ============================================================================
# TESTES DE RASTREAMENTO DE NÚMERO DE LINHA
# ============================================================================

def test_preservacao_numero_linha():
    """Testa que números de linha são corretamente preservados no TAC."""
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    esquerdo = criar_no_literal("100", "numero_inteiro", 42)
    direito = criar_no_literal("50", "numero_inteiro", 42)
    op_arit = criar_no_op_arit("+", esquerdo, direito, 42)
    linha = criar_no_linha(op_arit, 42, "int")

    ast = {"arvore_atribuida": [linha]}
    instrucoes = percorredor.gerar_tac(ast)

    # Todas instruções devem ter número de linha 42
    assert all(instr.linha == 42 for instr in instrucoes)


# ============================================================================
# TESTES DE ESTATÍSTICAS
# ============================================================================

def test_estatisticas():
    """Testa que estatísticas são corretamente rastreadas."""
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    # Gera algum TAC
    esquerdo = criar_no_literal("5", "numero_inteiro", 1)
    direito = criar_no_literal("3", "numero_inteiro", 1)
    op_arit = criar_no_op_arit("+", esquerdo, direito, 1)
    linha = criar_no_linha(op_arit, 1, "int")

    ast = {"arvore_atribuida": [linha]}
    percorredor.gerar_tac(ast)

    stats = percorredor.obter_estatisticas()

    assert stats["total_instrucoes"] == 3
    assert stats["contador_temp"] == 3  # t0, t1, t2
    assert stats["contador_rotulo"] == 0  # Sem rótulos ainda


# ============================================================================
# TESTES COM SNIPPETS REAIS DE AST
# ============================================================================

def test_ast_real_linha_1():
    """
    Testa com snippet real de AST de arvore_atribuida.json - Linha 1.

    Linha 1: (5 3 +)
    """
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    ast = {
        "arvore_atribuida": [
            {
                "tipo_vertice": "LINHA",
                "tipo_inferido": "int",
                "numero_linha": 1,
                "filhos": [
                    {
                        "tipo_vertice": "ARITH_OP",
                        "tipo_inferido": None,
                        "numero_linha": 1,
                        "filhos": [
                            {
                                "tipo_vertice": "LINHA",
                                "tipo_inferido": None,
                                "numero_linha": 1,
                                "filhos": [],
                                "valor": "5",
                                "subtipo": "numero_inteiro"
                            },
                            {
                                "tipo_vertice": "LINHA",
                                "tipo_inferido": None,
                                "numero_linha": 1,
                                "filhos": [],
                                "valor": "3",
                                "subtipo": "numero_inteiro"
                            }
                        ],
                        "operador": "+"
                    }
                ]
            }
        ]
    }

    instrucoes = percorredor.gerar_tac(ast)

    assert len(instrucoes) == 3
    assert instrucoes[0].para_string() == "t0 = 5"
    assert instrucoes[1].para_string() == "t1 = 3"
    assert instrucoes[2].para_string() == "t2 = t0 + t1"


def test_ast_real_linha_2():
    """
    Testa com snippet real de AST - Linha 2: (10.5 2.0 *)
    """
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    ast = {
        "arvore_atribuida": [
            {
                "tipo_vertice": "LINHA",
                "tipo_inferido": "real",
                "numero_linha": 2,
                "filhos": [
                    {
                        "tipo_vertice": "ARITH_OP",
                        "tipo_inferido": None,
                        "numero_linha": 2,
                        "filhos": [
                            {
                                "tipo_vertice": "LINHA",
                                "tipo_inferido": None,
                                "numero_linha": 2,
                                "filhos": [],
                                "valor": "10.5",
                                "subtipo": "numero_real"
                            },
                            {
                                "tipo_vertice": "LINHA",
                                "tipo_inferido": None,
                                "numero_linha": 2,
                                "filhos": [],
                                "valor": "2.0",
                                "subtipo": "numero_real"
                            }
                        ],
                        "operador": "*"
                    }
                ]
            }
        ]
    }

    instrucoes = percorredor.gerar_tac(ast)

    assert len(instrucoes) == 3
    assert instrucoes[0].tipo_dado == "real"
    assert instrucoes[1].tipo_dado == "real"
    assert instrucoes[2].para_string() == "t2 = t0 * t1"


# ============================================================================
# TESTES DE VERIFICAÇÃO PÓS-ORDEM
# ============================================================================

def test_percurso_pos_ordem():
    """
    Verifica que percurso é realmente pós-ordem (filhos antes de pais).

    Para (5 3 +), a ordem deve ser:
    1. Visita 5 (filho esquerdo)
    2. Visita 3 (filho direito)
    3. Visita + (pai)
    """
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    esquerdo = criar_no_literal("5", "numero_inteiro", 1)
    direito = criar_no_literal("3", "numero_inteiro", 1)
    op_arit = criar_no_op_arit("+", esquerdo, direito, 1)
    linha = criar_no_linha(op_arit, 1, "int")

    ast = {"arvore_atribuida": [linha]}
    instrucoes = percorredor.gerar_tac(ast)

    # Pós-ordem: filhos (5, 3) processados antes do pai (+)
    # Então devemos ter: t0=5, t1=3, DEPOIS t2=t0+t1
    assert instrucoes[0].para_string() == "t0 = 5"  # Filho esquerdo
    assert instrucoes[1].para_string() == "t1 = 3"  # Filho direito
    assert instrucoes[2].para_string() == "t2 = t0 + t1"  # Pai


# ============================================================================
# FIXTURES PYTEST
# ============================================================================

@pytest.fixture
def percorredor_novo():
    """Fixture fornecendo um PercorredorAST novo com GerenciadorTAC novo."""
    gerenciador = GerenciadorTAC()
    return PercorredorAST(gerenciador)


def test_com_fixture_percorredor_novo(percorredor_novo):
    """Testa usando fixture percorredor_novo."""
    assert percorredor_novo.instrucoes == []
    assert percorredor_novo.gerenciador.obter_contador_temp() == 0


# ============================================================================
# TESTES DE OPERAÇÕES DE COMPARAÇÃO E LÓGICAS
# ============================================================================

def test_stub_operacao_comparacao():
    """
    Testa stub de operação de comparação (Issue 1.5).

    Linha 7: (5.5 3.2 >)
    """
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    ast = {
        "arvore_atribuida": [
            {
                "tipo_vertice": "LINHA",
                "tipo_inferido": "boolean",
                "numero_linha": 7,
                "filhos": [
                    {
                        "tipo_vertice": "COMP_OP",
                        "tipo_inferido": None,
                        "numero_linha": 7,
                        "filhos": [
                            {
                                "tipo_vertice": "LINHA",
                                "tipo_inferido": None,
                                "numero_linha": 7,
                                "filhos": [],
                                "valor": "5.5",
                                "subtipo": "numero_real"
                            },
                            {
                                "tipo_vertice": "LINHA",
                                "tipo_inferido": None,
                                "numero_linha": 7,
                                "filhos": [],
                                "valor": "3.2",
                                "subtipo": "numero_real"
                            }
                        ],
                        "operador": ">"
                    }
                ]
            }
        ]
    }

    instrucoes = percorredor.gerar_tac(ast)

    # Stub ainda deve gerar TAC
    assert len(instrucoes) == 3
    assert instrucoes[2].operador == ">"
    assert instrucoes[2].tipo_dado == "boolean"


def test_stub_operacao_logica():
    """
    Testa stub de operação lógica (Issue 1.5).
    """
    gerenciador = GerenciadorTAC()
    percorredor = PercorredorAST(gerenciador)

    # Simples (true false &&)
    esquerdo = criar_no_literal("1", "numero_inteiro", 8)
    direito = criar_no_literal("0", "numero_inteiro", 8)

    op_logica = {
        "tipo_vertice": "LOGIC_OP",
        "tipo_inferido": None,
        "numero_linha": 8,
        "filhos": [esquerdo, direito],
        "operador": "&&"
    }

    linha = criar_no_linha(op_logica, 8, "boolean")
    ast = {"arvore_atribuida": [linha]}

    instrucoes = percorredor.gerar_tac(ast)

    # Stub deve gerar TAC
    assert len(instrucoes) == 3
    assert instrucoes[2].operador == "&&"
