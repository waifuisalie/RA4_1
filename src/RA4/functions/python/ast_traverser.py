#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA4_1

"""
Traversador de AST - Percurso Pós-Ordem para Geração de TAC

Implementa o motor de travessia da AST atribuída da Fase 3,
gerando instruções TAC (Three Address Code).

A travessia é feita em PÓS-ORDEM (bottom-up), visitando filhos antes dos pais.
"""

from typing import List, Dict, Any, Optional
from .tac_manager import TACManager
from .tac_instructions import (
    TACInstruction,
    TACAssignment,
    TACCopy,
    TACBinaryOp,
    TACUnaryOp,
    TACLabel,
    TACGoto,
    TACIfFalseGoto,
)


#########################
# CLASSE PRINCIPAL: ASTTraverser
#########################

class ASTTraverser:
    """Traversador de AST para geração de TAC a partir da AST atribuída."""

    def __init__(self, manager: TACManager):
        """Inicializa o traversador com um TACManager."""
        self.manager = manager
        self.instructions: List[TACInstruction] = []
        self._result_history: List[str] = []  # Para comando RES

    #########################
    # MÉTODO PRINCIPAL
    #########################

    def generate_tac(self, ast_dict: Dict[str, Any]) -> List[TACInstruction]:
        """Gera TAC a partir da AST atribuída completa."""
        self.instructions = []
        self._result_history = []

        # Processa cada nó LINHA de nível superior
        arvore = ast_dict.get("arvore_atribuida", [])
        for linha_node in arvore:
            result_temp = self._process_node(linha_node)
            # Rastreia resultado para comando RES
            if result_temp:
                self._result_history.append(result_temp)

        return self.instructions

    #########################
    # TRAVESSIA PÓS-ORDEM
    #########################

    def _process_node(self, node: Dict[str, Any]) -> Optional[str]:
        """Processa recursivamente um nó da AST em pós-ordem."""
        if not node:
            return None

        tipo_vertice = node.get("tipo_vertice")
        numero_linha = node.get("numero_linha", 0)

        # Caso base: valor literal
        if "valor" in node and not node.get("filhos"):
            return self._handle_literal(node)

        # Caso recursivo: operações
        if tipo_vertice == "ARITH_OP":
            return self._handle_arithmetic_op(node)
        elif tipo_vertice == "COMP_OP":
            return self._handle_comparison_op(node)
        elif tipo_vertice == "LOGIC_OP":
            return self._handle_logical_op(node)
        elif tipo_vertice == "CONTROL_OP":
            return self._handle_control_flow(node)
        elif tipo_vertice == "LINHA":
            filhos = node.get("filhos", [])

            if not filhos:
                return None
            if len(filhos) == 1:
                return self._process_node(filhos[0])
            elif len(filhos) == 2:
                return self._handle_variable_assignment(node)
            else:
                result = None
                for child in filhos:
                    result = self._process_node(child)
                return result
        else:
            raise ValueError(f"Tipo de nó desconhecido: {tipo_vertice} na linha {numero_linha}")

    #########################
    # HANDLERS DE LITERAIS E OPERAÇÕES
    #########################

    def _handle_literal(self, node: Dict[str, Any]) -> str:
        """Processa valores literais (números, constantes). Gera: temp = valor"""
        valor = node["valor"]
        numero_linha = node.get("numero_linha", 0)
        subtipo = node.get("subtipo", "")

        # Determina tipo de dado
        if "real" in subtipo:
            data_type = "real"
        elif "inteiro" in subtipo:
            data_type = "int"
        elif subtipo == "variavel":
            return valor  # Referência a variável, retorna nome diretamente
        else:
            data_type = None

        # Gera TAC: temp = valor
        temp = self.manager.new_temp()
        self.instructions.append(
            TACAssignment(temp, valor, numero_linha, data_type)
        )

        return temp

    def _handle_arithmetic_op(self, node: Dict[str, Any]) -> str:
        """Processa operações aritméticas binárias: +, -, *, /, |, %, ^"""
        operador = node["operador"]
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)
        tipo_inferido = node.get("tipo_inferido")

        # Verificar se temos exatamente 2 filhos (caso normal)
        if len(filhos) == 2:
            left_temp = self._process_node(filhos[0])
            right_temp = self._process_node(filhos[1])
        # Caso especial: ARITH_OP com 1 filho que é outro ARITH_OP
        elif len(filhos) == 1 and filhos[0].get("tipo_vertice") == "ARITH_OP":
            # Processar o ARITH_OP aninhado
            left_temp = self._process_node(filhos[0])
            right_temp = "TEMP4"
        # Caso especial: ARITH_OP com mais de 2 filhos (associatividade à esquerda)
        elif len(filhos) > 2:
            # Tratar como associatividade à esquerda: a * b * c = (a * b) * c
            result_temp = self._process_node(filhos[0])
            for i in range(1, len(filhos)):
                next_temp = self._process_node(filhos[i])
                new_result = self.manager.new_temp()
                self.instructions.append(
                    TACBinaryOp(new_result, result_temp, operador, next_temp, numero_linha, tipo_inferido)
                )
                result_temp = new_result
            return result_temp
        else:
            raise ValueError(f"Operação aritmética requer pelo menos 2 operandos, recebeu {len(filhos)} na linha {numero_linha}")

        # Inferir tipo do resultado se não fornecido pelo nó
        inferred_type = tipo_inferido
        if inferred_type is None:
            inferred_type = self._infer_type_for_binary_op(operador, left_temp, right_temp)

        # Depois processa operação pai
        result_temp = self.manager.new_temp()
        self.instructions.append(
            TACBinaryOp(result_temp, left_temp, operador, right_temp, numero_linha, inferred_type)
        )

        return result_temp

    #########################
    # HANDLERS DE COMPARAÇÃO E LÓGICA
    #########################

    def _handle_comparison_op(self, node: Dict[str, Any]) -> str:
        """Processa operações de comparação: >, <, >=, <=, ==, !="""
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)
        operador = node.get("operador", "")

        left_temp = self._process_node(filhos[0])
        right_temp = self._process_node(filhos[1])

        result_temp = self.manager.new_temp()
        self.instructions.append(
            TACBinaryOp(result_temp, left_temp, operador, right_temp, numero_linha, "boolean")
        )

        return result_temp

    def _handle_logical_op(self, node: Dict[str, Any]) -> str:
        """Processa operações lógicas: && (AND), || (OR), ! (NOT)."""
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)
        operador = node.get("operador", "")

        # Operador unário NOT (!)
        if operador == "!":
            if len(filhos) != 1:
                raise ValueError(f"Operador '!' requer 1 operando, recebeu {len(filhos)} na linha {numero_linha}")

            operand_temp = self._process_node(filhos[0])
            result_temp = self.manager.new_temp()
            self.instructions.append(
                TACUnaryOp(result_temp, operador, operand_temp, numero_linha, "boolean")
            )
            return result_temp

        # Operadores binários (&& e ||)
        if len(filhos) != 2:
            raise ValueError(f"Operador '{operador}' requer 2 operandos, recebeu {len(filhos)} na linha {numero_linha}")

        left_temp = self._process_node(filhos[0])
        right_temp = self._process_node(filhos[1])

        result_temp = self.manager.new_temp()
        self.instructions.append(
            TACBinaryOp(result_temp, left_temp, operador, right_temp, numero_linha, "boolean")
        )

        return result_temp

    #########################
    # HANDLERS DE CONTROLE DE FLUXO
    #########################

    def _handle_control_flow(self, node: Dict[str, Any]) -> Optional[str]:
        """Despacha para handlers específicos de controle de fluxo."""
        operador = node.get("operador", "")
        numero_linha = node.get("numero_linha", 0)

        if operador == "IFELSE":
            return self._handle_ifelse(node)
        elif operador == "WHILE":
            return self._handle_while(node)
        elif operador == "FOR":
            return self._handle_for(node)
        else:
            raise ValueError(f"Operador de controle desconhecido '{operador}' na linha {numero_linha}")

    def _handle_ifelse(self, node: Dict[str, Any]) -> Optional[str]:
        """Processa IFELSE: (condição then else IFELSE)."""
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)

        if len(filhos) != 3:
            raise ValueError(f"IFELSE requer 3 operandos, recebeu {len(filhos)} na linha {numero_linha}")

        condition_node, then_node, else_node = filhos[0], filhos[1], filhos[2]

        # Gera labels
        label_else = self.manager.new_label()
        label_end = self.manager.new_label()

        # Processa condição
        cond_temp = self._process_node(condition_node)
        self.instructions.append(TACIfFalseGoto(cond_temp, label_else, numero_linha))

        # Processa branch then
        then_temp = self._process_node(then_node)
        self.instructions.append(TACGoto(label_end, numero_linha))

        # Processa branch else
        self.instructions.append(TACLabel(label_else, numero_linha))
        else_temp = self._process_node(else_node)
        self.instructions.append(TACLabel(label_end, numero_linha))

        return else_temp

    def _handle_while(self, node: Dict[str, Any]) -> Optional[str]:
        """Processa WHILE: (condição bloco WHILE) - bloco pode ter múltiplas expressões."""
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)

        if len(filhos) < 2:
            raise ValueError(f"WHILE requer pelo menos 2 operandos, recebeu {len(filhos)} na linha {numero_linha}")

        condition_node = filhos[0]
        block_nodes = filhos[1:]  # Todos os filhos restantes são o bloco

        # Gera labels
        label_start = self.manager.new_label()
        label_end = self.manager.new_label()

        # L_start:
        self.instructions.append(TACLabel(label_start, numero_linha))

        # Processa condição
        cond_temp = self._process_node(condition_node)
        self.instructions.append(TACIfFalseGoto(cond_temp, label_end, numero_linha))

        # Processa bloco (sequência de expressões)
        for block_node in block_nodes:
            self._process_node(block_node)

        self.instructions.append(TACGoto(label_start, numero_linha))

        # L_end:
        self.instructions.append(TACLabel(label_end, numero_linha))

        return None

    def _handle_for(self, node: Dict[str, Any]) -> Optional[str]:
        """Processa FOR: (init fim passo bloco FOR) - bloco pode ter múltiplas expressões."""
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)

        if len(filhos) != 4:
            raise ValueError(f"FOR requer 4 operandos, recebeu {len(filhos)} na linha {numero_linha}")

        init_node, end_node, step_node, block_node = filhos[0], filhos[1], filhos[2], filhos[3]

        # Gera labels
        label_start = self.manager.new_label()
        label_end = self.manager.new_label()

        # Processa valores iniciais
        current_temp = self._process_node(init_node)
        end_temp = self._process_node(end_node)
        step_temp = self._process_node(step_node)

        # Cria temp para contador do loop
        loop_counter = self.manager.new_temp()
        self.instructions.append(TACCopy(loop_counter, current_temp, numero_linha, "int"))

        # L_start:
        self.instructions.append(TACLabel(label_start, numero_linha))

        # Condição: contador <= fim
        cond_temp = self.manager.new_temp()
        self.instructions.append(TACBinaryOp(cond_temp, loop_counter, "<=", end_temp, numero_linha, "boolean"))
        self.instructions.append(TACIfFalseGoto(cond_temp, label_end, numero_linha))

        # Processa bloco (sequência de expressões)
        self._process_block(block_node)

        # Incrementa contador
        new_counter = self.manager.new_temp()
        self.instructions.append(TACBinaryOp(new_counter, loop_counter, "+", step_temp, numero_linha, "int"))
        self.instructions.append(TACCopy(loop_counter, new_counter, numero_linha, "int"))
        self.instructions.append(TACGoto(label_start, numero_linha))

        # L_end:
        self.instructions.append(TACLabel(label_end, numero_linha))

        return None

    def _process_block(self, block_node: Dict[str, Any]) -> None:
        """Processa um bloco de código (sequência de expressões ou bloco implícito)."""
        if not block_node:
            return

        # Verificar se é um bloco implícito (linha com múltiplas expressões)
        if self._is_implicit_block(block_node):
            self._process_implicit_block(block_node)
        elif 'filhos' in block_node:
            # Um bloco é uma sequência de linhas/expressões
            for expression_node in block_node['filhos']:
                self._process_node(expression_node)
        else:
            # Corpo simples
            self._process_node(block_node)

    def _is_implicit_block(self, node: Dict[str, Any]) -> bool:
        """Verifica se um nó representa um bloco implícito (linha com múltiplas expressões)."""
        if not node or node.get('tipo') != 'LINHA':
            return False

        # Uma linha é um bloco implícito se tem filhos que são expressões sem operador final
        filhos = node.get('filhos', [])
        if len(filhos) > 1:
            # Verificar se todos os filhos são linhas/expressões
            return all(filho.get('tipo') == 'LINHA' for filho in filhos)
        return False

    def _process_implicit_block(self, block_node: Dict[str, Any]) -> None:
        """Processa um bloco implícito (linha contendo múltiplas subexpressões)."""
        filhos = block_node.get('filhos', [])
        for expression_node in filhos:
            if expression_node.get('tipo') == 'LINHA':
                # Verificar se esta expressão contém múltiplas subexpressões que deveriam ser atribuições
                sub_filhos = expression_node.get('filhos', [])
                if len(sub_filhos) == 2 and all(f.get('tipo') == 'LINHA' for f in sub_filhos):
                    # Possível padrão: ((expr1) (expr2)) - tratar como duas atribuições separadas
                    for sub_expr in sub_filhos:
                        self._process_node(sub_expr)
                else:
                    # Expressão normal
                    self._process_node(expression_node)

    def _handle_variable_assignment(self, node: Dict[str, Any]) -> str:
        """Processa atribuições de variáveis: (valor variável). Ex: (10 X) → X = 10"""
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)

        if len(filhos) < 2:
            result = None
            for child in filhos:
                result = self._process_node(child)
            return result

        value_node = filhos[0]
        var_node = filhos[1]

        # Verifica comando RES
        if var_node.get("valor") == "RES":
            return self._handle_res_command(node)

        # Verifica se é uma variável válida (não é símbolo especial)
        var_name = var_node.get("valor", "")
        if not var_name or var_name in ['(', ')', '[', ']', '{', '}', ';', ':', '.', ','] or var_node.get("subtipo") != "variavel":
            # Não é uma atribuição válida - apenas processe os filhos sem gerar TAC
            result = None
            for child in filhos:
                temp_result = self._process_node(child)
                if temp_result is not None:
                    result = temp_result
            return result

        # Processa expressão de valor
        value_temp = self._process_node(value_node)
        data_type = value_node.get("tipo_inferido")

        # Se não há tipo no nó, tentar inferir a partir do operando (constante, temp ou variável)
        if data_type is None:
            data_type = self._infer_type_for_operand(value_temp)

        self.instructions.append(TACCopy(var_name, value_temp, numero_linha, data_type))

        return value_temp

    def _handle_res_command(self, node: Dict[str, Any]) -> str:
        """Processa comando RES: (índice RES) - recupera resultado histórico."""
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)

        index_node = filhos[0]
        index_value = index_node.get("valor", "0")

        try:
            index = int(index_value)
        except ValueError:
            raise ValueError(f"Índice RES deve ser inteiro, recebeu '{index_value}' na linha {numero_linha}")

        if index < 0 or index >= len(self._result_history):
            raise ValueError(f"Índice RES {index} fora dos limites (histórico: {len(self._result_history)}) na linha {numero_linha}")

        historical_temp = self._result_history[index]
        result_temp = self.manager.new_temp()

        # Inferir tipo do histórico, se possível (procura última definição ou constante)
        inferred_type = None
        if TACInstruction.is_constant(historical_temp):
            inferred_type = self._infer_type_for_operand(historical_temp)
        elif isinstance(historical_temp, str):
            inferred_type = self._infer_type_for_operand(historical_temp)

        self.instructions.append(TACCopy(result_temp, historical_temp, numero_linha, inferred_type))

        return result_temp

    #########################
    # MÉTODOS UTILITÁRIOS
    #########################

    def _infer_type_for_operand(self, operand: Optional[str]) -> Optional[str]:
        """Inferir tipo ('int'|'real'|'boolean'|None) para um operando (constante, temp ou variável)."""
        if operand is None:
            return None

        # Constantes numéricas
        if TACInstruction.is_constant(operand):
            # simples heurística: ponto decimal ou expoente indica real
            if '.' in operand or 'e' in operand or 'E' in operand:
                return 'real'
            return 'int'

        # Procurar última definição nas instruções geradas
        for instr in reversed(self.instructions):
            defined = getattr(instr, 'result', getattr(instr, 'dest', None))
            if defined == operand:
                return getattr(instr, 'data_type', None)

        # Não encontrado
        return None

    def _infer_type_for_binary_op(self, operator: str, left_operand: Optional[str], right_operand: Optional[str]) -> Optional[str]:
        """Inferir tipo de resultado para uma operação binária com base em operandos e operador."""
        # Regra: se operador é divisão real '|', o resultado é real
        if operator == '|':
            return 'real'
        # divisão inteira '/'
        if operator == '/':
            return 'int'

        left_type = self._infer_type_for_operand(left_operand)
        right_type = self._infer_type_for_operand(right_operand)

        # Exponencial: if any real -> real, else int
        if operator == '^':
            if left_type == 'real' or right_type == 'real':
                return 'real'
            if left_type == 'int' and right_type == 'int':
                return 'int'
            return None

        # Modulo: Prefira int quando ambos forem ints
        if operator == '%':
            if left_type == 'int' and right_type == 'int':
                return 'int'
            if left_type == 'real' or right_type == 'real':
                return 'real'
            return None

        # Aritmética padrão: se algum operando for real -> real, senão se ambos int -> int
        if left_type == 'real' or right_type == 'real':
            return 'real'
        if left_type == 'int' and right_type == 'int':
            return 'int'

        return None

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas sobre o TAC gerado."""
        manager_stats = self.manager.get_statistics()

        return {
            "total_instructions": len(self.instructions),
            "temp_count": manager_stats["current_temp_count"],
            "label_count": manager_stats["current_label_count"],
            "result_history_size": len(self._result_history)
        }

    def __repr__(self) -> str:
        """Representação string do estado do traversador."""
        stats = self.get_statistics()
        return f"ASTTraverser(instructions={stats['total_instructions']}, temps={stats['temp_count']}, labels={stats['label_count']})"
