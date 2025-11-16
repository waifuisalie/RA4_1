#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1

import unittest
from src.RA3.functions.python import tipos

class TestConstantesTipos(unittest.TestCase):
    """Testes para as constantes de tipos."""

    def test_tipos_basicos_definidos(self):
        """Deve ter todas as constantes básicas definidas."""
        self.assertEqual(tipos.TYPE_INT, 'int')
        self.assertEqual(tipos.TYPE_REAL, 'real')
        self.assertEqual(tipos.TYPE_BOOLEAN, 'boolean')

    def test_conjuntos_tipos(self):
        """Deve ter os conjuntos de tipos corretos."""
        self.assertIn(tipos.TYPE_INT, tipos.TIPOS_VALIDOS)
        self.assertIn(tipos.TYPE_REAL, tipos.TIPOS_VALIDOS)
        self.assertIn(tipos.TYPE_BOOLEAN, tipos.TIPOS_VALIDOS)

        self.assertIn(tipos.TYPE_INT, tipos.TIPOS_NUMERICOS)
        self.assertIn(tipos.TYPE_REAL, tipos.TIPOS_NUMERICOS)
        self.assertNotIn(tipos.TYPE_BOOLEAN, tipos.TIPOS_NUMERICOS)

        self.assertIn(tipos.TYPE_INT, tipos.TIPOS_TRUTHY)
        self.assertIn(tipos.TYPE_REAL, tipos.TIPOS_TRUTHY)
        self.assertIn(tipos.TYPE_BOOLEAN, tipos.TIPOS_TRUTHY)


class TestPromocaoTipos(unittest.TestCase):
    """Testes para promoção de tipos."""

    def test_promover_int_int(self):
        """int + int = int."""
        self.assertEqual(tipos.promover_tipo('int', 'int'), 'int')

    def test_promover_int_real(self):
        """int + real = real."""
        self.assertEqual(tipos.promover_tipo('int', 'real'), 'real')
        self.assertEqual(tipos.promover_tipo('real', 'int'), 'real')

    def test_promover_real_real(self):
        """real + real = real."""
        self.assertEqual(tipos.promover_tipo('real', 'real'), 'real')

    def test_promover_tipo_invalido(self):
        """Deve rejeitar tipos inválidos."""
        with self.assertRaises(ValueError):
            tipos.promover_tipo('boolean', 'int')

        with self.assertRaises(ValueError):
            tipos.promover_tipo('int', 'boolean')


class TestConversaoBoolean(unittest.TestCase):
    """Testes para conversão para boolean."""

    def test_boolean_para_boolean(self):
        """Boolean direto."""
        self.assertTrue(tipos.para_booleano(True, 'boolean'))
        self.assertFalse(tipos.para_booleano(False, 'boolean'))

    def test_int_para_boolean(self):
        """Int para boolean."""
        self.assertTrue(tipos.para_booleano(5, 'int'))
        self.assertTrue(tipos.para_booleano(-1, 'int'))
        self.assertFalse(tipos.para_booleano(0, 'int'))

    def test_real_para_boolean(self):
        """Real para boolean."""
        self.assertTrue(tipos.para_booleano(3.14, 'real'))
        self.assertTrue(tipos.para_booleano(-2.5, 'real'))
        self.assertFalse(tipos.para_booleano(0.0, 'real'))

    def test_conversao_tipo_invalido(self):
        """Deve rejeitar tipo inválido."""
        with self.assertRaises(ValueError):
            tipos.para_booleano('string', 'invalid')


class TestCompatibilidadeAritmetica(unittest.TestCase):
    """Testes para compatibilidade aritmética."""

    def test_aritmetica_basica_compatibilidade(self):
        """Operadores básicos devem aceitar int/real."""
        self.assertTrue(tipos.tipos_compativeis_aritmetica('int', 'int'))
        self.assertTrue(tipos.tipos_compativeis_aritmetica('int', 'real'))
        self.assertTrue(tipos.tipos_compativeis_aritmetica('real', 'real'))
        self.assertFalse(tipos.tipos_compativeis_aritmetica('boolean', 'int'))

    def test_divisao_inteira_restrita(self):
        """Divisão inteira só aceita int + int."""
        self.assertTrue(tipos.tipos_compativeis_divisao_inteira('int', 'int'))
        self.assertFalse(tipos.tipos_compativeis_divisao_inteira('int', 'real'))
        self.assertFalse(tipos.tipos_compativeis_divisao_inteira('real', 'int'))
        self.assertFalse(tipos.tipos_compativeis_divisao_inteira('real', 'real'))

    def test_potencia_restrita(self):
        """Potência requer base numérica e expoente int."""
        self.assertTrue(tipos.tipos_compativeis_potencia('int', 'int'))
        self.assertTrue(tipos.tipos_compativeis_potencia('real', 'int'))
        self.assertFalse(tipos.tipos_compativeis_potencia('int', 'real'))
        self.assertFalse(tipos.tipos_compativeis_potencia('boolean', 'int'))

    def test_comparacao_compatibilidade(self):
        """Comparação aceita apenas numéricos."""
        self.assertTrue(tipos.tipos_compativeis_comparacao('int', 'int'))
        self.assertTrue(tipos.tipos_compativeis_comparacao('int', 'real'))
        self.assertTrue(tipos.tipos_compativeis_comparacao('real', 'real'))
        self.assertFalse(tipos.tipos_compativeis_comparacao('boolean', 'int'))

    def test_logico_compatibilidade(self):
        """Lógico aceita truthy types."""
        self.assertTrue(tipos.tipos_compativeis_logico('boolean', 'boolean'))
        self.assertTrue(tipos.tipos_compativeis_logico('int', 'boolean'))
        self.assertTrue(tipos.tipos_compativeis_logico('real', 'int'))
        self.assertFalse(tipos.tipos_compativeis_logico('string', 'int'))

    def test_logico_unario_compatibilidade(self):
        """Lógico unário aceita truthy types."""
        self.assertTrue(tipos.tipo_compativel_logico_unario('boolean'))
        self.assertTrue(tipos.tipo_compativel_logico_unario('int'))
        self.assertTrue(tipos.tipo_compativel_logico_unario('real'))
        self.assertFalse(tipos.tipo_compativel_logico_unario('string'))

    def test_condicao_compatibilidade(self):
        """Condição aceita truthy types."""
        self.assertTrue(tipos.tipo_compativel_condicao('boolean'))
        self.assertTrue(tipos.tipo_compativel_condicao('int'))
        self.assertTrue(tipos.tipo_compativel_condicao('real'))
        self.assertFalse(tipos.tipo_compativel_condicao('string'))

    def test_armazenamento_compatibilidade(self):
        """Armazenamento só aceita numéricos."""
        self.assertTrue(tipos.tipo_compativel_armazenamento('int'))
        self.assertTrue(tipos.tipo_compativel_armazenamento('real'))
        self.assertFalse(tipos.tipo_compativel_armazenamento('boolean'))


class TestTipoResultado(unittest.TestCase):
    """Testes para inferência de tipo resultante."""

    def test_resultado_aritmetica_basica(self):
        """Operadores aritméticos básicos."""
        self.assertEqual(tipos.tipo_resultado_aritmetica('int', 'int', '+'), 'int')
        self.assertEqual(tipos.tipo_resultado_aritmetica('int', 'real', '+'), 'real')
        self.assertEqual(tipos.tipo_resultado_aritmetica('real', 'real', '*'), 'real')

    def test_resultado_divisao_real(self):
        """Divisão real sempre retorna real."""
        self.assertEqual(tipos.tipo_resultado_aritmetica('int', 'int', '|'), 'real')
        self.assertEqual(tipos.tipo_resultado_aritmetica('real', 'real', '|'), 'real')

    def test_resultado_divisao_inteira(self):
        """Divisão inteira sempre retorna int."""
        self.assertEqual(tipos.tipo_resultado_aritmetica('int', 'int', '/'), 'int')
        self.assertEqual(tipos.tipo_resultado_aritmetica('int', 'int', '%'), 'int')

    def test_resultado_potencia(self):
        """Potência retorna tipo da base."""
        self.assertEqual(tipos.tipo_resultado_aritmetica('int', 'int', '^'), 'int')
        self.assertEqual(tipos.tipo_resultado_aritmetica('real', 'int', '^'), 'real')

    def test_resultado_comparacao(self):
        """Comparação sempre retorna boolean."""
        self.assertEqual(tipos.tipo_resultado_comparacao('int', 'int'), 'boolean')
        self.assertEqual(tipos.tipo_resultado_comparacao('real', 'real'), 'boolean')

    def test_resultado_logico(self):
        """Lógico sempre retorna boolean."""
        self.assertEqual(tipos.tipo_resultado_logico('boolean', 'boolean'), 'boolean')
        self.assertEqual(tipos.tipo_resultado_logico('int', 'real'), 'boolean')

    def test_resultado_logico_unario(self):
        """Lógico unário sempre retorna boolean."""
        self.assertEqual(tipos.tipo_resultado_logico_unario('boolean'), 'boolean')
        self.assertEqual(tipos.tipo_resultado_logico_unario('int'), 'boolean')

    def test_resultado_aritmetica_invalida(self):
        """Deve rejeitar operações inválidas."""
        with self.assertRaises(ValueError):
            tipos.tipo_resultado_aritmetica('boolean', 'int', '+')

        with self.assertRaises(ValueError):
            tipos.tipo_resultado_aritmetica('int', 'real', '/')

        with self.assertRaises(ValueError):
            tipos.tipo_resultado_aritmetica('int', 'real', '^')


class TestUtilitarios(unittest.TestCase):
    """Testes para funções utilitárias."""

    def test_descricao_tipo(self):
        """Deve retornar descrições corretas."""
        self.assertEqual(tipos.descricao_tipo('int'), 'inteiro')
        self.assertEqual(tipos.descricao_tipo('real'), 'real (ponto flutuante)')
        self.assertEqual(tipos.descricao_tipo('boolean'), 'booleano')
        self.assertIn('desconhecido', tipos.descricao_tipo('invalid'))


class TestIntegracaoTipos(unittest.TestCase):
    """Testes de integração simulando cenários reais."""

    def test_cenario_expressao_aritmetica(self):
        """Cenário: avaliação de expressão aritmética."""
        # Simular: (5 + 3.5) * 2
        # 5 (int) + 3.5 (real) = real
        tipo_soma = tipos.promover_tipo('int', 'real')
        self.assertEqual(tipo_soma, 'real')

        # real * 2 (int) = real
        tipo_multiplicacao = tipos.promover_tipo('real', 'int')
        self.assertEqual(tipo_multiplicacao, 'real')

    def test_cenario_condicional(self):
        """Cenário: avaliação de condição."""
        # Simular: (x > 0) && (y < 10)
        # x > 0 -> boolean
        self.assertEqual(tipos.tipo_resultado_comparacao('int', 'int'), 'boolean')

        # y < 10 -> boolean
        self.assertEqual(tipos.tipo_resultado_comparacao('int', 'int'), 'boolean')

        # boolean && boolean -> boolean
        self.assertEqual(tipos.tipo_resultado_logico('boolean', 'boolean'), 'boolean')

    def test_cenario_divisao_inteira(self):
        """Cenário: divisão inteira válida."""
        # Simular: 10 / 3
        # Deve ser int / int -> int
        self.assertTrue(tipos.tipos_compativeis_divisao_inteira('int', 'int'))
        self.assertEqual(tipos.tipo_resultado_aritmetica('int', 'int', '/'), 'int')

    def test_cenario_potencia(self):
        """Cenário: potência válida."""
        # Simular: 2.0 ^ 3
        # Deve ser real ^ int -> real
        self.assertTrue(tipos.tipos_compativeis_potencia('real', 'int'))
        self.assertEqual(tipos.tipo_resultado_aritmetica('real', 'int', '^'), 'real')

    def test_cenario_armazenamento(self):
        """Cenário: armazenamento de resultado."""
        # Simular: (5 + 3.5) -> VAR
        # 5 + 3.5 = real, pode ser armazenado
        tipo_expressao = tipos.promover_tipo('int', 'real')
        self.assertEqual(tipo_expressao, 'real')
        self.assertTrue(tipos.tipo_compativel_armazenamento('real'))

        # boolean não pode ser armazenado
        self.assertFalse(tipos.tipo_compativel_armazenamento('boolean'))


def run_tests():
    """Executa todos os testes."""
    # Configurar verbosidade
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    print("=" * 70)
    print("EXECUTANDO TESTES UNITÁRIOS - SISTEMA DE TIPOS")
    print("=" * 70)
    print()

    run_tests()