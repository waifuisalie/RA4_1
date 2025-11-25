#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA4_1

import sys
import os
import traceback
from pathlib import Path
import json

# ============================================================================
# IMPORTS - RA1 (Análise Léxica)
# ============================================================================
# Mantemos apenas o necessário para tokenização (entrada do RA2/RA3)
# Execução de expressões e geração de Assembly foram removidos (legacy RA1)
# ============================================================================

from src.RA1.functions.python.io_utils import lerArquivo, salvar_tokens
from src.RA1.functions.python.rpn_calc import parseExpressao
from src.RA1.functions.python.tokens import Tipo_de_Token

# LEGACY: Imports comentados - não mais necessários para RA2/RA3
# from src.RA1.functions.python.exibirResultados import exibirResultados  # Executa expressões (legacy)
# from src.RA1.functions.assembly import gerarAssemblyMultiple, save_assembly, save_registers_inc  # Assembly (legacy)
from src.RA2.functions.python.gerarArvore import exportar_arvores_json
from src.RA2.functions.python.lerTokens import lerTokens, validarTokens, reconhecerToken
from src.RA2.functions.python.construirGramatica import imprimir_gramatica_completa
from src.RA2.functions.python.construirTabelaLL1 import construirTabelaLL1
from src.RA2.functions.python.parsear import parsear_todas_linhas
from src.RA3.functions.python.analisador_semantico import analisarSemanticaDaJsonRA2
from src.RA3.functions.python.gerador_arvore_atribuida import executar_geracao_arvore_atribuida
from src.RA4.functions.python.gerador_tac import gerarTAC
from src.RA4.functions.python.otimizador_tac import TACOptimizer

BASE_DIR    = Path(__file__).resolve().parent        # raiz do repo
OUT_TOKENS  = BASE_DIR / "outputs" / "RA1" / "tokens" / "tokens_gerados.txt"
# OUT_ASM_DIR = BASE_DIR / "outputs" / "RA1" / "assembly"        # Reserved for RA4 (future assembly generation phase)
OUT_ARVORE_JSON = BASE_DIR / "outputs" / "RA2" / "arvore_sintatica.json"

OUT_TOKENS.parent.mkdir(parents=True, exist_ok=True)


def segmentar_linha_em_instrucoes(linha_texto):
    """Segmenta uma linha em múltiplas instruções baseado em parênteses balanceados

    Args:
        linha_texto: Linha de texto contendo uma ou mais expressões entre parênteses

    Returns:
        Lista de strings, onde cada string é uma instrução completa com parênteses balanceados
    """
    instrucoes = []
    elementos = linha_texto.split()
    i = 0

    while i < len(elementos):
        if elementos[i] == '(':
            # Encontra expressão balanceada
            instrucao_elementos = []
            nivel_parenteses = 0

            while i < len(elementos):
                elemento = elementos[i]
                instrucao_elementos.append(elemento)

                if elemento == '(':
                    nivel_parenteses += 1
                elif elemento == ')':
                    nivel_parenteses -= 1

                i += 1

                # Quando parênteses estão balanceados, temos uma instrução completa
                if nivel_parenteses == 0:
                    break

            if instrucao_elementos:
                instrucoes.append(' '.join(instrucao_elementos))
        else:
            i += 1

    return instrucoes


def executar_ra1_tokenizacao(operacoes_lidas):
    """Executa a tokenização (RA1) das operações lidas

    Tokeniza as expressões sem executá-las. Os tokens gerados são a entrada
    necessária para RA2 (Parser) e RA3 (Semântico).

    Args:
        operacoes_lidas: Lista de strings com as linhas do arquivo de entrada

    Returns:
        tuple: (tokens_salvos_txt, linhas_processadas) onde:
            - tokens_salvos_txt: Lista de listas de strings (tokens por linha)
            - linhas_processadas: Número de linhas processadas (excluindo vazias e comentários)

    Note:
        - Execução de expressões e geração de Assembly foram removidos (legacy RA1)
        - Motivo: Especificação RA3 afirma "não será necessário gerar código Assembly"
    """
    print("--- TOKENIZAÇÃO (RA1 Lexical Analysis - Input for RA2/RA3) ---")
    tokens_salvos_txt = []
    linhas_processadas = 0

    for i, linha in enumerate(operacoes_lidas, 1):
        # Pula linhas vazias ou comentários
        if not linha.strip() or linha.strip().startswith('#'):
            continue

        linhas_processadas += 1

        try:
            # Tokeniza sem executar
            lista_de_tokens = parseExpressao(linha)
            # Salva tokens completos (incluindo parênteses) para RA2
            tokens_completos = [str(token.valor) for token in lista_de_tokens if token.tipo != Tipo_de_Token.FIM]
            tokens_salvos_txt.append(tokens_completos)
        except Exception as e:
            print(f"  ERRO na linha {i}: {e}")
            tokens_salvos_txt.append([])  # Adiciona lista vazia para manter índices

    # Salva os tokens gerados
    salvar_tokens(tokens_salvos_txt, OUT_TOKENS)
    print(f"  [OK] {linhas_processadas} linha(s) tokenizadas")
    print(f"  [OK] Tokens salvos em: {OUT_TOKENS.relative_to(BASE_DIR)}\n")

    return tokens_salvos_txt, linhas_processadas


def executar_ra2_validacao_tokens():
    """Executa a leitura e validação de tokens para análise sintática (RA2)

    Returns:
        tuple: (tokens_para_ra2, tokens_sao_validos) onde:
            - tokens_para_ra2: Lista de tokens lidos
            - tokens_sao_validos: Boolean indicando se validação passou

    Raises:
        SystemExit: Se houver erro no processamento de tokens
    """
    try:
        print("\n--- PROCESSAMENTO DE TOKENS PARA RA2 ---")
        tokens_para_ra2 = lerTokens(str(OUT_TOKENS))
        tokens_sao_validos = validarTokens(tokens_para_ra2)
        print(f"Tokens processados: {len(tokens_para_ra2)} tokens")
        print(f"Validação dos tokens: {'SUCESSO' if tokens_sao_validos else 'FALHOU'}")
        return tokens_para_ra2, tokens_sao_validos
    except Exception as e:
        print(f"  Erro no processamento de tokens: {e}")
        traceback.print_exc()
        sys.exit(1)


def executar_ra2_gramatica():
    """Exibe a gramática completa e constrói a tabela LL(1)

    Returns:
        dict: Tabela LL(1) construída

    Raises:
        SystemExit: Se houver erro ao exibir gramática ou construir tabela LL(1)
    """
    # Análise Sintática - Gramática
    try:
        print("\n--- ANALISE SINTATICA - GRAMATICA ---")
        imprimir_gramatica_completa()
    except Exception as e:
        print(f"  Erro ao exibir gramática: {e}")
        traceback.print_exc()
        sys.exit(1)

    # Construção da tabela LL(1)
    try:
        print("\n--- CONSTRUÇÃO DA TABELA LL(1) ---")
        tabela_ll1 = construirTabelaLL1()
        print(f"  Tabela LL(1) construída com {len(tabela_ll1)} entradas")
        return tabela_ll1
    except Exception as e:
        print(f"  Erro ao construir tabela LL(1): {e}")
        traceback.print_exc()
        sys.exit(1)


def executar_ra2_parsing(tabela_ll1):
    """Executa o parsing das linhas de tokens usando a tabela LL(1)

    Args:
        tabela_ll1: Tabela LL(1) para parsing

    Returns:
        tuple: (derivacoes, tokens_por_linha) onde:
            - derivacoes: Lista de derivações do parser
            - tokens_por_linha: Lista de listas de tokens por linha

    Note:
        Lê linha por linha do arquivo tokens_gerados.txt e segmenta em instruções
        usando parênteses balanceados
    """
    print("\n--- ANÁLISE SINTÁTICA COM PARSEAR ---")

    # Lê linha por linha do arquivo tokens_gerados.txt
    tokens_por_linha = []
    linhas_arquivo = lerArquivo(str(OUT_TOKENS))

    for linha_texto in linhas_arquivo:
        linha_texto = linha_texto.strip()
        if linha_texto and not linha_texto.startswith('#'):
            # Segmenta linha em múltiplas instruções se necessário
            instrucoes = segmentar_linha_em_instrucoes(linha_texto)

            for instrucao in instrucoes:
                # Processa cada instrução individualmente usando lerTokens
                tokens_linha = []
                elementos = instrucao.split()

                for elemento in elementos:
                    # Usa o reconhecerToken do lerTokens.py
                    token = reconhecerToken(elemento, 1)  # linha fictícia
                    if token:
                        tokens_linha.append(token)

                if tokens_linha:
                    tokens_por_linha.append(tokens_linha)

    print(f"Analisando {len(tokens_por_linha)} linha(s) de tokens")

    # Aplica parsear para cada linha
    derivacoes = parsear_todas_linhas(tabela_ll1, tokens_por_linha)

    return derivacoes, tokens_por_linha


def executar_ra2_geracao_arvores(derivacoes, tokens_por_linha):
    """Gera e exporta as árvores sintáticas em formato JSON

    Args:
        derivacoes: Lista de derivações do parser
        tokens_por_linha: Lista de listas de tokens por linha

    Note:
        Gera JSON das árvores sintáticas (entrada para RA3)
        Atualiza a documentação da gramática com a última árvore gerada
    """
    print("\n--- GERAÇÃO DAS ÁRVORES SINTÁTICAS ---")

    # Reconstrói linhas originais a partir dos tokens
    linhas_originais = []
    tokens_list = []
    for tokens_linha in tokens_por_linha:
        linha_texto = ' '.join([str(token.valor) for token in tokens_linha])
        linhas_originais.append(linha_texto)
        tokens_list.append([str(token.valor) for token in tokens_linha])

    exportar_arvores_json(derivacoes, tokens_list, linhas_originais)


def executar_ra3_analise_semantica():
    """Executa a análise semântica (RA3) completa

    Carrega a AST do RA2, executa as 3 fases de análise semântica
    (tipos, memória, controle) e gera a árvore atribuída com relatórios.

    Note:
        - Fase 1: Type checking
        - Fase 2: Memory validation
        - Fase 3: Control structures validation
        - Gera 4 relatórios: arvore_atribuida.md, julgamento_tipos.md,
          erros_sematicos.md, tabela_simbolos.md
    """
    print("\n--- RA3: ANÁLISE SEMÂNTICA ---")

    try:
        # Load AST from RA2
        with open(str(OUT_ARVORE_JSON), 'r', encoding='utf-8') as f:
            arvore_ra2 = json.load(f)

        # Execute complete semantic analysis (3 phases: types, memory, control)
        # This orchestrator function runs all validation phases sequentially
        resultado_semantico = analisarSemanticaDaJsonRA2(arvore_ra2)

        # Handle results based on return type
        if isinstance(resultado_semantico, list):
            # Analysis returned errors (list of error strings)
            print("    Erro(s) semântico(s) encontrado(s):")
            for erro in resultado_semantico:
                print(f"    {erro}")

            print("\n--- GERAÇÃO DA ÁRVORE ATRIBUÍDA ---")
            print("  Falha na análise semântica - gerando árvore com dados parciais...")

            # Create result structure for partial tree generation
            resultado_semantico_dict = {
                'arvore_anotada': arvore_ra2,
                'tabela_simbolos': None,
                'erros': resultado_semantico
            }
            resultado_arvore = executar_geracao_arvore_atribuida(resultado_semantico_dict)

            if resultado_arvore['sucesso']:
                print("  [OK] Árvore atribuída gerada com dados parciais")
                print(f"  [OK] Relatórios de erro salvos em: {BASE_DIR / 'outputs' / 'RA3' / 'relatorios'}")
            else:
                print(f"  [ERROR] Falha na geração da árvore: {resultado_arvore.get('erro', 'Erro desconhecido')}")

        else:
            # Analysis succeeded (returned dict with 'arvore_anotada' and 'tabela_simbolos')
            print("    [OK] Análise semântica concluída com sucesso sem nenhum erro")

            print("\n--- GERAÇÃO DA ÁRVORE ATRIBUÍDA ---")
            resultado_arvore = executar_geracao_arvore_atribuida(resultado_semantico)

            if resultado_arvore['sucesso']:
                print("    [OK] Árvore atribuída gerada e salva com sucesso")
                print(f"    [OK] Relatórios gerados em: {BASE_DIR / 'outputs' / 'RA3' / 'relatorios'}")
                print("      - arvore_atribuida.md")
                print("      - julgamento_tipos.md")
                print("      - erros_sematicos.md")
                print("      - tabela_simbolos.md")
            else:
                print(f"    [ERROR] Falha na geração da árvore atribuída: {resultado_arvore.get('erro', 'Erro desconhecido')}")

    except FileNotFoundError:
        print(f"  [ERROR] ERRO: Arquivo de árvore sintática não encontrado: {OUT_ARVORE_JSON}")
        print("  Certifique-se de que a análise sintática (RA2) foi executada corretamente.")
    except json.JSONDecodeError as e:
        print(f"  [ERROR] ERRO: Arquivo JSON inválido: {e}")
        print(f"  Arquivo: {OUT_ARVORE_JSON}")
    except Exception as e:
        print(f"  [ERROR] ERRO na análise semântica: {e}")
        traceback.print_exc()
        # Continue execution even if semantic analysis fails


def executar_ra4_geracao_tac():
    """Executa a geração de TAC (RA4)

    Carrega a árvore atribuída do RA3 e gera código TAC.

    Output Files:
        - outputs/RA4/tac_instructions.json
        - outputs/RA4/tac_output.md
    """
    print("\n--- RA4: GERAÇÃO DE TAC ---")

    try:
        ast_path = BASE_DIR / "outputs" / "RA3" / "arvore_atribuida.json"
        output_dir = BASE_DIR / "outputs" / "RA4"

        result = gerarTAC(ast_path, output_dir, save_output=True, source_file=str(ast_path))

        if result["success"]:
            print(f"    [OK] {result['statistics']['total_instructions']} instruções TAC geradas")
            print(f"    [OK] Arquivos salvos em: {output_dir.relative_to(BASE_DIR)}")
            print("      - tac_instructions.json")
            print("      - tac_output.md")
        else:
            print(f"    [ERROR] {result['error']}")

    except FileNotFoundError:
        print(f"  [ERROR] Arquivo de árvore atribuída não encontrado")
        print("  Certifique-se de que a análise semântica (RA3) foi executada corretamente.")
    except Exception as e:
        print(f"  [ERROR] ERRO na geração de TAC: {e}")
        traceback.print_exc()


def executar_ra4_otimizacao_tac(arquivo_entrada):
    """Executa a otimização de TAC (RA4)

    Carrega as instruções TAC geradas e aplica otimizações.

    Args:
        arquivo_entrada: Nome do arquivo de entrada original

    Output Files:
        - outputs/RA4/tac_otimizado.json
        - outputs/RA4/tac_otimizado.md
        - outputs/RA4/relatorios/otimizacao_tac.md
    """
    print("\n--- RA4: OTIMIZAÇÃO DE TAC ---")

    try:
        tac_path = BASE_DIR / "outputs" / "RA4" / "tac_instructions.json"
        output_dir = BASE_DIR / "outputs" / "RA4"

        # Instancia o otimizador
        optimizer = TACOptimizer()
        
        # Carrega as instruções TAC
        optimizer.carregar_tac(str(tac_path))
        
        # Conta estatísticas antes da otimização
        initial_instructions = len(optimizer.instructions)
        initial_temporaries = optimizer._contar_temporarios()
        
        # Executa a otimização
        stats = optimizer.otimizarTAC(str(tac_path))
        
        # Cria estatísticas compatíveis com o método de relatório
        stats_compat = {
            'initial_instructions': initial_instructions,
            'final_instructions': len(optimizer.instructions),
            'initial_temporaries': initial_temporaries,
            'final_temporaries': optimizer._contar_temporarios(),
            'foldings': stats.get('constant_folding', 0),
            'propagations': stats.get('constant_propagation', 0),
            'dead_code': stats.get('dead_code_elimination', 0),
            'jump_elim': stats.get('jump_elimination', 0),
            'iterations': stats.get('iterations', 0)
        }
        optimizer._gerar_relatorio_otimizacoes_md(arquivo_entrada, stats_compat)

        print(f"    [OK] TAC otimizado com sucesso")
        print(f"    [OK] Instruções originais: {stats_compat['initial_instructions']}")
        print(f"    [OK] Instruções otimizadas: {stats_compat['final_instructions']}")
        if stats_compat['initial_instructions'] > 0:
            reducao = ((stats_compat['initial_instructions'] - stats_compat['final_instructions']) / stats_compat['initial_instructions'] * 100)
            print(f"    [OK] Redução: {reducao:.1f}%")
        else:
            print(f"    [OK] Redução: N/A (nenhuma instrução para otimizar)")
        print(f"    [OK] Arquivos salvos em: {output_dir.relative_to(BASE_DIR)}")
        print("      - tac_otimizado.json")
        print("      - tac_otimizado.md")
        print("      - relatorios/otimizacao_tac.md")

    except FileNotFoundError:
        print(f"  [ERROR] Arquivo de instruções TAC não encontrado")
        print("  Certifique-se de que a geração de TAC (RA4) foi executada corretamente.")
    except Exception as e:
        print(f"  [ERROR] ERRO na otimização de TAC: {e}")
        traceback.print_exc()


def main():
    """Função principal do compilador

    Orquestra todas as fases do compilador:
    1. Resolve caminho do arquivo de entrada
    2. Executa tokenização (RA1)
    3. Valida tokens (RA2)
    4. Constrói gramática e tabela LL(1) (RA2)
    5. Executa parsing (RA2)
    6. Gera árvores sintáticas (RA2)
    7. Executa análise semântica (RA3)
    8. Gera TAC (RA4)
    9. Otimiza TAC (RA4)

    Raises:
        SystemExit: Se houver erro crítico em qualquer fase
    """
    if len(sys.argv) < 2:
        print("ERRO -> Especificar arquivo de teste como argumento")
        print("Uso: python3 compilar.py <arquivo>")
        print("Exemplo: python3 compilar.py teste1_valido.txt")
        sys.exit(1)

    # Validar e carregar arquivo de entrada
    arquivo_entrada = sys.argv[1]

    # Verifica se arquivo existe
    if not os.path.exists(arquivo_entrada):
        print(f"ERRO -> Arquivo não encontrado: {arquivo_entrada}")
        sys.exit(1)

    # Verifica se é um arquivo (não diretório)
    if not os.path.isfile(arquivo_entrada):
        print(f"ERRO -> Caminho especificado é um diretório: {arquivo_entrada}")
        sys.exit(1)

    operacoes_lidas = lerArquivo(arquivo_entrada)
    print(f"\nArquivo de teste: {arquivo_entrada}\n")

    # Fase 1: Tokenização (RA1)
    tokens_salvos_txt, linhas_processadas = executar_ra1_tokenizacao(operacoes_lidas)

    # Fase 2: Validação de tokens (RA2)
    tokens_para_ra2, tokens_sao_validos = executar_ra2_validacao_tokens()

    # Fase 3: Gramática e tabela LL(1) (RA2)
    tabela_ll1 = executar_ra2_gramatica()

    # Fase 4: Parsing (RA2)
    try:
        derivacoes, tokens_por_linha = executar_ra2_parsing(tabela_ll1)
    except Exception as e:
        print(f"  Erro na análise sintática: {e}")
        traceback.print_exc()
        return

    # Fase 5: Geração de árvores sintáticas (RA2)
    executar_ra2_geracao_arvores(derivacoes, tokens_por_linha)

    # Fase 6: Análise semântica (RA3)
    executar_ra3_analise_semantica()

    # Fase 7: Geração de TAC (RA4)
    executar_ra4_geracao_tac()

    # Fase 8: Otimização de TAC (RA4)
    executar_ra4_otimizacao_tac(arquivo_entrada)


if __name__ == "__main__":
    main()