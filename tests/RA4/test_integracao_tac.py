#!/usr/bin/env python3
"""
Testes de integração para geração TAC usando arvore_atribuida.json completa.

Testa o pipeline completo: AST da Fase 3 → geração TAC

Esta suíte de testes valida que Issues 1.3 e 1.4 funcionam corretamente com
a AST atribuída completa da Fase 3, incluindo a correção recente onde todos
os nós (incluindo wrappers LINHA literais) têm tipo_inferido populado.

DEVE SER EXECUTADO COM ÁRVORE AST GERADA DE inputs/RA4/teste_gerarTAC.txt
"""

import json
import pytest
from pathlib import Path
from datetime import datetime
from src.RA4.functions.python.gerenciador_tac import GerenciadorTAC
from src.RA4.functions.python.percorredor_ast import PercorredorAST


# Caminhos
PROJECT_ROOT = Path(__file__).parent.parent.parent
AST_PATH = PROJECT_ROOT / "outputs" / "RA3" / "arvore_atribuida.json"
TAC_DEBUG_OUTPUT = PROJECT_ROOT / "outputs" / "RA4" / "debug_tac_output.txt"


@pytest.fixture
def ast_real():
    """Carrega a arvore_atribuida.json real da saída da Fase 3."""
    with open(AST_PATH, "r") as f:
        return json.load(f)


@pytest.fixture
def ast_apenas_aritmetica(ast_real):
    """
    Filtra AST para incluir apenas operações aritméticas (linhas 1-11, 26).

    Isso evita operações lógicas que ainda não estão implementadas (Issue 1.5+).
    Linhas 1-11: ops aritméticas
    Linhas 12-25: atribuições e referências de variáveis
    Linhas 26-31: ops de comparação (parcialmente implementadas)
    Linhas 32-34: ops lógicas (causam crashes - ! unário não tratado)
    """
    filtrado = {
        "arvore_atribuida": [
            linha for linha in ast_real["arvore_atribuida"]
            if linha.get("numero_linha", 0) <= 31  # Exclui ops lógicas (32-34)
        ]
    }
    return filtrado


@pytest.fixture
def gerador_tac():
    """Cria um gerador TAC novo."""
    gerenciador = GerenciadorTAC()
    return PercorredorAST(gerenciador)


class TestIntegracaoTAC:
    """Testes de integração usando saída real da AST da Fase 3."""

    def test_pode_gerar_tac_de_ast_real(self, ast_apenas_aritmetica, gerador_tac):
        """Testa que geração TAC funciona com operações aritméticas."""
        instrucoes = gerador_tac.gerar_tac(ast_apenas_aritmetica)

        # Verificações básicas de sanidade
        assert len(instrucoes) > 0, "Deve gerar pelo menos algumas instruções"
        assert all(hasattr(instr, 'linha') for instr in instrucoes), \
            "Todas instruções devem ter números de linha"
        assert all(hasattr(instr, 'para_string') for instr in instrucoes), \
            "Todas instruções devem ser stringificáveis"

    def test_numeros_linha_preservados(self, ast_apenas_aritmetica, gerador_tac):
        """Testa que números de linha da AST são preservados no TAC."""
        instrucoes = gerador_tac.gerar_tac(ast_apenas_aritmetica)

        # Todos números de linha devem ser válidos (1-31 para subconjunto aritmético)
        numeros_linha = [instr.linha for instr in instrucoes]
        assert all(1 <= linha <= 31 for linha in numeros_linha), \
            "Números de linha devem estar em range válido (1-31)"

        # Números de linha devem estar em ordem (não decrescente)
        assert numeros_linha == sorted(numeros_linha), \
            "Números de linha devem estar em ordem"

    def test_todos_operadores_aritmeticos_presentes(self, ast_apenas_aritmetica, gerador_tac):
        """Testa que todos os 7 operadores aritméticos são gerados corretamente."""
        instrucoes = gerador_tac.gerar_tac(ast_apenas_aritmetica)

        # Converte para strings para busca mais fácil
        strings_instr = [instr.para_string() for instr in instrucoes]

        # Verifica cada operador (requisito Issue 1.4)
        operadores = ['+', '-', '*', '/', '|', '%', '^']
        for op in operadores:
            encontrado = any(f" {op} " in s for s in strings_instr)
            assert encontrado, f"Operador '{op}' deve aparecer no TAC"

    def test_corretude_estatisticas(self, ast_apenas_aritmetica, gerador_tac):
        """Testa que rastreamento de estatísticas funciona corretamente."""
        instrucoes = gerador_tac.gerar_tac(ast_apenas_aritmetica)
        stats = gerador_tac.obter_estatisticas()

        # Verifica se estatísticas fazem sentido
        assert stats["total_instrucoes"] == len(instrucoes), \
            "Contagem de instruções deve corresponder"
        assert stats["contador_temp"] > 0, "Deve ter gerado variáveis temporárias"

    def test_gerar_e_salvar_tac_completo(self, ast_apenas_aritmetica, gerador_tac):
        """
        Gera TAC completo e salva em arquivo para debug.

        Este teste imprime TODAS instruções TAC no console (visível com flag -s)
        e salva em outputs/RA4/debug_tac_output.txt para inspeção.
        """
        # Gera TAC
        instrucoes = gerador_tac.gerar_tac(ast_apenas_aritmetica)
        stats = gerador_tac.obter_estatisticas()

        # Imprime no console
        print("\n" + "=" * 70)
        print("=== SAÍDA TAC COMPLETA ===")
        print("=" * 70)
        print()

        for instr in instrucoes:
            # Formato: "Linha  1: t0 = 5.0          [real]"
            info_tipo = f"[{instr.tipo_dado}]" if hasattr(instr, 'tipo_dado') and instr.tipo_dado else ""
            print(f"Linha {instr.linha:2}: {instr.para_string():<25} {info_tipo}")

        print()
        print("=" * 70)
        print("Estatísticas:")
        for chave, valor in stats.items():
            print(f"  {chave}: {valor}")
        print("=" * 70)
        print()

        # Salva em arquivo
        TAC_DEBUG_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        with open(TAC_DEBUG_OUTPUT, 'w') as f:
            f.write("Saída TAC - Gerada de arvore_atribuida.json\n")
            f.write(f"Gerado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")

            for instr in instrucoes:
                info_tipo = f"[tipo: {instr.tipo_dado}]" if hasattr(instr, 'tipo_dado') and instr.tipo_dado else ""
                f.write(f"Linha {instr.linha:2}: {instr.para_string():<25} {info_tipo}\n")

            f.write("\n" + "=" * 70 + "\n")
            f.write("Estatísticas:\n")
            for chave, valor in stats.items():
                f.write(f"  {chave}: {valor}\n")
            f.write("=" * 70 + "\n")

        print(f"Saída TAC salva em: {TAC_DEBUG_OUTPUT}")
        print()

        # Sempre passa - isto é para geração de output
        assert True

    def test_operacoes_especificas(self, ast_apenas_aritmetica, gerador_tac):
        """Testa operações específicas para verificar corretude."""
        instrucoes = gerador_tac.gerar_tac(ast_apenas_aritmetica)

        # Linha 1: deve ter adição
        linha_1 = [i for i in instrucoes if i.linha == 1]
        assert any('+' in i.para_string() for i in linha_1), "Linha 1 deve ter adição"

        # Linha 2: deve ter multiplicação
        linha_2 = [i for i in instrucoes if i.linha == 2]
        assert any('*' in i.para_string() for i in linha_2), "Linha 2 deve ter multiplicação"


class TestIssues1_3_e_1_4:
    """
    Testes específicos para critérios de aceitação das Issues 1.3 e 1.4.

    Issue 1.3: Motor de Percurso AST (Pós-ordem)
    Issue 1.4: Geração de Expressão Aritmética
    """

    def test_issue_1_3_percurso_pos_ordem(self, ast_apenas_aritmetica, gerador_tac):
        """
        Verifica Issue 1.3: Percurso pós-ordem funciona corretamente.

        Pós-ordem significa que filhos são processados antes dos pais.
        Para (5 3.0 +), devemos ver:
          1. Processa 5 (folha)
          2. Processa 3.0 (folha)
          3. Processa + (pai)
        """
        instrucoes = gerador_tac.gerar_tac(ast_apenas_aritmetica)
        linha_1 = [i for i in instrucoes if i.linha == 1]

        # Deve ser: t0 = 5, t1 = 3, t2 = t0 + t1
        # Isso prova pós-ordem: folhas primeiro, depois operação
        assert "5" in linha_1[0].para_string(), "Primeiro: operando esquerdo (5)"
        assert "3" in linha_1[1].para_string(), "Segundo: operando direito (3)"
        assert "+" in linha_1[2].para_string(), "Terceiro: operação nos operandos"

    def test_issue_1_4_todos_operadores(self, ast_apenas_aritmetica, gerador_tac):
        """
        Verifica Issue 1.4: Todos operadores aritméticos implementados.

        Operadores requeridos: +, -, *, /, |, %, ^
        """
        instrucoes = gerador_tac.gerar_tac(ast_apenas_aritmetica)
        todo_tac = " ".join(i.para_string() for i in instrucoes)

        operadores_requeridos = {
            '+': "adição",
            '-': "subtração",
            '*': "multiplicação",
            '/': "divisão inteira",
            '|': "divisão real",
            '%': "módulo",
            '^': "exponenciação"
        }

        for op, nome in operadores_requeridos.items():
            assert f" {op} " in todo_tac, f"Operador '{op}' ({nome}) deve estar no TAC"
