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
# - Execução e validação de expressões RPN
# - Processamento de estruturas de controle (WHILE, FOR, IFELSE)
# - Validação de resultados do código Assembly gerado
#
# STATUS: Não é mais necessário para RA2 (Parser) ou RA3+ (Analisador Semântico)
# MOTIVO: A especificação do RA3 afirma "Nesta fase, não será necessário gerar
#         código Assembly" - análise semântica não requer execução
#
# Este arquivo é mantido para:
# 1. Referência histórica e preservação da nota do RA1
# 2. Possível reutilização futura se validação de execução for necessária
#
# NÃO CORRIJA BUGS neste arquivo a menos que esteja trabalhando especificamente no RA1
# ============================================================================

import math
from .tokens import Token, Tipo_de_Token
from .analisador_lexico import Analisador_Lexico

def parseExpressao(linha_operacao: str):
    analisador_lexico = Analisador_Lexico(linha_operacao)
    tokens = analisador_lexico.analise()
    return tokens

def arredondar_16bit(valor):
    """Simula a precisão de ponto flutuante de 16 bits (duas casas decimais)."""
    try:
        return round(float(valor), 2)
    except (ValueError, TypeError):
        return valor

def encontrar_blocos_controle(tokens: list[Token], inicio: int, num_blocos: int) -> tuple[list, int]:
    """
    Encontra blocos delimitados por parênteses para estruturas de controle.
    Extrai exatamente num_blocos blocos sequenciais começando da posição inicio.

    Args:
        tokens: Lista de tokens
        inicio: Índice para começar a busca
        num_blocos: Número de blocos a extrair

    Returns:
        Tupla com (lista de blocos extraídos, próximo índice após os blocos)
    """
    blocos = []
    idx = inicio

    while idx < len(tokens) and len(blocos) < num_blocos:
        # Pula tokens que não são parênteses de abertura (espaços, etc)
        while idx < len(tokens) and tokens[idx].tipo != Tipo_de_Token.ABRE_PARENTESES:
            idx += 1

        if idx >= len(tokens):
            break

        # Encontrou um parêntese de abertura - extrair bloco completo
        bloco = []
        contagem = 1
        idx += 1  # Pula o parêntese de abertura inicial

        # Coleta todos os tokens até encontrar o parêntese de fechamento correspondente
        while idx < len(tokens) and contagem > 0:
            token_atual = tokens[idx]

            if token_atual.tipo == Tipo_de_Token.ABRE_PARENTESES:
                bloco.append(token_atual)
                contagem += 1
            elif token_atual.tipo == Tipo_de_Token.FECHA_PARENTESES:
                contagem -= 1
                if contagem > 0:
                    # Parêntese interno - adiciona ao bloco
                    bloco.append(token_atual)
                # Se contagem chegou a 0, encontramos o fechamento do bloco - não adiciona
            else:
                bloco.append(token_atual)

            idx += 1

        # Só adiciona o bloco se foi fechado corretamente
        if contagem == 0:
            blocos.append(bloco)
        else:
            # Bloco mal formado - parênteses não balanceados
            print(f"AVISO -> Bloco {len(blocos)+1} tem parênteses não balanceados")
            break

    return blocos, idx

def processarEstruturaControle(tokens: list[Token], memoria: dict) -> float:
    """
    Processa estruturas de controle (IFELSE, WHILE, FOR) em notação PÓS-FIXADA.
    O operador de controle aparece NO FINAL, após os blocos.
    Exemplo: ((condição)(verdadeiro)(falso) IFELSE) - operador por último
    """
    # Busca o operador de controle de TRÁS PARA FRENTE (pós-fixado)
    for i in range(len(tokens) - 1, -1, -1):
        token = tokens[i]
        if token.tipo == Tipo_de_Token.IFELSE:
            return processarIFELSE_posfixado(tokens, i, memoria)
        elif token.tipo == Tipo_de_Token.WHILE:
            return processarWHILE_posfixado(tokens, i, memoria)
        elif token.tipo == Tipo_de_Token.FOR:
            return processarFOR_posfixado(tokens, i, memoria)

    return 0.0

def processarIFELSE_posfixado(tokens: list[Token], pos_ifelse: int, memoria: dict) -> float:
    """
    Processa estrutura IFELSE PÓS-FIXADA: ((condição)(verdadeiro)(falso) IFELSE)

    Args:
        tokens: Lista de tokens da expressão
        pos_ifelse: Posição do token IFELSE (operador no final)
        memoria: Dicionário de variáveis

    Sintaxe: Blocos aparecem ANTES do operador IFELSE
    Exemplo: (((1.0 0.0 >) (10.0) (20.0) IFELSE) RESULTADO_IF)
    """
    try:
        # Extrai tokens ANTES do operador IFELSE
        # Estes tokens já foram processados e não têm os parênteses externos
        # Estrutura esperada: (condição) (verdadeiro) (falso)
        tokens_blocos = tokens[:pos_ifelse]

        # Encontra os 3 blocos necessários: (condição)(verdadeiro)(falso)
        blocos, _ = encontrar_blocos_controle(tokens_blocos, 0, 3)

        if len(blocos) != 3:
            print("ERRO -> IFELSE pós-fixado requer 3 blocos: (condição)(verdadeiro)(falso) IFELSE")
            return 0.0

        # Processa a condição
        condicao = processarTokens(blocos[0], memoria)

        # Executa o bloco apropriado (verdadeiro se != 0)
        if float(condicao) != 0.0:
            resultado = processarTokens(blocos[1], memoria)
            return resultado
        else:
            resultado = processarTokens(blocos[2], memoria)
            return resultado

    except Exception as e:
        print(f"ERRO no IFELSE pós-fixado: {e}")
        return 0.0

def processarWHILE_posfixado(tokens: list[Token], pos_while: int, memoria: dict) -> float:
    """
    Processa estrutura WHILE PÓS-FIXADA: ((condição)(corpo) WHILE)

    Args:
        tokens: Lista de tokens da expressão
        pos_while: Posição do token WHILE (operador no final)
        memoria: Dicionário de variáveis

    Sintaxe: Blocos aparecem ANTES do operador WHILE
    Exemplo: (((X 5.0 <)((X 1.0 +) X) WHILE) LOOP_X)
    """
    try:
        # Extrai tokens ANTES do operador WHILE
        # Estes tokens já foram processados e não têm os parênteses externos
        # Estrutura esperada: (condição) (corpo)
        tokens_blocos = tokens[:pos_while]

        # Encontra os 2 blocos necessários: (condição)(corpo)
        blocos, _ = encontrar_blocos_controle(tokens_blocos, 0, 2)

        if len(blocos) != 2:
            print("ERRO -> WHILE pós-fixado requer 2 blocos: (condição)(corpo) WHILE")
            return 0.0

        resultado = 0.0
        iteracoes = 0
        max_iteracoes = 1000  # Limite de segurança

        while iteracoes < max_iteracoes:
            # Avalia a condição
            condicao = processarTokens(blocos[0], memoria)

            # Se a condição é falsa, sai do loop
            if float(condicao) == 0.0:
                break

            # Executa o corpo do loop
            resultado = executarCorpoLoop(blocos[1], memoria)
            iteracoes += 1

        return resultado

    except Exception as e:
        print(f"ERRO no WHILE pós-fixado: {e}")
        return 0.0

def processarFOR_posfixado(tokens: list[Token], pos_for: int, memoria: dict) -> float:
    """
    Processa estrutura FOR PÓS-FIXADA: ((inicial)(final)(incremento)(corpo) FOR)

    Args:
        tokens: Lista de tokens da expressão
        pos_for: Posição do token FOR (operador no final)
        memoria: Dicionário de variáveis

    Sintaxe: Blocos aparecem ANTES do operador FOR
    Exemplo: (((1.0)(10.0)(1.0)((I 1.0 +) SOMA) FOR) RESULTADO_FOR)
    """
    try:
        # Extrai tokens ANTES do operador FOR
        # Estes tokens já foram processados e não têm os parênteses externos
        # Estrutura esperada: (inicial) (final) (incremento) (corpo)
        tokens_blocos = tokens[:pos_for]

        # Encontra os 4 blocos necessários: (inicial)(final)(incremento)(corpo)
        blocos, _ = encontrar_blocos_controle(tokens_blocos, 0, 4)

        if len(blocos) != 4:
            print("ERRO -> FOR pós-fixado requer 4 blocos: (inicial)(final)(incremento)(corpo) FOR")
            return 0.0

        # Avalia os parâmetros do FOR
        inicial = int(processarTokens(blocos[0], memoria))
        final = int(processarTokens(blocos[1], memoria))
        incremento = int(processarTokens(blocos[2], memoria)) or 1

        resultado = 0.0
        contador = inicial
        iteracoes = 0
        max_iteracoes = 1000  # Limite de segurança

        # Cria uma variável de controle implícita para o loop
        memoria['_FOR_COUNTER'] = float(contador)

        while contador < final and iteracoes < max_iteracoes:
            # Atualiza a variável de controle
            memoria['_FOR_COUNTER'] = float(contador)

            # Executa o corpo do loop
            resultado = executarCorpoLoop(blocos[3], memoria)

            contador += incremento
            iteracoes += 1

        # Remove a variável de controle temporária
        if '_FOR_COUNTER' in memoria:
            del memoria['_FOR_COUNTER']

        return resultado

    except Exception as e:
        print(f"ERRO no FOR pós-fixado: {e}")
        return 0.0

def executarCorpoLoop(tokens_corpo: list[Token], memoria: dict) -> float:
    """
    Executa o corpo de um loop, que pode conter múltiplas expressões.
    Exemplo: ((X X 1 +)(Y X 2 *)) -> executa duas expressões sequenciais
    """
    if not tokens_corpo:
        return 0.0
    
    # Separa as expressões individuais
    expressoes = []
    i = 0
    
    while i < len(tokens_corpo):
        if tokens_corpo[i].tipo == Tipo_de_Token.ABRE_PARENTESES:
            # Encontra uma expressão delimitada por parênteses
            contagem = 1
            j = i + 1
            expressao = []
            
            while j < len(tokens_corpo) and contagem > 0:
                token_atual = tokens_corpo[j]
                
                if token_atual.tipo == Tipo_de_Token.ABRE_PARENTESES:
                    contagem += 1
                elif token_atual.tipo == Tipo_de_Token.FECHA_PARENTESES:
                    contagem -= 1
                    
                if contagem > 0:
                    expressao.append(token_atual)
                    
                j += 1
            
            if expressao:
                expressoes.append(expressao)
            
            i = j
        else:
            i += 1
    
    # Executa todas as expressões sequencialmente
    resultado = 0.0
    
    for expressao in expressoes:
        # Verifica se é uma atribuição de variável e inicializa se necessário (nova sintaxe: VALOR VARIAVEL)
        if len(expressao) >= 1 and expressao[-1].tipo == Tipo_de_Token.VARIAVEL:
            var_nome = expressao[-1].valor
            if var_nome not in memoria:
                memoria[var_nome] = 0.0
        
        # Adiciona parênteses de volta para processamento correto
        expressao_completa = [Token(Tipo_de_Token.ABRE_PARENTESES, '(')] + expressao + [Token(Tipo_de_Token.FECHA_PARENTESES, ')')]
        resultado = executarExpressao(expressao_completa, memoria)
    
    # Se não encontrou expressões delimitadas, processa todos os tokens como uma única expressão
    if not expressoes:
        resultado = processarTokens(tokens_corpo, memoria)
    
    return resultado

def executarExpressao(tokens: list[Token], memoria: dict) -> float:
    """
    Executa uma expressão RPN de forma recursiva, lidando corretamente com expressões aninhadas.
    """
    if not tokens:
        return 0.0

    # Remove apenas tokens FIM e parênteses EXTERNOS (primeiro e último)
    tokens_sem_fim = [token for token in tokens if token.tipo != Tipo_de_Token.FIM]

    # Remove parênteses externos se existirem
    if (len(tokens_sem_fim) >= 2 and
        tokens_sem_fim[0].tipo == Tipo_de_Token.ABRE_PARENTESES and
        tokens_sem_fim[-1].tipo == Tipo_de_Token.FECHA_PARENTESES):
        tokens_limpos = tokens_sem_fim[1:-1]
    else:
        tokens_limpos = tokens_sem_fim

    if not tokens_limpos:
        return 0.0
    
    # Verifica se é uma atribuição de variável simples (NUMERO VARIAVEL)
    if (len(tokens_limpos) == 2 and 
        tokens_limpos[0].tipo == Tipo_de_Token.NUMERO_REAL and 
        tokens_limpos[1].tipo == Tipo_de_Token.VARIAVEL):
        
        valor = float(tokens_limpos[0].valor)
        var_nome = tokens_limpos[1].valor
        memoria[var_nome] = valor
        
        return valor
    
    # Verifica se contém estruturas de controle primeiro
    for token in tokens_limpos:
        if token.tipo in [Tipo_de_Token.IFELSE, Tipo_de_Token.WHILE, Tipo_de_Token.FOR]:
            return processarEstruturaControle(tokens_limpos, memoria)
    
    # Verifica se é uma atribuição com expressão aninhada (EXPRESSAO VARIAVEL)
    if (len(tokens_limpos) >= 2 and 
        tokens_limpos[-1].tipo == Tipo_de_Token.VARIAVEL):
        
        var_nome = tokens_limpos[-1].valor
        # Processa a expressão (todos os tokens exceto o último que é a variável)
        resultado = processarTokens(tokens_limpos[:-1], memoria)
        memoria[var_nome] = resultado
                
        return resultado
    
    # Caso contrário, processa normalmente
    resultado = processarTokens(tokens_limpos, memoria)
    
    # Não adiciona ao histórico aqui, pois já foi adicionado nas atribuições
    return resultado

def processarTokens(tokens: list[Token], memoria: dict) -> float:
    """
    Processa uma lista de tokens em notação RPN.
    """
    if not tokens:
        return 0.0
    
    # Se há apenas um token
    if len(tokens) == 1:
        token = tokens[0]
        if token.tipo == Tipo_de_Token.NUMERO_REAL:
            return float(token.valor)
        elif token.tipo == Tipo_de_Token.VARIAVEL:
            return memoria.get(token.valor, 0.0)
        elif token.tipo == Tipo_de_Token.RES:
            hist = memoria.get('historico_resultados', [])
            return hist[-1] if hist else 0.0
        return 0.0
    
    # Caso especial: índice + RES (ex: 3 RES)
    if (len(tokens) == 2 and 
        tokens[0].tipo == Tipo_de_Token.NUMERO_REAL and 
        tokens[1].tipo == Tipo_de_Token.RES):
        
        idx = int(float(tokens[0].valor))
        hist = memoria.get('historico_resultados', [])
        if hist and 0 < idx <= len(hist):
            resultado = hist[-idx]

            return resultado
        else:
            print(f"ERRO -> Índice {idx} fora do intervalo do histórico (tamanho: {len(hist)})")
            return 0.0
    
    # Processa expressões aninhadas primeiro
    tokens_expandidos = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token.tipo == Tipo_de_Token.ABRE_PARENTESES:
            # Encontra o bloco correspondente
            contagem = 1
            j = i + 1
            sub_tokens = []
            
            while j < len(tokens) and contagem > 0:
                if tokens[j].tipo == Tipo_de_Token.ABRE_PARENTESES:
                    contagem += 1
                elif tokens[j].tipo == Tipo_de_Token.FECHA_PARENTESES:
                    contagem -= 1
                
                if contagem > 0:
                    sub_tokens.append(tokens[j])
                j += 1
            
            # Processa a subexpressão
            if sub_tokens:
                resultado = processarTokens(sub_tokens, memoria)
                # Cria um token com o resultado
                token_resultado = Token(Tipo_de_Token.NUMERO_REAL, resultado)
                tokens_expandidos.append(token_resultado)
            
            i = j
        else:
            tokens_expandidos.append(token)
            i += 1
    
    # Agora processa com uma pilha RPN tradicional
    pilha = []
    
    for token in tokens_expandidos:
        if token.tipo == Tipo_de_Token.NUMERO_REAL:
            pilha.append(float(token.valor))
            
        elif token.tipo == Tipo_de_Token.VARIAVEL:
            valor = memoria.get(token.valor, 0.0)
            pilha.append(valor)
            
        elif token.tipo == Tipo_de_Token.RES:
            # Verifica se há um índice na pilha
            if pilha and isinstance(pilha[-1], (int, float)):
                idx = int(pilha.pop())
                hist = memoria.get('historico_resultados', [])
                if hist and 0 < idx <= len(hist):
                    pilha.append(hist[-idx])
                else:
                    print(f"ERRO -> Índice {idx} fora do intervalo do histórico (tamanho: {len(hist)})")
                    pilha.append(0.0)
            else:
                # Sem índice, retorna o último resultado
                hist = memoria.get('historico_resultados', [])
                if hist:
                    pilha.append(hist[-1])
                else:
                    print("ERRO -> Histórico vazio")
                    pilha.append(0.0)
                
        elif str(token.valor) in ['+', '-', '*', '/', '|', '%', '^']:
            if len(pilha) >= 2:
                b = pilha.pop()
                a = pilha.pop()
                
                try:
                    if token.valor == '+': resultado = a + b
                    elif token.valor == '-': resultado = a - b
                    elif token.valor == '*': resultado = a * b
                    elif token.valor == '/': resultado = int(a / b) if b != 0 else 0.0  # Divisão INTEIRA
                    elif token.valor == '|': resultado = a / b if b != 0 else 0.0  # Divisão REAL
                    elif token.valor == '%': resultado = a % b if b != 0 else 0.0
                    elif token.valor == '^': resultado = math.pow(a, b)
                    
                    pilha.append(arredondar_16bit(resultado))
                except (ZeroDivisionError, ValueError, OverflowError):
                    pilha.append(0.0)
            else:
                print(f"ERRO -> Tokens insuficientes para o operador '{token.valor}'")
                pilha.append(0.0)
                
        elif str(token.valor) in ['<', '>', '==', '<=', '>=', '!=']:
            if len(pilha) >= 2:
                b = pilha.pop()
                a = pilha.pop()
                
                try:
                    # Garante que os valores sejam numéricos
                    a_num = float(a)
                    b_num = float(b)
                    
                    if token.valor == '<': resultado = 1.0 if a_num < b_num else 0.0
                    elif token.valor == '>': resultado = 1.0 if a_num > b_num else 0.0
                    elif token.valor == '==': resultado = 1.0 if abs(a_num - b_num) < 1e-10 else 0.0
                    elif token.valor == '<=': resultado = 1.0 if a_num <= b_num else 0.0
                    elif token.valor == '>=': resultado = 1.0 if a_num >= b_num else 0.0
                    elif token.valor == '!=': resultado = 1.0 if abs(a_num - b_num) >= 1e-10 else 0.0
                    else: resultado = 0.0
                    
                    pilha.append(resultado)
                except (ValueError, TypeError) as e:
                    print(f"ERRO na comparação {token.valor}: {e}")
                    pilha.append(0.0)
            else:
                print(f"ERRO -> Tokens insuficientes para o operador '{token.valor}'")
                pilha.append(0.0)
                
        elif str(token.valor) in ['&&', '||']:
            if len(pilha) >= 2:
                b = pilha.pop()
                a = pilha.pop()
                
                try:
                    # Converte para booleano: 0 = falso, qualquer outro valor = verdadeiro
                    a_bool = float(a) != 0.0
                    b_bool = float(b) != 0.0
                    
                    if token.valor == '&&': resultado = 1.0 if a_bool and b_bool else 0.0
                    elif token.valor == '||': resultado = 1.0 if a_bool or b_bool else 0.0
                    else: resultado = 0.0
                    
                    pilha.append(resultado)
                except (ValueError, TypeError) as e:
                    print(f"ERRO na operação lógica {token.valor}: {e}")
                    pilha.append(0.0)
            else:
                print(f"ERRO -> Tokens insuficientes para o operador '{token.valor}'")
                pilha.append(0.0)
                
        elif str(token.valor) == '!':
            if len(pilha) >= 1:
                a = pilha.pop()
                try:
                    # NOT lógico: 0 vira 1, qualquer outro valor vira 0
                    resultado = 1.0 if float(a) == 0.0 else 0.0
                    pilha.append(resultado)
                except (ValueError, TypeError) as e:
                    print(f"ERRO na operação NOT: {e}")
                    pilha.append(0.0)
            else:
                print("ERRO -> Token insuficiente para o operador '!'")
                pilha.append(0.0)
    
    return arredondar_16bit(pilha[-1] if pilha else 0.0)
