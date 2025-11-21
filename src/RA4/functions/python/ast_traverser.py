"""
AST Traverser - Post-Order Tree Traversal for TAC Generation

This module implements the AST (Abstract Syntax Tree) traversal engine that walks
the attributed AST from Phase 3 and generates Three Address Code (TAC) instructions.

The traversal is done in POST-ORDER (bottom-up), visiting children before parents,
which is essential for proper TAC generation.
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


class ASTTraverser:
    """
    AST Traverser for generating TAC from attributed AST.

    This class implements a post-order (bottom-up) traversal of the AST,
    generating TAC instructions as it processes each node.

    Usage:
        manager = TACManager()
        traverser = ASTTraverser(manager)
        instructions = traverser.generate_tac(ast_dict)
    """

    def __init__(self, manager: TACManager):
        """
        Initialize the AST traverser.

        Args:
            manager: TACManager instance for generating temporary variables and labels
        """
        self.manager = manager
        self.instructions: List[TACInstruction] = []
        self._result_history: List[str] = []  # For RES command (Issue 1.6)

    def generate_tac(self, ast_dict: Dict[str, Any]) -> List[TACInstruction]:
        """
        Main entry point: Generate TAC from complete attributed AST.

        Args:
            ast_dict: The attributed AST dictionary from Phase 3
                     Format: {"arvore_atribuida": [list of LINHA nodes]}

        Returns:
            List of TACInstruction objects in execution order

        Example:
            >>> ast = {"arvore_atribuida": [...]}
            >>> instructions = traverser.generate_tac(ast)
        """
        self.instructions = []
        self._result_history = []

        # Process each top-level LINHA node
        arvore = ast_dict.get("arvore_atribuida", [])
        for linha_node in arvore:
            result_temp = self._process_node(linha_node)
            # Track result for RES command support (Issue 1.6)
            if result_temp:
                self._result_history.append(result_temp)

        return self.instructions

    def _process_node(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Recursively process an AST node in POST-ORDER.

        This is the core traversal method. It visits children BEFORE processing
        the parent node, which is essential for TAC generation.

        Args:
            node: AST node dictionary

        Returns:
            The temporary variable name holding this node's result, or None

        Post-order sequence example for (5 3 +):
            1. Process child '5' → t0 = 5
            2. Process child '3' → t1 = 3
            3. Process parent '+' → t2 = t0 + t1
        """
        if not node:
            return None

        tipo_vertice = node.get("tipo_vertice")
        numero_linha = node.get("numero_linha", 0)

        # === BASE CASE: Literal Value ===
        if "valor" in node and not node.get("filhos"):
            return self._handle_literal(node)

        # === RECURSIVE CASE: Operations ===

        # Arithmetic operations: +, -, *, /, |, %, ^
        if tipo_vertice == "ARITH_OP":
            return self._handle_arithmetic_op(node)

        # Comparison operations: >, <, >=, <=, ==, != (Issue 1.5)
        elif tipo_vertice == "COMP_OP":
            return self._handle_comparison_op(node)

        # Logical operations: &&, || (Issue 1.5)
        elif tipo_vertice == "LOGIC_OP":
            return self._handle_logical_op(node)

        # Control flow: WHILE, FOR, IFELSE (Issue 1.7)
        elif tipo_vertice == "CONTROL_OP":
            return self._handle_control_flow(node)

        # LINHA wrapper node: process its children
        elif tipo_vertice == "LINHA":
            filhos = node.get("filhos", [])

            # Empty line
            if not filhos:
                return None

            # Single child: process it
            if len(filhos) == 1:
                return self._process_node(filhos[0])

            # Multiple children: might be variable assignment (Issue 1.6)
            # Format: [value, variable] for assignment like (10 X)
            elif len(filhos) == 2:
                return self._handle_variable_assignment(node)

            # Multiple children with control flow
            else:
                # Process all children and return last result
                result = None
                for child in filhos:
                    result = self._process_node(child)
                return result

        # Unknown node type
        else:
            raise ValueError(f"Unknown node type: {tipo_vertice} at line {numero_linha}")

    # ========================================================================
    # HANDLER METHODS - Issue 1.3 + 1.4 (Implemented)
    # ========================================================================

    def _handle_literal(self, node: Dict[str, Any]) -> str:
        """
        Handle literal values (numbers, constants).

        Generates: temp = value

        Args:
            node: Node with "valor" field

        Returns:
            Temporary variable holding the literal value

        Example:
            Node: {"valor": "5", "subtipo": "numero_inteiro", "numero_linha": 1}
            Generates: t0 = 5
            Returns: "t0"
        """
        valor = node["valor"]
        numero_linha = node.get("numero_linha", 0)
        subtipo = node.get("subtipo", "")

        # Determine data type
        if "real" in subtipo:
            data_type = "real"
        elif "inteiro" in subtipo:
            data_type = "int"
        elif subtipo == "variavel":
            # This is a variable reference, not a literal
            # Just return the variable name (no TAC needed)
            return valor
        else:
            data_type = None

        # Generate TAC: temp = value
        temp = self.manager.new_temp()
        self.instructions.append(
            TACAssignment(temp, valor, numero_linha, data_type)
        )

        return temp

    def _handle_arithmetic_op(self, node: Dict[str, Any]) -> str:
        """
        Handle arithmetic binary operations: +, -, *, /, |, %, ^

        POST-ORDER:
        1. Process left operand (child 0)
        2. Process right operand (child 1)
        3. Generate operation TAC

        Args:
            node: ARITH_OP node with operator and 2 children

        Returns:
            Temporary variable holding the operation result

        Example:
            Node: ARITH_OP with operator "+" and children [5, 3]
            Generates:
                t0 = 5
                t1 = 3
                t2 = t0 + t1
            Returns: "t2"
        """
        operador = node["operador"]
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)
        tipo_inferido = node.get("tipo_inferido")

        if len(filhos) != 2:
            raise ValueError(
                f"Arithmetic operation requires 2 operands, got {len(filhos)} "
                f"at line {numero_linha}"
            )

        # POST-ORDER: Process children FIRST
        left_temp = self._process_node(filhos[0])
        right_temp = self._process_node(filhos[1])

        # THEN process parent operation
        result_temp = self.manager.new_temp()
        self.instructions.append(
            TACBinaryOp(
                result_temp,
                left_temp,
                operador,
                right_temp,
                numero_linha,
                tipo_inferido
            )
        )

        return result_temp

    # ========================================================================
    # PLACEHOLDER METHODS - Issues 1.5, 1.6, 1.7 (To Be Implemented)
    # ========================================================================

    def _handle_comparison_op(self, node: Dict[str, Any]) -> str:
        """
        Handle comparison operations: >, <, >=, <=, ==, !=

        TODO: Implement in Issue 1.5

        For now: stub implementation that processes children
        """
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)
        operador = node.get("operador", "")

        # Process children
        left_temp = self._process_node(filhos[0])
        right_temp = self._process_node(filhos[1])

        # Generate comparison TAC
        result_temp = self.manager.new_temp()
        self.instructions.append(
            TACBinaryOp(
                result_temp,
                left_temp,
                operador,
                right_temp,
                numero_linha,
                "boolean"
            )
        )

        return result_temp

    def _handle_logical_op(self, node: Dict[str, Any]) -> str:
        """
        Handle logical operations: &&, || (binary) and ! (unary)

        Issue 1.5 - Operações Lógicas

        Binary operators (&&, ||):
            TAC: t2 = t0 && t1

        Unary operator (!):
            TAC: t1 = !t0
        """
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)
        operador = node.get("operador", "")

        # Handle unary NOT operator (!)
        if operador == "!":
            if len(filhos) != 1:
                raise ValueError(
                    f"NOT operator '!' requires 1 operand, got {len(filhos)} "
                    f"at line {numero_linha}"
                )

            # Process single operand
            operand_temp = self._process_node(filhos[0])

            # Generate unary TAC: result = !operand
            result_temp = self.manager.new_temp()
            self.instructions.append(
                TACUnaryOp(
                    result_temp,
                    operador,
                    operand_temp,
                    numero_linha,
                    "boolean"
                )
            )

            return result_temp

        # Handle binary operators (&& and ||)
        if len(filhos) != 2:
            raise ValueError(
                f"Logical operator '{operador}' requires 2 operands, got {len(filhos)} "
                f"at line {numero_linha}"
            )

        # Process children in post-order
        left_temp = self._process_node(filhos[0])
        right_temp = self._process_node(filhos[1])

        # Generate binary logical TAC
        result_temp = self.manager.new_temp()
        self.instructions.append(
            TACBinaryOp(
                result_temp,
                left_temp,
                operador,
                right_temp,
                numero_linha,
                "boolean"
            )
        )

        return result_temp

    def _handle_control_flow(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Handle control flow structures: WHILE, FOR, IFELSE

        Issue 1.7 - Control Flow

        Dispatches to specific handlers based on operator type.
        """
        operador = node.get("operador", "")
        numero_linha = node.get("numero_linha", 0)

        if operador == "IFELSE":
            return self._handle_ifelse(node)
        elif operador == "WHILE":
            return self._handle_while(node)
        elif operador == "FOR":
            return self._handle_for(node)
        else:
            raise ValueError(
                f"Unknown control flow operator '{operador}' "
                f"at line {numero_linha}"
            )

    def _handle_ifelse(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Handle IFELSE: (condition then_expr else_expr IFELSE)

        Issue 1.7 - IFELSE Control Flow

        TAC pattern:
            <condition TAC>
            if_false t_cond goto L_else
            <then TAC>
            goto L_end
        L_else:
            <else TAC>
        L_end:

        Args:
            node: CONTROL_OP node with operator "IFELSE" and 3 children
                  [condition, then_branch, else_branch]

        Returns:
            The temporary variable holding the result (from then or else branch)
        """
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)

        if len(filhos) != 3:
            raise ValueError(
                f"IFELSE requires 3 operands (condition, then, else), got {len(filhos)} "
                f"at line {numero_linha}"
            )

        condition_node = filhos[0]
        then_node = filhos[1]
        else_node = filhos[2]

        # Generate labels
        label_else = self.manager.new_label()
        label_end = self.manager.new_label()

        # Process condition
        cond_temp = self._process_node(condition_node)

        # Generate: if_false cond_temp goto label_else
        self.instructions.append(
            TACIfFalseGoto(cond_temp, label_else, numero_linha)
        )

        # Process then branch
        then_temp = self._process_node(then_node)

        # Generate: goto label_end
        self.instructions.append(
            TACGoto(label_end, numero_linha)
        )

        # Generate: label_else:
        self.instructions.append(
            TACLabel(label_else, numero_linha)
        )

        # Process else branch
        else_temp = self._process_node(else_node)

        # Generate: label_end:
        self.instructions.append(
            TACLabel(label_end, numero_linha)
        )

        # Return the result (could be from either branch at runtime)
        # For TAC purposes, we return the else_temp as the "last" value
        return else_temp

    def _handle_while(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Handle WHILE: (condition body WHILE)

        Issue 1.7 - WHILE Control Flow

        TAC pattern:
        L_start:
            <condition TAC>
            if_false t_cond goto L_end
            <body TAC>
            goto L_start
        L_end:

        Args:
            node: CONTROL_OP node with operator "WHILE" and 2 children
                  [condition, body]

        Returns:
            None (WHILE doesn't produce a value)
        """
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)

        if len(filhos) != 2:
            raise ValueError(
                f"WHILE requires 2 operands (condition, body), got {len(filhos)} "
                f"at line {numero_linha}"
            )

        condition_node = filhos[0]
        body_node = filhos[1]

        # Generate labels
        label_start = self.manager.new_label()
        label_end = self.manager.new_label()

        # Generate: label_start:
        self.instructions.append(
            TACLabel(label_start, numero_linha)
        )

        # Process condition
        cond_temp = self._process_node(condition_node)

        # Generate: if_false cond_temp goto label_end
        self.instructions.append(
            TACIfFalseGoto(cond_temp, label_end, numero_linha)
        )

        # Process body
        self._process_node(body_node)

        # Generate: goto label_start
        self.instructions.append(
            TACGoto(label_start, numero_linha)
        )

        # Generate: label_end:
        self.instructions.append(
            TACLabel(label_end, numero_linha)
        )

        # WHILE doesn't produce a value
        return None

    def _handle_for(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Handle FOR: (init end step body FOR)

        Issue 1.7 - FOR Control Flow

        FOR loop iterates from init to end with given step.

        TAC pattern:
            t_current = <init TAC>
            t_end = <end TAC>
            t_step = <step TAC>
        L_start:
            t_cond = t_current <= t_end
            if_false t_cond goto L_end
            <body TAC>
            t_current = t_current + t_step
            goto L_start
        L_end:

        Args:
            node: CONTROL_OP node with operator "FOR" and 4 children
                  [init, end, step, body]

        Returns:
            None (FOR doesn't produce a value)
        """
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)

        if len(filhos) != 4:
            raise ValueError(
                f"FOR requires 4 operands (init, end, step, body), got {len(filhos)} "
                f"at line {numero_linha}"
            )

        init_node = filhos[0]
        end_node = filhos[1]
        step_node = filhos[2]
        body_node = filhos[3]

        # Generate labels
        label_start = self.manager.new_label()
        label_end = self.manager.new_label()

        # Process init, end, and step values
        current_temp = self._process_node(init_node)
        end_temp = self._process_node(end_node)
        step_temp = self._process_node(step_node)

        # Create a dedicated temp for the loop counter
        loop_counter = self.manager.new_temp()
        self.instructions.append(
            TACCopy(loop_counter, current_temp, numero_linha, "int")
        )

        # Generate: label_start:
        self.instructions.append(
            TACLabel(label_start, numero_linha)
        )

        # Generate condition: t_cond = loop_counter <= end_temp
        cond_temp = self.manager.new_temp()
        self.instructions.append(
            TACBinaryOp(
                cond_temp,
                loop_counter,
                "<=",
                end_temp,
                numero_linha,
                "boolean"
            )
        )

        # Generate: if_false cond_temp goto label_end
        self.instructions.append(
            TACIfFalseGoto(cond_temp, label_end, numero_linha)
        )

        # Process body
        self._process_node(body_node)

        # Increment loop counter: loop_counter = loop_counter + step_temp
        new_counter = self.manager.new_temp()
        self.instructions.append(
            TACBinaryOp(
                new_counter,
                loop_counter,
                "+",
                step_temp,
                numero_linha,
                "int"
            )
        )
        self.instructions.append(
            TACCopy(loop_counter, new_counter, numero_linha, "int")
        )

        # Generate: goto label_start
        self.instructions.append(
            TACGoto(label_start, numero_linha)
        )

        # Generate: label_end:
        self.instructions.append(
            TACLabel(label_end, numero_linha)
        )

        # FOR doesn't produce a value
        return None

    def _handle_variable_assignment(self, node: Dict[str, Any]) -> str:
        """
        Handle variable assignments: (value variable)

        Issue 1.6 - Variable Assignment

        Example: (10 X) means X = 10
        In RPN: value comes first, then variable name

        TAC generated:
            t0 = 10
            X = t0

        Args:
            node: LINHA node with 2 children [value_expr, variable]

        Returns:
            The temporary variable holding the assigned value
        """
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)

        if len(filhos) < 2:
            # Fallback: process all children
            result = None
            for child in filhos:
                result = self._process_node(child)
            return result

        # First child is the value/expression
        value_node = filhos[0]
        # Second child should be the variable or RES command
        var_node = filhos[1]

        # Check if second child is RES command (Issue 1.6 - RES)
        if var_node.get("valor") == "RES":
            return self._handle_res_command(node)

        # Check if this is indeed a variable assignment
        if var_node.get("subtipo") != "variavel":
            # Not a variable assignment, process all children
            result = None
            for child in filhos:
                result = self._process_node(child)
            return result

        # Process the value expression
        value_temp = self._process_node(value_node)

        # Get the variable name
        var_name = var_node["valor"]

        # Get type info from the value node or expression
        data_type = value_node.get("tipo_inferido")

        # Generate TAC: variable = value_temp
        self.instructions.append(
            TACCopy(
                var_name,
                value_temp,
                numero_linha,
                data_type
            )
        )

        # Return the value temp (the result of this expression)
        return value_temp

    def _handle_res_command(self, node: Dict[str, Any]) -> str:
        """
        Handle RES command: (index RES) - get historical result

        Issue 1.6 - RES Command

        RES retrieves a previously computed result from history.
        In RPN: (1 RES) means get result at position 1 (0-indexed)
                (RES) alone means get the last result

        TAC generated:
            t_new = t_previous  (copy from history)

        Args:
            node: LINHA node where second child is RES

        Returns:
            The temporary variable holding the retrieved result
        """
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)

        # Get the index (first child)
        index_node = filhos[0]
        index_value = index_node.get("valor", "0")

        try:
            index = int(index_value)
        except ValueError:
            raise ValueError(
                f"RES index must be an integer, got '{index_value}' "
                f"at line {numero_linha}"
            )

        # Validate index is within history bounds
        if index < 0 or index >= len(self._result_history):
            raise ValueError(
                f"RES index {index} out of bounds (history size: {len(self._result_history)}) "
                f"at line {numero_linha}"
            )

        # Get the historical result temp
        historical_temp = self._result_history[index]

        # Generate TAC: new_temp = historical_temp
        result_temp = self.manager.new_temp()
        self.instructions.append(
            TACCopy(
                result_temp,
                historical_temp,
                numero_linha,
                None  # Type unknown at this point
            )
        )

        return result_temp

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the generated TAC.

        Returns:
            Dictionary with statistics:
                - total_instructions: Total TAC instructions generated
                - temp_count: Number of temporaries created
                - label_count: Number of labels created
        """
        manager_stats = self.manager.get_statistics()

        return {
            "total_instructions": len(self.instructions),
            "temp_count": manager_stats["current_temp_count"],
            "label_count": manager_stats["current_label_count"],
            "result_history_size": len(self._result_history)
        }

    def __repr__(self) -> str:
        """String representation of the traverser state."""
        stats = self.get_statistics()
        return (
            f"ASTTraverser("
            f"instructions={stats['total_instructions']}, "
            f"temps={stats['temp_count']}, "
            f"labels={stats['label_count']})"
        )
