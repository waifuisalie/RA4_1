#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

from pathlib import Path

def lerArquivo(nomeArquivo: str):
    try:
        with open(nomeArquivo, 'r', encoding="utf-8") as arquivos_teste:
            return [linha.strip() for linha in arquivos_teste if linha.strip()]
    except FileNotFoundError:
        print(f'ERRO -> Arquivo não encontrado: {nomeArquivo}')
        return []

from pathlib import Path

def salvar_tokens(tokens_por_linha, nome_arquivo: str | Path) -> bool:
    try:
        destino = Path(nome_arquivo)

        # Cria a pasta se necessário
        destino.parent.mkdir(parents=True, exist_ok=True)

        with destino.open("w", encoding='utf-8') as f:
            for lista_de_tokens in tokens_por_linha:
                f.write(" ".join(lista_de_tokens) + "\n")

        return True
    except Exception as e:
        print(f'ERRO -> Falha ao escrever os tokens no arquivo: {e}')
        return False

