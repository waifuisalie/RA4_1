#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

# ============================================================================
# LEGACY CODE - RA1 PHASE ONLY
# ============================================================================
# Este módulo foi usado na RA1 (Fase de Análise Léxica) para:
# - Tokenização de expressões RPN (AINDA NECESSÁRIO para RA2/RA3)
# - Execução e exibição de resultados (NÃO MAIS NECESSÁRIO)
#
# STATUS: Parcialmente legacy - a função executarExpressao() não é mais usada
# MOTIVO: RA3 não requer execução de expressões, apenas análise semântica
#
# NOTA: A tokenização (parseExpressao) ainda é necessária para gerar
#       tokens_gerados.txt que é entrada para RA2 e RA3
#
# Este arquivo é mantido para referência histórica do RA1
# ============================================================================

import io
import sys
from pathlib import Path
from src.RA1.functions.python.rpn_calc import parseExpressao, executarExpressao
from src.RA1.functions.python.io_utils import salvar_tokens
from src.RA1.functions.python.tokens import Tipo_de_Token

def criarMensagemErro(linha: str, numero_linha: int, tipo_erro: str, detalhes: str = "") -> str:
    """Cria mensagem de erro formatada para exibição"""
    erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
    erro += f"    ERRO DE {tipo_erro}: {detalhes}"
    return erro

def exibirResultados(vetor_linhas: list[str], out_tokens: Path) -> tuple[bool, int, int]:
    
    memoria_global = {}
    tokens_salvos_txt = []
    contador_erros = 0
    linhas_processadas = 0

    # Inicializar o histórico na memória global
    memoria_global['historico_resultados'] = []

    for i, linha in enumerate(vetor_linhas, 1):
        # Pula linhas vazias ou comentários
        if not linha.strip() or linha.strip().startswith('#'):
            continue

        linhas_processadas += 1

        try:
            lista_de_tokens = parseExpressao(linha)
            # para salvar tokens completos (incluindo parênteses) para RA2
            tokens_completos = [str(token.valor) for token in lista_de_tokens if token.tipo != Tipo_de_Token.FIM]
            tokens_salvos_txt.append(tokens_completos)

            # Captura saída para detectar erros do RA1
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            try:
                resultado = executarExpressao(lista_de_tokens, memoria_global)
                sys.stdout = old_stdout

                # Verifica se houve erro capturado
                output = buffer.getvalue()

                # Detecta se é uma CONSULTA RES PURA (não deve adicionar ao histórico)
                # Formato: ( NUMERO RES ) -> tokens = [ABRE, NUMERO, RES, FECHA, FIM]
                is_res_query = False
                tokens_sem_fim = [t for t in lista_de_tokens if t.tipo != Tipo_de_Token.FIM]

                if len(tokens_sem_fim) == 4:  # ( NUMERO RES )
                    if (tokens_sem_fim[0].tipo == Tipo_de_Token.ABRE_PARENTESES and
                        tokens_sem_fim[1].tipo == Tipo_de_Token.NUMERO_REAL and
                        tokens_sem_fim[2].tipo == Tipo_de_Token.RES and
                        tokens_sem_fim[3].tipo == Tipo_de_Token.FECHA_PARENTESES):
                        is_res_query = True

                if 'ERRO' in output:
                    print(f"Linha {i:02d}: Expressão '{linha}' -> Resultado: {resultado}")
                    # Formata o erro com indentação
                    erro_lines = output.strip().split('\n')
                    for erro_line in erro_lines:
                        if erro_line.strip():
                            print(f"    {erro_line}")
                    contador_erros += 1
                else:
                    print(f"Linha {i:02d}: Expressão '{linha}' -> Resultado: {resultado}")

                # Só adiciona ao histórico se NÃO for uma consulta RES pura
                if not is_res_query:
                    memoria_global['historico_resultados'].append(resultado)
            except Exception as exec_error:
                sys.stdout = old_stdout
                raise exec_error
            
        except ValueError as e:
            print(criarMensagemErro(linha, i, "SINTAXE", str(e)))
            tokens_salvos_txt.append([])  # Adiciona lista vazia para manter índices
            memoria_global['historico_resultados'].append(None)  # Adiciona None para erro
            contador_erros += 1
            
        except ZeroDivisionError:
            print(criarMensagemErro(linha, i, "MATEMÁTICO", "Divisão por zero"))
            tokens_salvos_txt.append([])
            memoria_global['historico_resultados'].append(None)
            contador_erros += 1
            
        except Exception as e:
            print(criarMensagemErro(linha, i, "INESPERADO", f"{type(e).__name__}: {e}"))
            tokens_salvos_txt.append([])
            memoria_global['historico_resultados'].append(None)
            contador_erros += 1

    # Salva os tokens gerados
    salvar_tokens(tokens_salvos_txt, out_tokens)
    
    # Retorna (sucesso, linhas_processadas, contador_erros)
    return (contador_erros == 0, linhas_processadas, contador_erros)