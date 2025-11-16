#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

from .tokens import Token, Tipo_de_Token

class Analisador_Lexico:
    def __init__(self, texto_fonte: str):
        self.texto_fonte = texto_fonte
        self.ponteiro = 0
        self.caractere = self.texto_fonte[self.ponteiro] if self.texto_fonte else None
        self.resultado = ""

    def avanca_ponteiro(self):
        self.ponteiro += 1
        if self.ponteiro < len(self.texto_fonte):
            self.caractere = self.texto_fonte[self.ponteiro]
        else:
            self.caractere = None
        # Debug
        #print(f'Ponteiro: {self.ponteiro}, Caractere: {self.caractere}')

    def ignora_espaco(self):
        while self.caractere is not None and self.caractere.isspace():
            self.avanca_ponteiro()

    def analise(self):
        tokens = []
        while self.caractere is not None:
            token = self.estado_zero()
            if token:
                tokens.append(token)
        tokens.append(Token(Tipo_de_Token.FIM, None))
        return tokens

    def estado_zero(self):
        self.ignora_espaco()
        if self.caractere is None:
            return None
        if self.caractere.isalpha():
            return self.estado_comando()
        if self.caractere.isdigit():
            return self.estado_numero()
        return self.estado_operador()

    def estado_operador(self):
        token = None
        caractere_atual = self.caractere  # Armazena o caractere atual
        
        if self.caractere == '(':
            token = Token(Tipo_de_Token.ABRE_PARENTESES, '(')
            self.avanca_ponteiro()
        elif self.caractere == ')':
            token = Token(Tipo_de_Token.FECHA_PARENTESES, ')')
            self.avanca_ponteiro()
        elif self.caractere == '+':
            token = Token(Tipo_de_Token.SOMA, '+')
            self.avanca_ponteiro()
        elif self.caractere == '-':
            token = Token(Tipo_de_Token.SUBTRACAO, '-')
            self.avanca_ponteiro()
        elif self.caractere == '*':
            token = Token(Tipo_de_Token.MULTIPLICACAO, '*')
            self.avanca_ponteiro()
        elif self.caractere == '/':
            token = Token(Tipo_de_Token.DIVISAO_INTEIRA, '/')
            self.avanca_ponteiro()
        elif self.caractere == '%':
            token = Token(Tipo_de_Token.RESTO, '%')
            self.avanca_ponteiro()
        elif self.caractere == '^':
            token = Token(Tipo_de_Token.POTENCIA, '^')
            self.avanca_ponteiro()
        elif self.caractere == '<':
            self.avanca_ponteiro()
            if self.caractere == '=':
                token = Token(Tipo_de_Token.MENOR_IGUAL, '<=')
                self.avanca_ponteiro()
            else:
                token = Token(Tipo_de_Token.MENOR, '<')
        elif self.caractere == '>':
            self.avanca_ponteiro()
            if self.caractere == '=':
                token = Token(Tipo_de_Token.MAIOR_IGUAL, '>=')
                self.avanca_ponteiro()
            else:
                token = Token(Tipo_de_Token.MAIOR, '>')
        elif self.caractere == '=':
            self.avanca_ponteiro()
            if self.caractere == '=':
                token = Token(Tipo_de_Token.IGUAL, '==')
                self.avanca_ponteiro()
            else:
                raise ValueError("ERRO -> Esperado '=' após '='")
        elif self.caractere == '!':
            self.avanca_ponteiro()
            if self.caractere == '=':
                token = Token(Tipo_de_Token.DIFERENTE, '!=')
                self.avanca_ponteiro()
            else:
                token = Token(Tipo_de_Token.NOT, '!')
        elif self.caractere == '|':
            self.avanca_ponteiro()
            if self.caractere == '|':
                token = Token(Tipo_de_Token.OR, '||')
                self.avanca_ponteiro()
            else:
                token = Token(Tipo_de_Token.DIVISAO_REAL, '|')
        elif self.caractere == '&':
            self.avanca_ponteiro()
            if self.caractere == '&':
                token = Token(Tipo_de_Token.AND, '&&')
                self.avanca_ponteiro()
            else:
                raise ValueError("ERRO -> Esperado '&' após '&'")
        if token:
            return token
        raise ValueError(f"ERRO -> Caractere inválido: '{self.caractere}'")

    def estado_numero(self):
        resultado = ""
        while self.caractere is not None and self.caractere.isdigit():
            resultado += self.caractere
            self.avanca_ponteiro()
        if self.caractere == '.':
            resultado += self.caractere
            self.avanca_ponteiro()
            if not (self.caractere and self.caractere.isdigit()):
                raise ValueError("ERRO -> Espera-se dígito após o ponto decimal.")
            while self.caractere is not None and self.caractere.isdigit():
                resultado += self.caractere
                self.avanca_ponteiro()
            return Token(Tipo_de_Token.NUMERO_REAL, float(resultado))
        else:
            # Número sem ponto decimal - é inteiro
            return Token(Tipo_de_Token.NUMERO_INTEIRO, int(resultado))

    def estado_comando(self):
        resultado = ""
        while self.caractere is not None and (self.caractere.isalpha() or self.caractere.isdigit() or self.caractere == '_'):
            resultado += self.caractere
            self.avanca_ponteiro()
            
        # Lista de palavras-chave
        palavras_chave = {
            "RES": Tipo_de_Token.RES,
            "WHILE": Tipo_de_Token.WHILE,
            "FOR": Tipo_de_Token.FOR,
            "IFELSE": Tipo_de_Token.IFELSE
        }
        
        # Verifica se é uma palavra-chave
        if resultado in palavras_chave:
            return Token(palavras_chave[resultado], resultado)
        else:
            # Qualquer sequência não reconhecida é considerada uma variável
            return Token(Tipo_de_Token.VARIAVEL, resultado)