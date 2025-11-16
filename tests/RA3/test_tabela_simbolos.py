#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1

"""
Testes Unitários para a Tabela de Símbolos

Este módulo contém testes abrangentes para todas as funcionalidades
da tabela de símbolos do analisador semântico.
"""

import unittest
from src.RA3.functions.python.tabela_simbolos import TabelaSimbolos, SimboloInfo, inicializarTabelaSimbolos
from src.RA3.functions.python import tipos


class TestSimboloInfo(unittest.TestCase):
    """Testes para a classe SimboloInfo."""

    def test_criar_simbolo_valido(self):
        """Deve criar símbolo com dados válidos."""
        simbolo = SimboloInfo(
            nome='VAR',
            tipo=tipos.TYPE_INT,
            inicializada=True,
            escopo=0,
            linha_declaracao=5
        )
        self.assertEqual(simbolo.nome, 'VAR')
        self.assertEqual(simbolo.tipo, tipos.TYPE_INT)
        self.assertTrue(simbolo.inicializada)
        self.assertEqual(simbolo.escopo, 0)
        self.assertEqual(simbolo.linha_declaracao, 5)

    def test_tipo_invalido(self):
        """Deve rejeitar tipo inválido para armazenamento."""
        with self.assertRaises(ValueError):
            SimboloInfo(nome='VAR', tipo=tipos.TYPE_BOOLEAN)

    def test_nome_lowercase_erro(self):
        """Deve rejeitar nome não-uppercase."""
        with self.assertRaises(ValueError):
            SimboloInfo(nome='var', tipo=tipos.TYPE_INT)

    def test_str_representation(self):
        """Deve ter representação string legível."""
        simbolo = SimboloInfo(nome='PI', tipo=tipos.TYPE_REAL, inicializada=True)
        string = str(simbolo)
        self.assertIn('PI', string)
        self.assertIn('real', string)
        self.assertIn('inicializada', string)


class TestTabelaSimbolos(unittest.TestCase):
    """Testes para a classe TabelaSimbolos."""

    def setUp(self):
        """Cria tabela limpa antes de cada teste."""
        self.tabela = TabelaSimbolos()

    def test_tabela_inicialmente_vazia(self):
        """Tabela deve estar vazia ao ser criada."""
        self.assertEqual(len(self.tabela), 0)
        self.assertEqual(len(self.tabela.simbolos), 0)

    def test_adicionar_simbolo(self):
        """Deve adicionar novo símbolo à tabela."""
        simbolo = self.tabela.adicionarSimbolo('VAR', tipos.TYPE_INT, True, 10)

        self.assertIsNotNone(simbolo)
        self.assertEqual(simbolo.nome, 'VAR')
        self.assertEqual(simbolo.tipo, tipos.TYPE_INT)
        self.assertTrue(simbolo.inicializada)
        self.assertEqual(simbolo.linha_declaracao, 10)
        self.assertEqual(len(self.tabela), 1)

    def test_adicionar_converte_uppercase(self):
        """Deve converter nome para uppercase automaticamente."""
        simbolo = self.tabela.adicionarSimbolo('var', tipos.TYPE_INT)
        self.assertEqual(simbolo.nome, 'VAR')

    def test_adicionar_tipo_invalido_erro(self):
        """Deve rejeitar tipo inválido para armazenamento."""
        with self.assertRaises(ValueError):
            self.tabela.adicionarSimbolo('BOOL_VAR', tipos.TYPE_BOOLEAN)

    def test_atualizar_simbolo_existente(self):
        """Deve atualizar símbolo que já existe."""
        # Adicionar como int
        self.tabela.adicionarSimbolo('VAR', tipos.TYPE_INT, False, 5)
        self.assertEqual(len(self.tabela), 1)

        # Atualizar para real
        simbolo = self.tabela.adicionarSimbolo('VAR', tipos.TYPE_REAL, True, 10)
        self.assertEqual(len(self.tabela), 1)  # Ainda apenas 1 símbolo
        self.assertEqual(simbolo.tipo, tipos.TYPE_REAL)
        self.assertTrue(simbolo.inicializada)

    def test_buscar_simbolo(self):
        """Deve encontrar símbolo adicionado."""
        self.tabela.adicionarSimbolo('VAR', tipos.TYPE_INT)
        simbolo = self.tabela.buscarSimbolo('VAR')

        self.assertIsNotNone(simbolo)
        self.assertEqual(simbolo.nome, 'VAR')

    def test_buscar_case_insensitive(self):
        """Busca deve ser case-insensitive."""
        self.tabela.adicionarSimbolo('VAR', tipos.TYPE_INT)

        self.assertIsNotNone(self.tabela.buscarSimbolo('VAR'))
        self.assertIsNotNone(self.tabela.buscarSimbolo('var'))
        self.assertIsNotNone(self.tabela.buscarSimbolo('Var'))

    def test_buscar_simbolo_inexistente(self):
        """Deve retornar None para símbolo não encontrado."""
        simbolo = self.tabela.buscarSimbolo('INEXISTENTE')
        self.assertIsNone(simbolo)

    def test_existe(self):
        """Deve verificar existência de símbolo."""
        self.assertFalse(self.tabela.existe('VAR'))

        self.tabela.adicionarSimbolo('VAR', tipos.TYPE_INT)
        self.assertTrue(self.tabela.existe('VAR'))
        self.assertTrue(self.tabela.existe('var'))  # Case-insensitive

    def test_contains_operator(self):
        """Deve suportar operador 'in'."""
        self.tabela.adicionarSimbolo('VAR', tipos.TYPE_INT)

        self.assertTrue('VAR' in self.tabela)
        self.assertTrue('var' in self.tabela)
        self.assertFalse('INEXISTENTE' in self.tabela)

    def test_marcar_inicializada(self):
        """Deve marcar símbolo como inicializada."""
        self.tabela.adicionarSimbolo('VAR', tipos.TYPE_INT, False)
        self.assertFalse(self.tabela.verificar_inicializacao('VAR'))

        sucesso = self.tabela.marcar_inicializada('VAR', 20)
        self.assertTrue(sucesso)
        self.assertTrue(self.tabela.verificar_inicializacao('VAR'))

        simbolo = self.tabela.buscarSimbolo('VAR')
        self.assertEqual(simbolo.linha_declaracao, 20)

    def test_marcar_inicializada_inexistente(self):
        """Deve retornar False ao marcar símbolo inexistente."""
        sucesso = self.tabela.marcar_inicializada('INEXISTENTE')
        self.assertFalse(sucesso)

    def test_verificar_inicializacao(self):
        """Deve verificar corretamente estado de inicialização."""
        # Não existe
        self.assertFalse(self.tabela.verificar_inicializacao('VAR'))

        # Existe mas não inicializada
        self.tabela.adicionarSimbolo('VAR', tipos.TYPE_INT, False)
        self.assertFalse(self.tabela.verificar_inicializacao('VAR'))

        # Existe e inicializada
        self.tabela.marcar_inicializada('VAR')
        self.assertTrue(self.tabela.verificar_inicializacao('VAR'))

    def test_obter_tipo(self):
        """Deve retornar tipo de símbolo."""
        self.tabela.adicionarSimbolo('INT_VAR', tipos.TYPE_INT)
        self.tabela.adicionarSimbolo('REAL_VAR', tipos.TYPE_REAL)

        self.assertEqual(self.tabela.obter_tipo('INT_VAR'), tipos.TYPE_INT)
        self.assertEqual(self.tabela.obter_tipo('REAL_VAR'), tipos.TYPE_REAL)
        self.assertIsNone(self.tabela.obter_tipo('INEXISTENTE'))

    def test_registrar_uso(self):
        """Deve registrar uso de variável."""
        self.tabela.adicionarSimbolo('VAR', tipos.TYPE_INT)

        sucesso = self.tabela.registrar_uso('VAR', 25)
        self.assertTrue(sucesso)
        self.assertEqual(self.tabela.obter_numero_usos('VAR'), 1)

        simbolo = self.tabela.buscarSimbolo('VAR')
        self.assertEqual(simbolo.linha_ultimo_uso, 25)

    def test_registrar_uso_multiplo(self):
        """Deve contar múltiplos usos."""
        self.tabela.adicionarSimbolo('VAR', tipos.TYPE_INT)

        self.tabela.registrar_uso('VAR')
        self.tabela.registrar_uso('VAR')
        self.tabela.registrar_uso('VAR')

        self.assertEqual(self.tabela.obter_numero_usos('VAR'), 3)

    def test_obter_numero_usos_zero(self):
        """Variável nunca usada deve ter contador zero."""
        self.tabela.adicionarSimbolo('VAR', tipos.TYPE_INT)
        self.assertEqual(self.tabela.obter_numero_usos('VAR'), 0)

    def test_obter_numero_usos_inexistente(self):
        """Variável inexistente deve retornar zero."""
        self.assertEqual(self.tabela.obter_numero_usos('INEXISTENTE'), 0)

    def test_limpar(self):
        """Deve limpar todos os símbolos."""
        self.tabela.adicionarSimbolo('VAR1', tipos.TYPE_INT)
        self.tabela.adicionarSimbolo('VAR2', tipos.TYPE_REAL)
        self.assertEqual(len(self.tabela), 2)

        self.tabela.limpar()
        self.assertEqual(len(self.tabela), 0)
        self.assertFalse(self.tabela.existe('VAR1'))
        self.assertFalse(self.tabela.existe('VAR2'))

    def test_listar_simbolos(self):
        """Deve listar todos os símbolos."""
        self.tabela.adicionarSimbolo('A', tipos.TYPE_INT, True)
        self.tabela.adicionarSimbolo('B', tipos.TYPE_REAL, False)
        self.tabela.adicionarSimbolo('C', tipos.TYPE_INT, True)

        simbolos = self.tabela.listar_simbolos()
        self.assertEqual(len(simbolos), 3)

        # Deve estar ordenado por nome
        nomes = [s.nome for s in simbolos]
        self.assertEqual(nomes, ['A', 'B', 'C'])

    def test_listar_apenas_inicializadas(self):
        """Deve filtrar apenas símbolos inicializados."""
        self.tabela.adicionarSimbolo('A', tipos.TYPE_INT, True)
        self.tabela.adicionarSimbolo('B', tipos.TYPE_REAL, False)
        self.tabela.adicionarSimbolo('C', tipos.TYPE_INT, True)

        inicializadas = self.tabela.listar_simbolos(apenas_inicializadas=True)
        self.assertEqual(len(inicializadas), 2)
        nomes = [s.nome for s in inicializadas]
        self.assertIn('A', nomes)
        self.assertIn('C', nomes)
        self.assertNotIn('B', nomes)

    def test_gerar_relatorio(self):
        """Deve gerar relatório textual."""
        self.tabela.adicionarSimbolo('CONTADOR', tipos.TYPE_INT, True, 5)
        self.tabela.adicionarSimbolo('PI', tipos.TYPE_REAL, True, 10)
        self.tabela.registrar_uso('CONTADOR', 20)

        relatorio = self.tabela.gerar_relatorio()

        self.assertIn('TABELA DE SÍMBOLOS', relatorio)
        self.assertIn('CONTADOR', relatorio)
        self.assertIn('PI', relatorio)
        self.assertIn('int', relatorio)
        self.assertIn('real', relatorio)

    def test_escopo_inicial(self):
        """Deve ter escopo inicial correto."""
        self.assertEqual(self.tabela.escopo_atual, 0)

    def test_multiplos_simbolos(self):
        """Deve gerenciar múltiplos símbolos corretamente."""
        variaveis = ['VAR1', 'VAR2', 'VAR3', 'CONTADOR', 'SOMA', 'PI']

        for var in variaveis:
            tipo = tipos.TYPE_REAL if 'PI' in var else tipos.TYPE_INT
            self.tabela.adicionarSimbolo(var, tipo, True)

        self.assertEqual(len(self.tabela), len(variaveis))

        for var in variaveis:
            self.assertTrue(self.tabela.existe(var))
            self.assertTrue(self.tabela.verificar_inicializacao(var))


class TestIntegracaoTabelaSimbolos(unittest.TestCase):
    """Testes de integração simulando uso real."""

    def setUp(self):
        """Cria tabela limpa."""
        self.tabela = inicializarTabelaSimbolos()

    def test_cenario_uso_tipico(self):
        """Simula uso típico: declarar, usar, verificar."""
        # Linha 1: (5 CONTADOR MEM)
        self.tabela.adicionarSimbolo('CONTADOR', tipos.TYPE_INT, True, 1)

        # Linha 2: (CONTADOR 1 + CONTADOR MEM)
        self.assertTrue(self.tabela.verificar_inicializacao('CONTADOR'))
        self.tabela.registrar_uso('CONTADOR', 2)
        self.tabela.adicionarSimbolo('CONTADOR', tipos.TYPE_INT, True, 2)

        # Linha 3: (CONTADOR)
        self.assertTrue(self.tabela.verificar_inicializacao('CONTADOR'))
        self.tabela.registrar_uso('CONTADOR', 3)

        # Verificações finais
        self.assertEqual(self.tabela.obter_numero_usos('CONTADOR'), 2)
        self.assertEqual(self.tabela.obter_tipo('CONTADOR'), tipos.TYPE_INT)

    def test_erro_uso_antes_inicializacao(self):
        """Deve detectar uso antes de inicialização."""
        # Tentar usar variável não inicializada
        existe = self.tabela.existe('VAR')
        self.assertFalse(existe)

        # Se existe, verificar inicialização
        if existe:
            inicializada = self.tabela.verificar_inicializacao('VAR')
            self.assertFalse(inicializada)

    def test_mudanca_tipo_variavel(self):
        """Deve permitir redeclaração com tipo diferente."""
        # Declarar como int
        self.tabela.adicionarSimbolo('VAR', tipos.TYPE_INT, True, 5)
        self.assertEqual(self.tabela.obter_tipo('VAR'), tipos.TYPE_INT)

        # Redeclarar como real
        self.tabela.adicionarSimbolo('VAR', tipos.TYPE_REAL, True, 10)
        self.assertEqual(self.tabela.obter_tipo('VAR'), tipos.TYPE_REAL)
        self.assertEqual(len(self.tabela), 1)  # Ainda apenas 1 símbolo

    def test_variaveis_diferentes_tipos(self):
        """Deve gerenciar variáveis de tipos diferentes."""
        self.tabela.adicionarSimbolo('INT_VAR', tipos.TYPE_INT, True, 1)
        self.tabela.adicionarSimbolo('REAL_VAR', tipos.TYPE_REAL, True, 2)

        self.assertEqual(self.tabela.obter_tipo('INT_VAR'), tipos.TYPE_INT)
        self.assertEqual(self.tabela.obter_tipo('REAL_VAR'), tipos.TYPE_REAL)

        # Ambas devem estar inicializadas
        self.assertTrue(self.tabela.verificar_inicializacao('INT_VAR'))
        self.assertTrue(self.tabela.verificar_inicializacao('REAL_VAR'))


def run_tests():
    """Executa todos os testes."""
    # Configurar verbosidade
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    print("=" * 70)
    print("EXECUTANDO TESTES UNITÁRIOS - TABELA DE SÍMBOLOS")
    print("=" * 70)
    print()

    run_tests()
