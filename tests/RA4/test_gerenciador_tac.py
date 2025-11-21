"""
Testes Unitários para Gerenciador TAC

Testa a classe GerenciadorTAC para geração de variáveis temporárias e rótulos.

Execute com: pytest tests/RA4/test_gerenciador_tac.py -v
"""

import sys
import os
import pytest

# Adiciona raiz do projeto ao Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from src.RA4.functions.python.gerenciador_tac import GerenciadorTAC


# ============================================================================
# TESTES DE FUNCIONALIDADE BÁSICA
# ============================================================================

def test_inicializacao_gerenciador_tac():
    """Testa que GerenciadorTAC inicializa com contadores em 0."""
    gerenciador = GerenciadorTAC()

    assert gerenciador.obter_contador_temp() == 0
    assert gerenciador.obter_contador_rotulo() == 0


def test_primeira_temp_e_t0():
    """Testa que a primeira variável temporária é t0."""
    gerenciador = GerenciadorTAC()
    temp = gerenciador.nova_temp()

    assert temp == "t0"
    assert gerenciador.obter_contador_temp() == 1


def test_primeiro_rotulo_e_L0():
    """Testa que o primeiro rótulo é L0."""
    gerenciador = GerenciadorTAC()
    rotulo = gerenciador.novo_rotulo()

    assert rotulo == "L0"
    assert gerenciador.obter_contador_rotulo() == 1


# ============================================================================
# TESTES DE GERAÇÃO DE VARIÁVEIS TEMPORÁRIAS
# ============================================================================

def test_sequencia_temp():
    """Testa que temporários são gerados na sequência correta: t0, t1, t2, ..."""
    gerenciador = GerenciadorTAC()

    temps = [gerenciador.nova_temp() for _ in range(10)]
    esperado = [f"t{i}" for i in range(10)]

    assert temps == esperado


def test_unicidade_temp():
    """Testa que cada chamada a nova_temp() retorna uma variável única."""
    gerenciador = GerenciadorTAC()

    temps = [gerenciador.nova_temp() for _ in range(100)]

    # Verifica se todos temps são únicos
    assert len(temps) == len(set(temps))
    # Verifica se estão na sequência correta
    assert temps == [f"t{i}" for i in range(100)]


@pytest.mark.parametrize("quantidade", [1, 5, 10, 50, 100])
def test_contagem_geracao_temp(quantidade):
    """Testa que contador de temp rastreia corretamente o número de temps gerados."""
    gerenciador = GerenciadorTAC()

    for _ in range(quantidade):
        gerenciador.nova_temp()

    assert gerenciador.obter_contador_temp() == quantidade


# ============================================================================
# TESTES DE GERAÇÃO DE RÓTULOS
# ============================================================================

def test_sequencia_rotulo():
    """Testa que rótulos são gerados na sequência correta: L0, L1, L2, ..."""
    gerenciador = GerenciadorTAC()

    rotulos = [gerenciador.novo_rotulo() for _ in range(10)]
    esperado = [f"L{i}" for i in range(10)]

    assert rotulos == esperado


def test_unicidade_rotulo():
    """Testa que cada chamada a novo_rotulo() retorna um rótulo único."""
    gerenciador = GerenciadorTAC()

    rotulos = [gerenciador.novo_rotulo() for _ in range(100)]

    # Verifica se todos rótulos são únicos
    assert len(rotulos) == len(set(rotulos))
    # Verifica se estão na sequência correta
    assert rotulos == [f"L{i}" for i in range(100)]


@pytest.mark.parametrize("quantidade", [1, 5, 10, 50, 100])
def test_contagem_geracao_rotulo(quantidade):
    """Testa que contador de rótulo rastreia corretamente o número de rótulos gerados."""
    gerenciador = GerenciadorTAC()

    for _ in range(quantidade):
        gerenciador.novo_rotulo()

    assert gerenciador.obter_contador_rotulo() == quantidade


# ============================================================================
# TESTES DE GERAÇÃO MISTA
# ============================================================================

def test_temps_e_rotulos_independentes():
    """Testa que contadores de temp e rótulo são independentes."""
    gerenciador = GerenciadorTAC()

    # Gera alguns temps
    t0 = gerenciador.nova_temp()
    t1 = gerenciador.nova_temp()

    # Gera alguns rótulos
    l0 = gerenciador.novo_rotulo()
    l1 = gerenciador.novo_rotulo()

    # Gera mais temps
    t2 = gerenciador.nova_temp()

    # Gera mais rótulos
    l2 = gerenciador.novo_rotulo()

    assert t0 == "t0"
    assert t1 == "t1"
    assert t2 == "t2"
    assert l0 == "L0"
    assert l1 == "L1"
    assert l2 == "L2"
    assert gerenciador.obter_contador_temp() == 3
    assert gerenciador.obter_contador_rotulo() == 3


def test_geracao_intercalada():
    """Testa geração de temps e rótulos de forma intercalada."""
    gerenciador = GerenciadorTAC()

    resultados = []
    resultados.append(gerenciador.nova_temp())   # t0
    resultados.append(gerenciador.novo_rotulo())  # L0
    resultados.append(gerenciador.nova_temp())   # t1
    resultados.append(gerenciador.novo_rotulo())  # L1
    resultados.append(gerenciador.nova_temp())   # t2
    resultados.append(gerenciador.novo_rotulo())  # L2

    assert resultados == ["t0", "L0", "t1", "L1", "t2", "L2"]


# ============================================================================
# TESTES DE FUNCIONALIDADE DE RESET
# ============================================================================

def test_resetar_contadores_reseta_temp():
    """Testa que resetar_contadores() reseta o contador de temp para 0."""
    gerenciador = GerenciadorTAC()

    # Gera alguns temps
    gerenciador.nova_temp()  # t0
    gerenciador.nova_temp()  # t1
    gerenciador.nova_temp()  # t2

    assert gerenciador.obter_contador_temp() == 3

    # Reset
    gerenciador.resetar_contadores()

    assert gerenciador.obter_contador_temp() == 0
    assert gerenciador.nova_temp() == "t0"


def test_resetar_contadores_reseta_rotulo():
    """Testa que resetar_contadores() reseta o contador de rótulo para 0."""
    gerenciador = GerenciadorTAC()

    # Gera alguns rótulos
    gerenciador.novo_rotulo()  # L0
    gerenciador.novo_rotulo()  # L1
    gerenciador.novo_rotulo()  # L2

    assert gerenciador.obter_contador_rotulo() == 3

    # Reset
    gerenciador.resetar_contadores()

    assert gerenciador.obter_contador_rotulo() == 0
    assert gerenciador.novo_rotulo() == "L0"


def test_resetar_contadores_reseta_ambos():
    """Testa que resetar_contadores() reseta ambos contadores de temp e rótulo."""
    gerenciador = GerenciadorTAC()

    # Gera alguns de cada
    gerenciador.nova_temp()   # t0
    gerenciador.nova_temp()   # t1
    gerenciador.novo_rotulo()  # L0
    gerenciador.novo_rotulo()  # L1
    gerenciador.novo_rotulo()  # L2

    assert gerenciador.obter_contador_temp() == 2
    assert gerenciador.obter_contador_rotulo() == 3

    # Reset
    gerenciador.resetar_contadores()

    assert gerenciador.obter_contador_temp() == 0
    assert gerenciador.obter_contador_rotulo() == 0
    assert gerenciador.nova_temp() == "t0"
    assert gerenciador.novo_rotulo() == "L0"


def test_multiplos_resets():
    """Testa que resetar_contadores() pode ser chamado múltiplas vezes."""
    gerenciador = GerenciadorTAC()

    for _ in range(5):
        # Gera alguns itens
        gerenciador.nova_temp()
        gerenciador.novo_rotulo()

        # Reset e verifica
        gerenciador.resetar_contadores()
        assert gerenciador.obter_contador_temp() == 0
        assert gerenciador.obter_contador_rotulo() == 0


# ============================================================================
# TESTES DE ESTATÍSTICAS
# ============================================================================

def test_estatisticas_estado_inicial():
    """Testa que estatísticas estão corretas no estado inicial."""
    gerenciador = GerenciadorTAC()

    stats = gerenciador.obter_estatisticas()

    assert stats["contador_temp_atual"] == 0
    assert stats["contador_rotulo_atual"] == 0
    assert stats["total_temps_criados"] == 0
    assert stats["total_rotulos_criados"] == 0


def test_estatisticas_apos_geracao():
    """Testa que estatísticas rastreiam corretamente temps e rótulos gerados."""
    gerenciador = GerenciadorTAC()

    # Gera 5 temps e 3 rótulos
    for _ in range(5):
        gerenciador.nova_temp()
    for _ in range(3):
        gerenciador.novo_rotulo()

    stats = gerenciador.obter_estatisticas()

    assert stats["contador_temp_atual"] == 5
    assert stats["contador_rotulo_atual"] == 3
    assert stats["total_temps_criados"] == 5
    assert stats["total_rotulos_criados"] == 3


def test_estatisticas_persistem_apos_reset():
    """Testa que estatísticas totais persistem através de resetar_contadores()."""
    gerenciador = GerenciadorTAC()

    # Primeiro programa: 3 temps, 2 rótulos
    for _ in range(3):
        gerenciador.nova_temp()
    for _ in range(2):
        gerenciador.novo_rotulo()

    gerenciador.resetar_contadores()

    # Segundo programa: 4 temps, 5 rótulos
    for _ in range(4):
        gerenciador.nova_temp()
    for _ in range(5):
        gerenciador.novo_rotulo()

    stats = gerenciador.obter_estatisticas()

    # Contagens atuais devem refletir segundo programa
    assert stats["contador_temp_atual"] == 4
    assert stats["contador_rotulo_atual"] == 5

    # Contagens totais devem incluir ambos programas
    assert stats["total_temps_criados"] == 7  # 3 + 4
    assert stats["total_rotulos_criados"] == 7  # 2 + 5


# ============================================================================
# TESTES DE REPRESENTAÇÃO STRING
# ============================================================================

def test_repr():
    """Testa que __repr__ retorna string informativa."""
    gerenciador = GerenciadorTAC()

    gerenciador.nova_temp()
    gerenciador.nova_temp()
    gerenciador.novo_rotulo()

    repr_str = repr(gerenciador)

    assert "GerenciadorTAC" in repr_str
    assert "contador_temp=2" in repr_str
    assert "contador_rotulo=1" in repr_str


# ============================================================================
# TESTES DE CENÁRIOS DE INTEGRAÇÃO
# ============================================================================

def test_cenario_expressao_simples():
    """
    Testa um cenário realístico: gerando TAC para expressão (5 3 +).

    TAC esperado:
        t0 = 5
        t1 = 3
        t2 = t0 + t1
    """
    gerenciador = GerenciadorTAC()

    temp1 = gerenciador.nova_temp()  # Para literal 5
    temp2 = gerenciador.nova_temp()  # Para literal 3
    temp3 = gerenciador.nova_temp()  # Para resultado da adição

    assert temp1 == "t0"
    assert temp2 == "t1"
    assert temp3 == "t2"
    assert gerenciador.obter_contador_temp() == 3


def test_cenario_if_statement():
    """
    Testa um cenário realístico: gerando TAC para if statement.

    Padrão esperado:
        [avaliação da condição usando temps]
        if condição goto L0
        [bloco else]
        goto L1
        L0:
        [bloco then]
        L1:
    """
    gerenciador = GerenciadorTAC()

    # Avaliação da condição pode usar temps
    temp_cond = gerenciador.nova_temp()

    # Rótulos para fluxo de controle
    rotulo_then = gerenciador.novo_rotulo()
    rotulo_fim = gerenciador.novo_rotulo()

    assert temp_cond == "t0"
    assert rotulo_then == "L0"
    assert rotulo_fim == "L1"


def test_cenario_loop():
    """
    Testa um cenário realístico: gerando TAC para um loop.

    Padrão esperado:
        L0:  (início do loop)
        [corpo do loop com temps]
        [verificação da condição]
        if condição goto L0
        L1:  (fim do loop)
    """
    gerenciador = GerenciadorTAC()

    rotulo_inicio = gerenciador.novo_rotulo()

    # Corpo do loop pode usar vários temps
    temp1 = gerenciador.nova_temp()
    temp2 = gerenciador.nova_temp()
    temp_cond = gerenciador.nova_temp()

    rotulo_fim = gerenciador.novo_rotulo()

    assert rotulo_inicio == "L0"
    assert temp1 == "t0"
    assert temp2 == "t1"
    assert temp_cond == "t2"
    assert rotulo_fim == "L1"


def test_cenario_multiplos_programas():
    """
    Testa processamento de múltiplos programas sequencialmente.
    Cada programa deve começar com t0 e L0.
    """
    gerenciador = GerenciadorTAC()

    # Primeiro programa
    temp1_prog1 = gerenciador.nova_temp()
    rotulo1_prog1 = gerenciador.novo_rotulo()

    assert temp1_prog1 == "t0"
    assert rotulo1_prog1 == "L0"

    # Reset para segundo programa
    gerenciador.resetar_contadores()

    # Segundo programa deve começar de 0
    temp1_prog2 = gerenciador.nova_temp()
    rotulo1_prog2 = gerenciador.novo_rotulo()

    assert temp1_prog2 == "t0"
    assert rotulo1_prog2 == "L0"

    # Mas estatísticas totais devem refletir ambos programas
    stats = gerenciador.obter_estatisticas()
    assert stats["total_temps_criados"] == 2
    assert stats["total_rotulos_criados"] == 2


# ============================================================================
# FIXTURES PYTEST
# ============================================================================

@pytest.fixture
def gerenciador_novo():
    """Fixture fornecendo uma instância nova de GerenciadorTAC para cada teste."""
    return GerenciadorTAC()


@pytest.fixture
def gerenciador_populado():
    """Fixture fornecendo um GerenciadorTAC com alguns temps e rótulos já gerados."""
    gerenciador = GerenciadorTAC()
    gerenciador.nova_temp()  # t0
    gerenciador.nova_temp()  # t1
    gerenciador.novo_rotulo()  # L0
    return gerenciador


def test_com_fixture_gerenciador_novo(gerenciador_novo):
    """Testa usando fixture gerenciador_novo."""
    assert gerenciador_novo.obter_contador_temp() == 0
    assert gerenciador_novo.obter_contador_rotulo() == 0


def test_com_fixture_gerenciador_populado(gerenciador_populado):
    """Testa usando fixture gerenciador_populado."""
    assert gerenciador_populado.obter_contador_temp() == 2
    assert gerenciador_populado.obter_contador_rotulo() == 1

    # Gera próximos itens
    assert gerenciador_populado.nova_temp() == "t2"
    assert gerenciador_populado.novo_rotulo() == "L1"
