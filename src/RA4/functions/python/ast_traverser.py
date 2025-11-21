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
    TACBinaryOp,
    TACUnaryOp,
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
        Handle logical operations: &&, ||

        TODO: Implement in Issue 1.5

        For now: stub implementation that processes children
        """
        filhos = node["filhos"]
        numero_linha = node.get("numero_linha", 0)
        operador = node.get("operador", "")

        # Process children
        left_temp = self._process_node(filhos[0])
        right_temp = self._process_node(filhos[1])

        # Generate logical TAC
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

        TODO: Implement in Issue 1.7

        For now: raise NotImplementedError
        """
        operador = node.get("operador", "")
        numero_linha = node.get("numero_linha", 0)

        raise NotImplementedError(
            f"Control flow '{operador}' not yet implemented (Issue 1.7) "
            f"at line {numero_linha}"
        )

    def _handle_variable_assignment(self, node: Dict[str, Any]) -> str:
        """
        Handle variable assignments: (value variable)

        Example: (10 X) means X = 10

        TODO: Implement properly in Issue 1.6

        For now: stub implementation that processes children
        """
        filhos = node["filhos"]

        # Process both children
        if len(filhos) >= 2:
            # First child is the value/expression
            value_temp = self._process_node(filhos[0])

            # Second child should be the variable
            var_node = filhos[1]
            if var_node.get("subtipo") == "variavel":
                # This is a variable assignment
                # For now, just return the value temp
                # TODO: Generate proper assignment TAC in Issue 1.6
                return value_temp

        # Fallback: process all children
        result = None
        for child in filhos:
            result = self._process_node(child)
        return result

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
