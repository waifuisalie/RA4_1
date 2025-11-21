"""
Percorredor AST - Percurso pós-ordem para geração TAC.
"""

from typing import List, Dict, Any, Optional
from .gerenciador_tac import GerenciadorTAC
from .instrucoes_tac import (
    InstrucaoTAC,
    TACAtribuicao,
    TACCopia,
    TACOperacaoBinaria,
    TACOperacaoUnaria,
    TACRotulo,
    TACDesvio,
    TACSeNaoDesvio,
)


class PercorredorAST:
    """Percorre a AST em pós-ordem gerando instruções TAC."""

    def __init__(self, gerenciador: GerenciadorTAC):
        self.gerenciador = gerenciador
        self.instrucoes: List[InstrucaoTAC] = []
        self._historico_resultados: List[str] = []

    def gerar_tac(self, dicionario_ast: Dict[str, Any]) -> List[InstrucaoTAC]:
        """Gera TAC a partir da AST atribuída."""
        self.instrucoes = []
        self._historico_resultados = []

        arvore = dicionario_ast.get("arvore_atribuida", [])
        for no_linha in arvore:
            temp_resultado = self._processar_no(no_linha)
            if temp_resultado:
                self._historico_resultados.append(temp_resultado)

        return self.instrucoes

    def _processar_no(self, no: Dict[str, Any]) -> Optional[str]:
        """Processa um nó em pós-ordem (filhos antes do pai)."""
        if not no:
            return None

        tipo_vertice = no.get("tipo_vertice")
        numero_linha = no.get("numero_linha", 0)

        # Valor literal
        if "valor" in no and not no.get("filhos"):
            return self._tratar_literal(no)

        # Operações aritméticas
        if tipo_vertice == "ARITH_OP":
            return self._tratar_op_aritmetica(no)

        # Operações de comparação
        elif tipo_vertice == "COMP_OP":
            return self._tratar_op_comparacao(no)

        # Operações lógicas
        elif tipo_vertice == "LOGIC_OP":
            return self._tratar_op_logica(no)

        # Fluxo de controle
        elif tipo_vertice == "CONTROL_OP":
            return self._tratar_fluxo_controle(no)

        # Wrapper LINHA
        elif tipo_vertice == "LINHA":
            filhos = no.get("filhos", [])

            if not filhos:
                return None

            if len(filhos) == 1:
                return self._processar_no(filhos[0])

            elif len(filhos) == 2:
                return self._tratar_atribuicao_variavel(no)

            else:
                resultado = None
                for filho in filhos:
                    resultado = self._processar_no(filho)
                return resultado

        else:
            raise ValueError(f"Tipo de nó desconhecido: {tipo_vertice} na linha {numero_linha}")

    # --- LITERAIS E OPERAÇÕES ---

    def _tratar_literal(self, no: Dict[str, Any]) -> str:
        """Trata literais: temp = valor"""
        valor = no["valor"]
        numero_linha = no.get("numero_linha", 0)
        subtipo = no.get("subtipo", "")

        # Determina tipo
        if "real" in subtipo:
            tipo_dado = "real"
        elif "inteiro" in subtipo:
            tipo_dado = "int"
        elif subtipo == "variavel":
            return valor
        else:
            tipo_dado = None

        temp = self.gerenciador.nova_temp()
        self.instrucoes.append(TACAtribuicao(temp, valor, numero_linha, tipo_dado))
        return temp

    def _tratar_op_aritmetica(self, no: Dict[str, Any]) -> str:
        """Trata operações: +, -, *, /, |, %, ^"""
        operador = no["operador"]
        filhos = no["filhos"]
        numero_linha = no.get("numero_linha", 0)
        tipo_inferido = no.get("tipo_inferido")

        if len(filhos) != 2:
            raise ValueError(f"Operação aritmética requer 2 operandos na linha {numero_linha}")

        temp_esquerdo = self._processar_no(filhos[0])
        temp_direito = self._processar_no(filhos[1])

        temp_resultado = self.gerenciador.nova_temp()
        self.instrucoes.append(
            TACOperacaoBinaria(temp_resultado, temp_esquerdo, operador, temp_direito, numero_linha, tipo_inferido)
        )
        return temp_resultado

    def _tratar_op_comparacao(self, no: Dict[str, Any]) -> str:
        """Trata comparações: >, <, >=, <=, ==, !="""
        filhos = no["filhos"]
        numero_linha = no.get("numero_linha", 0)
        operador = no.get("operador", "")

        temp_esquerdo = self._processar_no(filhos[0])
        temp_direito = self._processar_no(filhos[1])

        temp_resultado = self.gerenciador.nova_temp()
        self.instrucoes.append(
            TACOperacaoBinaria(temp_resultado, temp_esquerdo, operador, temp_direito, numero_linha, "boolean")
        )
        return temp_resultado

    def _tratar_op_logica(self, no: Dict[str, Any]) -> str:
        """Trata operações lógicas: &&, ||, !"""
        filhos = no["filhos"]
        numero_linha = no.get("numero_linha", 0)
        operador = no.get("operador", "")

        # NOT unário
        if operador == "!":
            if len(filhos) != 1:
                raise ValueError(f"NOT requer 1 operando na linha {numero_linha}")

            temp_operando = self._processar_no(filhos[0])
            temp_resultado = self.gerenciador.nova_temp()
            self.instrucoes.append(
                TACOperacaoUnaria(temp_resultado, operador, temp_operando, numero_linha, "boolean")
            )
            return temp_resultado

        # Binários && e ||
        if len(filhos) != 2:
            raise ValueError(f"Operador '{operador}' requer 2 operandos na linha {numero_linha}")

        temp_esquerdo = self._processar_no(filhos[0])
        temp_direito = self._processar_no(filhos[1])

        temp_resultado = self.gerenciador.nova_temp()
        self.instrucoes.append(
            TACOperacaoBinaria(temp_resultado, temp_esquerdo, operador, temp_direito, numero_linha, "boolean")
        )
        return temp_resultado

    # --- FLUXO DE CONTROLE ---

    def _tratar_fluxo_controle(self, no: Dict[str, Any]) -> Optional[str]:
        """Despacha para IFELSE, WHILE ou FOR."""
        operador = no.get("operador", "")
        numero_linha = no.get("numero_linha", 0)

        if operador == "IFELSE":
            return self._tratar_ifelse(no)
        elif operador == "WHILE":
            return self._tratar_while(no)
        elif operador == "FOR":
            return self._tratar_for(no)
        else:
            raise ValueError(f"Operador de controle desconhecido '{operador}' na linha {numero_linha}")

    def _tratar_ifelse(self, no: Dict[str, Any]) -> Optional[str]:
        """Trata IFELSE: condição, então, senão."""
        filhos = no["filhos"]
        numero_linha = no.get("numero_linha", 0)

        if len(filhos) != 3:
            raise ValueError(f"IFELSE requer 3 operandos na linha {numero_linha}")

        no_condicao, no_entao, no_senao = filhos

        rotulo_senao = self.gerenciador.novo_rotulo()
        rotulo_fim = self.gerenciador.novo_rotulo()

        temp_cond = self._processar_no(no_condicao)
        self.instrucoes.append(TACSeNaoDesvio(temp_cond, rotulo_senao, numero_linha))

        temp_entao = self._processar_no(no_entao)
        self.instrucoes.append(TACDesvio(rotulo_fim, numero_linha))

        self.instrucoes.append(TACRotulo(rotulo_senao, numero_linha))
        temp_senao = self._processar_no(no_senao)

        self.instrucoes.append(TACRotulo(rotulo_fim, numero_linha))
        return temp_senao

    def _tratar_while(self, no: Dict[str, Any]) -> Optional[str]:
        """Trata WHILE: condição, corpo."""
        filhos = no["filhos"]
        numero_linha = no.get("numero_linha", 0)

        if len(filhos) != 2:
            raise ValueError(f"WHILE requer 2 operandos na linha {numero_linha}")

        no_condicao, no_corpo = filhos

        rotulo_inicio = self.gerenciador.novo_rotulo()
        rotulo_fim = self.gerenciador.novo_rotulo()

        self.instrucoes.append(TACRotulo(rotulo_inicio, numero_linha))

        temp_cond = self._processar_no(no_condicao)
        self.instrucoes.append(TACSeNaoDesvio(temp_cond, rotulo_fim, numero_linha))

        self._processar_no(no_corpo)
        self.instrucoes.append(TACDesvio(rotulo_inicio, numero_linha))

        self.instrucoes.append(TACRotulo(rotulo_fim, numero_linha))
        return None

    def _tratar_for(self, no: Dict[str, Any]) -> Optional[str]:
        """Trata FOR: inicio, fim, passo, corpo."""
        filhos = no["filhos"]
        numero_linha = no.get("numero_linha", 0)

        if len(filhos) != 4:
            raise ValueError(f"FOR requer 4 operandos na linha {numero_linha}")

        no_inicio, no_fim, no_passo, no_corpo = filhos

        rotulo_inicio = self.gerenciador.novo_rotulo()
        rotulo_fim = self.gerenciador.novo_rotulo()

        temp_atual = self._processar_no(no_inicio)
        temp_fim = self._processar_no(no_fim)
        temp_passo = self._processar_no(no_passo)

        contador_laco = self.gerenciador.nova_temp()
        self.instrucoes.append(TACCopia(contador_laco, temp_atual, numero_linha, "int"))

        self.instrucoes.append(TACRotulo(rotulo_inicio, numero_linha))

        temp_cond = self.gerenciador.nova_temp()
        self.instrucoes.append(
            TACOperacaoBinaria(temp_cond, contador_laco, "<=", temp_fim, numero_linha, "boolean")
        )
        self.instrucoes.append(TACSeNaoDesvio(temp_cond, rotulo_fim, numero_linha))

        self._processar_no(no_corpo)

        novo_contador = self.gerenciador.nova_temp()
        self.instrucoes.append(
            TACOperacaoBinaria(novo_contador, contador_laco, "+", temp_passo, numero_linha, "int")
        )
        self.instrucoes.append(TACCopia(contador_laco, novo_contador, numero_linha, "int"))

        self.instrucoes.append(TACDesvio(rotulo_inicio, numero_linha))
        self.instrucoes.append(TACRotulo(rotulo_fim, numero_linha))
        return None

    # --- ATRIBUIÇÃO E RES ---

    def _tratar_atribuicao_variavel(self, no: Dict[str, Any]) -> str:
        """Trata atribuição: (valor variavel) -> variavel = valor"""
        filhos = no["filhos"]
        numero_linha = no.get("numero_linha", 0)

        if len(filhos) < 2:
            resultado = None
            for filho in filhos:
                resultado = self._processar_no(filho)
            return resultado

        no_valor = filhos[0]
        no_var = filhos[1]

        if no_var.get("valor") == "RES":
            return self._tratar_comando_res(no)

        if no_var.get("subtipo") != "variavel":
            resultado = None
            for filho in filhos:
                resultado = self._processar_no(filho)
            return resultado

        temp_valor = self._processar_no(no_valor)
        nome_var = no_var["valor"]
        tipo_dado = no_valor.get("tipo_inferido")

        self.instrucoes.append(TACCopia(nome_var, temp_valor, numero_linha, tipo_dado))
        return temp_valor

    def _tratar_comando_res(self, no: Dict[str, Any]) -> str:
        """Trata RES: obtém resultado histórico pelo índice."""
        filhos = no["filhos"]
        numero_linha = no.get("numero_linha", 0)

        no_indice = filhos[0]
        valor_indice = no_indice.get("valor", "0")

        try:
            indice = int(valor_indice)
        except ValueError:
            raise ValueError(f"Índice RES deve ser inteiro na linha {numero_linha}")

        if indice < 0 or indice >= len(self._historico_resultados):
            raise ValueError(f"Índice RES {indice} fora dos limites na linha {numero_linha}")

        temp_historico = self._historico_resultados[indice]
        temp_resultado = self.gerenciador.nova_temp()
        self.instrucoes.append(TACCopia(temp_resultado, temp_historico, numero_linha, None))
        return temp_resultado

    # --- UTILITÁRIOS ---

    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas da geração."""
        stats = self.gerenciador.obter_estatisticas()
        return {
            "total_instrucoes": len(self.instrucoes),
            "contador_temp": stats["contador_temp_atual"],
            "contador_rotulo": stats["contador_rotulo_atual"],
            "tamanho_historico_resultados": len(self._historico_resultados)
        }

    def __repr__(self) -> str:
        stats = self.obter_estatisticas()
        return f"PercorredorAST(instrucoes={stats['total_instrucoes']}, temps={stats['contador_temp']}, rotulos={stats['contador_rotulo']})"
