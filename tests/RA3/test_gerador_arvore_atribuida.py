#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1

import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from src.RA3.functions.python import gerador_arvore_atribuida


class TestGerarArvoreAtribuida(unittest.TestCase):
    """Testes para a função gerarArvoreAtribuida."""

    def test_arvore_vazia(self):
        """Deve retornar árvore vazia para entrada vazia."""
        resultado = gerador_arvore_atribuida.gerarArvoreAtribuida({})
        esperado = {'arvore_atribuida': []}
        self.assertEqual(resultado, esperado)

    def test_arvore_sem_linhas(self):
        """Deve retornar árvore vazia quando não há linhas."""
        arvore_anotada = {'outras_chaves': 'valor'}
        resultado = gerador_arvore_atribuida.gerarArvoreAtribuida(arvore_anotada)
        esperado = {'arvore_atribuida': []}
        self.assertEqual(resultado, esperado)

    def test_arvore_com_uma_linha_simples(self):
        """Deve processar uma linha simples corretamente."""
        arvore_anotada = {
            'linhas': [
                {
                    'numero_linha': 1,
                    'tipo': 'int',
                    'operador': '+',
                    'elementos': [
                        {'subtipo': 'numero_inteiro', 'valor': 5, 'tipo': 'int'},
                        {'subtipo': 'numero_inteiro', 'valor': 3, 'tipo': 'int'}
                    ]
                }
            ]
        }

        resultado = gerador_arvore_atribuida.gerarArvoreAtribuida(arvore_anotada)

        self.assertEqual(len(resultado['arvore_atribuida']), 1)
        no_raiz = resultado['arvore_atribuida'][0]

        self.assertEqual(no_raiz['tipo_vertice'], 'ARITH_OP')
        self.assertEqual(no_raiz['tipo_inferido'], 'int')
        self.assertEqual(no_raiz['numero_linha'], 1)
        self.assertEqual(no_raiz['operador'], '+')
        self.assertEqual(len(no_raiz['filhos']), 2)

    def test_arvore_com_multiplas_linhas(self):
        """Deve processar múltiplas linhas corretamente."""
        arvore_anotada = {
            'linhas': [
                {
                    'numero_linha': 1,
                    'tipo': 'int',
                    'operador': '+',
                    'elementos': [
                        {'subtipo': 'numero_inteiro', 'valor': 5, 'tipo': 'int'},
                        {'subtipo': 'numero_inteiro', 'valor': 3, 'tipo': 'int'}
                    ]
                },
                {
                    'numero_linha': 2,
                    'tipo': 'boolean',
                    'operador': '>',
                    'elementos': [
                        {'subtipo': 'numero_inteiro', 'valor': 10, 'tipo': 'int'},
                        {'subtipo': 'numero_inteiro', 'valor': 5, 'tipo': 'int'}
                    ]
                }
            ]
        }

        resultado = gerador_arvore_atribuida.gerarArvoreAtribuida(arvore_anotada)

        self.assertEqual(len(resultado['arvore_atribuida']), 2)

        # Verificar primeira linha
        no1 = resultado['arvore_atribuida'][0]
        self.assertEqual(no1['tipo_vertice'], 'ARITH_OP')
        self.assertEqual(no1['tipo_inferido'], 'int')
        self.assertEqual(no1['numero_linha'], 1)

        # Verificar segunda linha
        no2 = resultado['arvore_atribuida'][1]
        self.assertEqual(no2['tipo_vertice'], 'COMP_OP')
        self.assertEqual(no2['tipo_inferido'], 'boolean')
        self.assertEqual(no2['numero_linha'], 2)


class TestConstruirNoAtribuido(unittest.TestCase):
    """Testes para a função _construir_no_atribuido."""

    def test_no_linha_simples(self):
        """Deve construir nó para linha simples."""
        no = {
            'numero_linha': 1,
            'tipo': 'int'
        }

        resultado = gerador_arvore_atribuida._construir_no_atribuido(no, 1)

        self.assertEqual(resultado['tipo_vertice'], 'LINHA')
        self.assertEqual(resultado['tipo_inferido'], 'int')
        self.assertEqual(resultado['numero_linha'], 1)
        self.assertEqual(resultado['filhos'], [])

    def test_no_operador_aritmetico(self):
        """Deve construir nó para operador aritmético."""
        no = {
            'numero_linha': 1,
            'tipo': 'int',
            'operador': '+',
            'elementos': [
                {'subtipo': 'numero_inteiro', 'valor': 5, 'tipo': 'int'},
                {'subtipo': 'numero_inteiro', 'valor': 3, 'tipo': 'int'}
            ]
        }

        resultado = gerador_arvore_atribuida._construir_no_atribuido(no, 1)

        self.assertEqual(resultado['tipo_vertice'], 'ARITH_OP')
        self.assertEqual(resultado['tipo_inferido'], 'int')
        self.assertEqual(resultado['numero_linha'], 1)
        self.assertEqual(resultado['operador'], '+')
        self.assertEqual(len(resultado['filhos']), 2)

    def test_no_operador_comparacao(self):
        """Deve construir nó para operador de comparação."""
        no = {
            'numero_linha': 1,
            'tipo': 'boolean',
            'operador': '>',
            'elementos': [
                {'subtipo': 'numero_inteiro', 'valor': 10, 'tipo': 'int'},
                {'subtipo': 'numero_inteiro', 'valor': 5, 'tipo': 'int'}
            ]
        }

        resultado = gerador_arvore_atribuida._construir_no_atribuido(no, 1)

        self.assertEqual(resultado['tipo_vertice'], 'COMP_OP')
        self.assertEqual(resultado['tipo_inferido'], 'boolean')
        self.assertEqual(resultado['numero_linha'], 1)
        self.assertEqual(resultado['operador'], '>')

    def test_no_operador_logico(self):
        """Deve construir nó para operador lógico."""
        no = {
            'numero_linha': 1,
            'tipo': 'boolean',
            'operador': '&&',
            'elementos': [
                {'subtipo': 'numero_inteiro', 'valor': 1, 'tipo': 'int'},
                {'subtipo': 'numero_inteiro', 'valor': 0, 'tipo': 'int'}
            ]
        }

        resultado = gerador_arvore_atribuida._construir_no_atribuido(no, 1)

        self.assertEqual(resultado['tipo_vertice'], 'LOGIC_OP')
        self.assertEqual(resultado['tipo_inferido'], 'boolean')
        self.assertEqual(resultado['operador'], '&&')

    def test_no_operador_controle(self):
        """Deve construir nó para operador de controle."""
        no = {
            'numero_linha': 1,
            'tipo': 'real',
            'operador': 'IFELSE',
            'elementos': [
                {'subtipo': 'numero_inteiro', 'valor': 1, 'tipo': 'int'},
                {'subtipo': 'numero_real', 'valor': 3.14, 'tipo': 'real'},
                {'subtipo': 'numero_real', 'valor': 2.71, 'tipo': 'real'}
            ]
        }

        resultado = gerador_arvore_atribuida._construir_no_atribuido(no, 1)

        self.assertEqual(resultado['tipo_vertice'], 'CONTROL_OP')
        self.assertEqual(resultado['tipo_inferido'], 'real')
        self.assertEqual(resultado['operador'], 'IFELSE')

    def test_no_res(self):
        """Deve construir nó para operador RES."""
        no = {
            'numero_linha': 1,
            'tipo': 'int',
            'operador': 'RES',
            'elementos': [
                {'subtipo': 'numero_inteiro', 'valor': 2, 'tipo': 'int'}
            ]
        }

        resultado = gerador_arvore_atribuida._construir_no_atribuido(no, 1)

        self.assertEqual(resultado['tipo_vertice'], 'RES')
        self.assertEqual(resultado['tipo_inferido'], 'int')
        self.assertEqual(resultado['operador'], 'RES')

    def test_no_com_subexpressao(self):
        """Deve construir nó com subexpressão LINHA."""
        no = {
            'numero_linha': 1,
            'tipo': 'int',
            'operador': '+',
            'elementos': [
                {'subtipo': 'numero_inteiro', 'valor': 5, 'tipo': 'int'},
                {
                    'subtipo': 'LINHA',
                    'elementos': [
                        {'subtipo': 'numero_inteiro', 'valor': 3, 'tipo': 'int'},
                        {'subtipo': 'numero_inteiro', 'valor': 2, 'tipo': 'int'}
                    ],
                    'operador': '*'
                }
            ]
        }

        resultado = gerador_arvore_atribuida._construir_no_atribuido(no, 1)

        self.assertEqual(resultado['tipo_vertice'], 'ARITH_OP')
        self.assertEqual(len(resultado['filhos']), 2)

        # Verificar subexpressão
        sub_no = resultado['filhos'][1]
        self.assertEqual(sub_no['tipo_vertice'], 'ARITH_OP')
        self.assertEqual(sub_no['operador'], '*')
        self.assertEqual(len(sub_no['filhos']), 2)

    def test_no_com_variavel(self):
        """Deve construir nó para variável."""
        no = {
            'numero_linha': 1,
            'tipo': 'int',
            'subtipo': 'variavel',
            'valor': 'X'
        }

        resultado = gerador_arvore_atribuida._construir_no_atribuido(no, 1)

        self.assertEqual(resultado['tipo_vertice'], 'LINHA')
        self.assertEqual(resultado['tipo_inferido'], 'int')
        self.assertEqual(resultado['numero_linha'], 1)
        self.assertEqual(resultado['subtipo'], 'variavel')
        self.assertEqual(resultado['valor'], 'X')


class TestSalvarArvoreAtribuida(unittest.TestCase):
    """Testes para a função salvarArvoreAtribuida."""

    @patch('src.RA3.functions.python.gerador_arvore_atribuida.OUT_ARVORE_ATRIBUIDA_JSON')
    @patch('builtins.open', new_callable=mock_open)
    def test_salvar_arvore_simples(self, mock_file, mock_path):
        """Deve salvar árvore atribuída em JSON."""
        # Configure the mock path's parent with a MagicMock
        mock_parent = MagicMock()
        mock_path.parent = mock_parent

        arvore_atribuida = {
            'arvore_atribuida': [
                {
                    'tipo_vertice': 'ARITH_OP',
                    'tipo_inferido': 'int',
                    'numero_linha': 1,
                    'operador': '+',
                    'filhos': []
                }
            ]
        }

        gerador_arvore_atribuida.salvarArvoreAtribuida(arvore_atribuida)

        # Verificar se mkdir foi chamado no parent do path mockado
        mock_parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)

        # Verificar se open foi chamado (deve ser chamado 2 vezes - outputs e raiz)
        self.assertEqual(mock_file.call_count, 2)

        # Verificar se json.dump foi chamado (write é chamado múltiplas vezes pelo json.dump)
        self.assertTrue(mock_file().write.called)


class TestExecutarGeracaoArvoreAtribuida(unittest.TestCase):
    """Testes para a função executar_geracao_arvore_atribuida."""

    @patch('src.RA3.functions.python.gerador_arvore_atribuida.salvarArvoreAtribuida')
    @patch('src.RA3.functions.python.gerador_arvore_atribuida.gerarRelatoriosMarkdown')
    @patch('src.RA3.functions.python.gerador_arvore_atribuida.gerarArvoreAtribuida')
    def test_execucao_sucesso(self, mock_gerar_arvore, mock_gerar_relatorios, mock_salvar):
        """Deve executar geração completa com sucesso."""
        # Configurar mocks
        mock_gerar_arvore.return_value = {'arvore_atribuida': []}

        resultado_semantico = {
            'arvore_anotada': {'linhas': []},
            'erros': [],
            'tabela_simbolos': None
        }

        resultado = gerador_arvore_atribuida.executar_geracao_arvore_atribuida(resultado_semantico)

        self.assertTrue(resultado['sucesso'])
        self.assertIn('arvore_atribuida', resultado)
        self.assertIn('relatorios_gerados', resultado)
        self.assertIn('arquivo_arvore_json', resultado)

        # Verificar que os relatórios foram gerados em ambos os locais (outputs e raiz)
        self.assertEqual(len(resultado['relatorios_gerados']), 8)  # 4 relatórios x 2 locais

        # Verificar caminhos dos relatórios
        relatorios_outputs = [
            str(gerador_arvore_atribuida.OUT_RELATORIOS_DIR / "arvore_atribuida.md"),
            str(gerador_arvore_atribuida.OUT_RELATORIOS_DIR / "julgamento_tipos.md"),
            str(gerador_arvore_atribuida.OUT_RELATORIOS_DIR / "erros_sematicos.md"),
            str(gerador_arvore_atribuida.OUT_RELATORIOS_DIR / "tabela_simbolos.md")
        ]

        relatorios_raiz = [
            str(gerador_arvore_atribuida.ROOT_RELATORIOS_DIR / "arvore_atribuida.md"),
            str(gerador_arvore_atribuida.ROOT_RELATORIOS_DIR / "julgamento_tipos.md"),
            str(gerador_arvore_atribuida.ROOT_RELATORIOS_DIR / "erros_sematicos.md"),
            str(gerador_arvore_atribuida.ROOT_RELATORIOS_DIR / "tabela_simbolos.md")
        ]

        for relatorio in relatorios_outputs + relatorios_raiz:
            self.assertIn(relatorio, resultado['relatorios_gerados'])

    @patch('src.RA3.functions.python.gerador_arvore_atribuida.gerarArvoreAtribuida')
    def test_execucao_com_erro(self, mock_gerar_arvore):
        """Deve lidar com erros durante a geração."""
        # Configurar mock para lançar exceção
        mock_gerar_arvore.side_effect = Exception("Erro de teste")

        resultado_semantico = {
            'arvore_anotada': {'linhas': []},
            'erros': [],
            'tabela_simbolos': None
        }

        resultado = gerador_arvore_atribuida.executar_geracao_arvore_atribuida(resultado_semantico)

        self.assertFalse(resultado['sucesso'])
        self.assertIn('Erro na geração da árvore atribuída', resultado['erro'])
        self.assertIsNone(resultado['arvore_atribuida'])
        self.assertEqual(resultado['relatorios_gerados'], [])


class TestRelatoriosMarkdown(unittest.TestCase):
    """Testes para as funções de geração de relatórios."""

    def test_formatar_arvore_simples(self):
        """Deve formatar árvore simples corretamente."""
        no = {
            'tipo_vertice': 'ARITH_OP',
            'tipo_inferido': 'int',
            'numero_linha': 1,
            'operador': '+',
            'filhos': []
        }

        resultado = gerador_arvore_atribuida._formatar_arvore(no, 0)

        linhas = resultado.strip().split('\n')
        self.assertEqual(len(linhas), 1)
        self.assertIn('ARITH_OP (+)', linhas[0])
        self.assertIn(': int', linhas[0])

    def test_formatar_arvore_com_filhos(self):
        """Deve formatar árvore com filhos corretamente."""
        no = {
            'tipo_vertice': 'ARITH_OP',
            'tipo_inferido': 'int',
            'numero_linha': 1,
            'operador': '+',
            'filhos': [
                {
                    'tipo_vertice': 'LINHA',
                    'tipo_inferido': 'int',
                    'numero_linha': 1,
                    'valor': 5,
                    'subtipo': 'numero_inteiro',
                    'filhos': []
                },
                {
                    'tipo_vertice': 'LINHA',
                    'tipo_inferido': 'int',
                    'numero_linha': 1,
                    'valor': 3,
                    'subtipo': 'numero_inteiro',
                    'filhos': []
                }
            ]
        }

        resultado = gerador_arvore_atribuida._formatar_arvore(no, 0)

        linhas = resultado.strip().split('\n')
        self.assertTrue(len(linhas) >= 3)  # Nó pai + 2 filhos

        # Verificar indentação
        self.assertTrue(linhas[0].startswith('ARITH_OP'))
        self.assertTrue(linhas[1].startswith('  LINHA'))  # Filho 1
        self.assertTrue(linhas[2].startswith('  LINHA'))  # Filho 2


if __name__ == '__main__':
    unittest.main()