"""
Suite de testes para classes de instrução TAC

Este arquivo testa todos os tipos de instrução TAC para garantir que:
1. Geram representação string correta (para_string)
2. Geram representação JSON correta (para_dicionario)
3. Identificam corretamente variáveis definidas (define_variavel)
4. Identificam corretamente variáveis usadas (usa_variaveis)

Execute com pytest:
    pytest tests/RA4/test_instrucoes_tac.py -v

Ou execute todos os testes RA4:
    pytest tests/RA4/ -v
"""

import sys
import os
import json
import pytest

# Adiciona raiz do projeto ao path para permitir imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Importa classes de instrução TAC
from src.RA4.functions.python.instrucoes_tac import (
    InstrucaoTAC,
    TACAtribuicao,
    TACCopia,
    TACOperacaoBinaria,
    TACOperacaoUnaria,
    TACRotulo,
    TACDesvio,
    TACSeDesvio,
    TACSeNaoDesvio,
    TACLeituraMemoria,
    TACEscritaMemoria,
    TACChamada,
    TACRetorno,
    instrucao_de_dicionario,
)


# ============================================================================
# TESTE: INSTRUÇÕES DE ATRIBUIÇÃO
# ============================================================================

def test_atribuicao_com_literal():
    """Testa TACAtribuicao com valor literal"""
    instr = TACAtribuicao("t0", "5", linha=1, tipo_dado="int")

    assert instr.para_string() == "t0 = 5"
    assert instr.define_variavel == "t0"
    assert instr.usa_variaveis == []

    # Testa serialização JSON
    dados = instr.para_dicionario()
    assert dados["tipo"] == "atribuicao"
    assert dados["destino"] == "t0"
    assert dados["origem"] == "5"
    assert dados["linha"] == 1
    assert dados["tipo_dado"] == "int"


def test_atribuicao_com_variavel():
    """Testa TACAtribuicao com variável"""
    instr = TACAtribuicao("t1", "X", linha=2, tipo_dado="int")

    assert instr.para_string() == "t1 = X"
    assert instr.define_variavel == "t1"
    assert instr.usa_variaveis == ["X"]


def test_instrucao_copia():
    """Testa instrução TACCopia"""
    instr = TACCopia("a", "b", linha=3, tipo_dado="int")

    assert instr.para_string() == "a = b"
    assert instr.define_variavel == "a"
    assert instr.usa_variaveis == ["b"]


# ============================================================================
# TESTE: INSTRUÇÕES DE OPERAÇÃO
# ============================================================================

def test_op_binaria_com_temporarios():
    """Testa TACOperacaoBinaria com variáveis temporárias"""
    instr = TACOperacaoBinaria("t2", "t0", "+", "t1", linha=3, tipo_dado="int")

    assert instr.para_string() == "t2 = t0 + t1"
    assert instr.define_variavel == "t2"
    assert instr.usa_variaveis == ["t0", "t1"]


def test_op_binaria_comparacao():
    """Testa TACOperacaoBinaria com operador de comparação"""
    instr = TACOperacaoBinaria("t3", "X", ">", "5", linha=4, tipo_dado="boolean")

    assert instr.para_string() == "t3 = X > 5"
    assert instr.define_variavel == "t3"
    assert instr.usa_variaveis == ["X"]  # "5" é constante, não incluída


def test_op_binaria_divisao_real():
    """Testa TACOperacaoBinaria com divisão real"""
    instr = TACOperacaoBinaria("t4", "10.5", "|", "2.0", linha=5, tipo_dado="real")

    assert instr.para_string() == "t4 = 10.5 | 2.0"
    assert instr.define_variavel == "t4"
    assert instr.usa_variaveis == []  # Ambos operandos são constantes


def test_op_binaria_todos_operadores():
    """Testa TACOperacaoBinaria com todos os operadores suportados"""
    operadores = ["+", "-", "*", "/", "|", "%", "^", ">", "<", ">=", "<=", "==", "!=", "&&", "||"]

    for op in operadores:
        instr = TACOperacaoBinaria("t0", "a", op, "b", linha=1)
        assert op in instr.para_string()


def test_op_unaria_negacao():
    """Testa TACOperacaoUnaria com negação"""
    instr = TACOperacaoUnaria("t5", "-", "X", linha=6, tipo_dado="int")

    assert instr.para_string() == "t5 = -X"
    assert instr.define_variavel == "t5"
    assert instr.usa_variaveis == ["X"]


def test_op_unaria_not_logico():
    """Testa TACOperacaoUnaria com NOT lógico"""
    instr = TACOperacaoUnaria("t6", "!", "condicao", linha=7, tipo_dado="boolean")

    assert instr.para_string() == "t6 = !condicao"
    assert instr.define_variavel == "t6"
    assert instr.usa_variaveis == ["condicao"]


# ============================================================================
# TESTE: INSTRUÇÕES DE FLUXO DE CONTROLE
# ============================================================================

def test_rotulo():
    """Testa instrução TACRotulo"""
    rotulo = TACRotulo("L1", linha=8)

    assert rotulo.para_string() == "L1:"
    assert rotulo.define_variavel is None
    assert rotulo.usa_variaveis == []


def test_desvio():
    """Testa instrução TACDesvio"""
    desvio = TACDesvio("L1", linha=9)

    assert desvio.para_string() == "goto L1"
    assert desvio.define_variavel is None
    assert desvio.usa_variaveis == []


def test_se_desvio():
    """Testa instrução TACSeDesvio"""
    se_desvio = TACSeDesvio("t5", "L2", linha=10)

    assert se_desvio.para_string() == "if t5 goto L2"
    assert se_desvio.define_variavel is None
    assert se_desvio.usa_variaveis == ["t5"]


def test_se_nao_desvio():
    """Testa instrução TACSeNaoDesvio"""
    se_nao = TACSeNaoDesvio("t6", "L3", linha=11)

    assert se_nao.para_string() == "ifFalse t6 goto L3"
    assert se_nao.define_variavel is None
    assert se_nao.usa_variaveis == ["t6"]


def test_se_desvio_com_condicao_constante():
    """Testa TACSeDesvio com condição constante"""
    se_desvio = TACSeDesvio("0", "L1", linha=12)

    assert se_desvio.para_string() == "if 0 goto L1"
    assert se_desvio.usa_variaveis == []  # "0" é constante


# ============================================================================
# TESTE: INSTRUÇÕES DE ACESSO À MEMÓRIA
# ============================================================================

def test_leitura_memoria():
    """Testa instrução TACLeituraMemoria"""
    leitura_mem = TACLeituraMemoria("t7", "X", linha=12, tipo_dado="int")

    assert leitura_mem.para_string() == "t7 = MEM[X]"
    assert leitura_mem.define_variavel == "t7"
    assert leitura_mem.usa_variaveis == ["X"]

    # Testa serialização JSON
    dados = leitura_mem.para_dicionario()
    assert dados["tipo"] == "leitura_memoria"
    assert dados["resultado"] == "t7"
    assert dados["endereco"] == "X"


def test_escrita_memoria():
    """Testa instrução TACEscritaMemoria"""
    escrita_mem = TACEscritaMemoria("Y", "t8", linha=13, tipo_dado="int")

    assert escrita_mem.para_string() == "MEM[Y] = t8"
    assert escrita_mem.define_variavel == "Y"
    assert escrita_mem.usa_variaveis == ["t8"]


# ============================================================================
# TESTE: INSTRUÇÕES DE FUNÇÃO
# ============================================================================

def test_chamada():
    """Testa instrução TACChamada"""
    chamada = TACChamada("t9", "fatorial", 1, linha=14, tipo_dado="int")

    assert chamada.para_string() == "t9 = call fatorial, 1"
    assert chamada.define_variavel == "t9"
    assert chamada.usa_variaveis == []


def test_retorno():
    """Testa instrução TACRetorno"""
    ret = TACRetorno("t10", linha=15, tipo_dado="int")

    assert ret.para_string() == "return t10"
    assert ret.define_variavel is None
    assert ret.usa_variaveis == ["t10"]


def test_retorno_com_constante():
    """Testa TACRetorno com valor constante"""
    ret = TACRetorno("42", linha=16, tipo_dado="int")

    assert ret.para_string() == "return 42"
    assert ret.usa_variaveis == []  # "42" é constante


# ============================================================================
# TESTE: EXEMPLOS DE PROGRAMA COMPLETO
# ============================================================================

def test_programa_tac_completo():
    """Testa geração de programa TAC completo para: (5 3 +)"""
    instrucoes = [
        TACAtribuicao("t0", "5", linha=1, tipo_dado="int"),
        TACAtribuicao("t1", "3", linha=1, tipo_dado="int"),
        TACOperacaoBinaria("t2", "t0", "+", "t1", linha=1, tipo_dado="int"),
    ]

    # Verifica representação string
    assert instrucoes[0].para_string() == "t0 = 5"
    assert instrucoes[1].para_string() == "t1 = 3"
    assert instrucoes[2].para_string() == "t2 = t0 + t1"

    # Verifica serialização JSON
    tac_json = {"instrucoes": [instr.para_dicionario() for instr in instrucoes]}
    assert len(tac_json["instrucoes"]) == 3
    assert tac_json["instrucoes"][0]["tipo"] == "atribuicao"
    assert tac_json["instrucoes"][2]["tipo"] == "operacao_binaria"


def test_analise_variaveis():
    """Testa análise de uso de variáveis"""
    instrucoes = [
        TACAtribuicao("t0", "5", linha=1, tipo_dado="int"),
        TACAtribuicao("t1", "3", linha=1, tipo_dado="int"),
        TACOperacaoBinaria("t2", "t0", "+", "t1", linha=1, tipo_dado="int"),
    ]

    todas_definidas = set()
    todas_usadas = set()

    for instr in instrucoes:
        if instr.define_variavel:
            todas_definidas.add(instr.define_variavel)
        todas_usadas.update(instr.usa_variaveis)

    assert todas_definidas == {"t0", "t1", "t2"}
    assert todas_usadas == {"t0", "t1"}
    assert todas_definidas - todas_usadas == {"t2"}  # t2 é definida mas nunca usada (código morto)


# ============================================================================
# TESTE: CENÁRIOS DE OTIMIZAÇÃO
# ============================================================================

def test_deteccao_constant_folding():
    """Testa detecção de oportunidades de constant folding"""
    # Esta instrução pode ser folded em tempo de compilação: 2 + 3 = 5
    instr = TACOperacaoBinaria("t0", "2", "+", "3", linha=1, tipo_dado="int")

    # Ambos operandos são constantes
    assert InstrucaoTAC.eh_constante("2")
    assert InstrucaoTAC.eh_constante("3")
    assert instr.usa_variaveis == []  # Nenhuma variável usada


def test_deteccao_codigo_morto():
    """Testa detecção de código morto"""
    instrucoes = [
        TACAtribuicao("t0", "2", linha=1, tipo_dado="int"),
        TACAtribuicao("t1", "3", linha=2, tipo_dado="int"),
        TACOperacaoBinaria("t2", "t0", "+", "t1", linha=3, tipo_dado="int"),
        TACAtribuicao("t3", "10", linha=4, tipo_dado="int"),  # Morto: t3 nunca usado
        TACOperacaoBinaria("t4", "t2", "*", "2", linha=5, tipo_dado="int"),
    ]

    vars_definidas = {}
    vars_usadas = set()

    for i, instr in enumerate(instrucoes):
        if instr.define_variavel:
            vars_definidas[instr.define_variavel] = i
        vars_usadas.update(instr.usa_variaveis)

    # t3 é definida mas nunca usada
    assert "t3" in vars_definidas
    assert "t3" not in vars_usadas


# ============================================================================
# TESTE: SERIALIZAÇÃO JSON
# ============================================================================

def test_roundtrip_serializacao():
    """Testa serialização e desserialização JSON"""
    original = TACOperacaoBinaria("t5", "X", "+", "10", linha=20, tipo_dado="int")

    # Serializa para dict
    dados = original.para_dicionario()

    # Desserializa de volta
    restaurado = instrucao_de_dicionario(dados)

    # Verifica se correspondem
    assert original.para_string() == restaurado.para_string()
    assert original.define_variavel == restaurado.define_variavel
    assert original.usa_variaveis == restaurado.usa_variaveis


def test_serializacao_todos_tipos_instrucao():
    """Testa serialização para todos os tipos de instrução"""
    instrucoes = [
        TACAtribuicao("t0", "5", linha=1),
        TACCopia("a", "b", linha=2),
        TACOperacaoBinaria("t1", "a", "+", "b", linha=3),
        TACOperacaoUnaria("t2", "-", "c", linha=4),
        TACRotulo("L1", linha=5),
        TACDesvio("L1", linha=6),
        TACSeDesvio("t3", "L2", linha=7),
        TACSeNaoDesvio("t4", "L3", linha=8),
        TACLeituraMemoria("t5", "X", linha=9),
        TACEscritaMemoria("Y", "t6", linha=10),
        TACChamada("t7", "func", 2, linha=11),
        TACRetorno("t8", linha=12),
    ]

    for original in instrucoes:
        dados = original.para_dicionario()
        restaurado = instrucao_de_dicionario(dados)
        assert original.para_string() == restaurado.para_string()


# ============================================================================
# TESTE: MÉTODOS AUXILIARES
# ============================================================================

def test_metodo_eh_constante():
    """Testa o método estático eh_constante"""
    # Constantes inteiras
    assert InstrucaoTAC.eh_constante("0")
    assert InstrucaoTAC.eh_constante("42")
    assert InstrucaoTAC.eh_constante("-5")

    # Constantes float
    assert InstrucaoTAC.eh_constante("3.14")
    assert InstrucaoTAC.eh_constante("10.5")
    assert InstrucaoTAC.eh_constante("-2.718")

    # Não constantes (variáveis)
    assert not InstrucaoTAC.eh_constante("X")
    assert not InstrucaoTAC.eh_constante("temp")
    assert not InstrucaoTAC.eh_constante("t0")


def test_propriedade_define_variavel():
    """Testa propriedade define_variavel para todos os tipos de instrução"""
    # Devem definir variáveis
    assert TACAtribuicao("t0", "5", linha=1).define_variavel == "t0"
    assert TACOperacaoBinaria("t1", "a", "+", "b", linha=1).define_variavel == "t1"
    assert TACOperacaoUnaria("t2", "-", "c", linha=1).define_variavel == "t2"
    assert TACLeituraMemoria("t3", "X", linha=1).define_variavel == "t3"
    assert TACEscritaMemoria("Y", "t4", linha=1).define_variavel == "Y"
    assert TACChamada("t5", "func", 1, linha=1).define_variavel == "t5"

    # NÃO devem definir variáveis
    assert TACRotulo("L1", linha=1).define_variavel is None
    assert TACDesvio("L1", linha=1).define_variavel is None
    assert TACSeDesvio("t0", "L1", linha=1).define_variavel is None
    assert TACSeNaoDesvio("t0", "L1", linha=1).define_variavel is None
    assert TACRetorno("t0", linha=1).define_variavel is None


def test_propriedade_usa_variaveis():
    """Testa propriedade usa_variaveis filtra corretamente constantes"""
    # Deve incluir apenas variáveis
    instr1 = TACOperacaoBinaria("t0", "X", "+", "5", linha=1)
    assert instr1.usa_variaveis == ["X"]  # "5" é constante, excluída

    instr2 = TACOperacaoBinaria("t1", "10", "*", "20", linha=1)
    assert instr2.usa_variaveis == []  # Ambas constantes, lista vazia

    instr3 = TACOperacaoBinaria("t2", "a", "-", "b", linha=1)
    assert instr3.usa_variaveis == ["a", "b"]  # Ambas variáveis


# ============================================================================
# MARCADORES E PARAMETRIZAÇÃO PYTEST
# ============================================================================

@pytest.mark.parametrize("operador", ["+", "-", "*", "/", "|", "%", "^"])
def test_operadores_aritmeticos(operador):
    """Testa todos os operadores aritméticos"""
    instr = TACOperacaoBinaria("t0", "a", operador, "b", linha=1, tipo_dado="int")
    assert operador in instr.para_string()
    assert instr.define_variavel == "t0"
    assert instr.usa_variaveis == ["a", "b"]


@pytest.mark.parametrize("operador", [">", "<", ">=", "<=", "==", "!="])
def test_operadores_comparacao(operador):
    """Testa todos os operadores de comparação"""
    instr = TACOperacaoBinaria("t0", "a", operador, "b", linha=1, tipo_dado="boolean")
    assert operador in instr.para_string()
    assert instr.define_variavel == "t0"


@pytest.mark.parametrize("operador", ["&&", "||"])
def test_operadores_logicos(operador):
    """Testa operadores lógicos"""
    instr = TACOperacaoBinaria("t0", "a", operador, "b", linha=1, tipo_dado="boolean")
    assert operador in instr.para_string()


# ============================================================================
# FIXTURES PYTEST (para uso futuro)
# ============================================================================

@pytest.fixture
def programa_tac_exemplo():
    """Fixture fornecendo um programa TAC de exemplo"""
    return [
        TACAtribuicao("t0", "5", linha=1, tipo_dado="int"),
        TACAtribuicao("t1", "3", linha=1, tipo_dado="int"),
        TACOperacaoBinaria("t2", "t0", "+", "t1", linha=1, tipo_dado="int"),
    ]


def test_com_fixture(programa_tac_exemplo):
    """Exemplo de teste usando fixture pytest"""
    assert len(programa_tac_exemplo) == 3
    assert programa_tac_exemplo[0].para_string() == "t0 = 5"
