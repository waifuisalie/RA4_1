"""
Unit Tests for AST Traverser

Tests the ASTTraverser class for TAC generation from attributed AST.

Run with: pytest tests/RA4/test_ast_traverser.py -v
"""

import sys
import os
import pytest

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from src.RA4.functions.python.tac_manager import TACManager
from src.RA4.functions.python.ast_traverser import ASTTraverser
from src.RA4.functions.python.tac_instructions import (
    TACAssignment,
    TACBinaryOp,
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_literal_node(valor: str, subtipo: str, numero_linha: int = 1):
    """Helper to create a literal node."""
    return {
        "tipo_vertice": "LINHA",
        "tipo_inferido": None,
        "numero_linha": numero_linha,
        "filhos": [],
        "valor": valor,
        "subtipo": subtipo
    }


def create_arith_op_node(operador: str, left, right, numero_linha: int = 1):
    """Helper to create an arithmetic operation node."""
    return {
        "tipo_vertice": "ARITH_OP",
        "tipo_inferido": None,
        "numero_linha": numero_linha,
        "filhos": [left, right],
        "operador": operador
    }


def create_linha_node(child, numero_linha: int = 1, tipo_inferido: str = "int"):
    """Helper to create a LINHA wrapper node."""
    return {
        "tipo_vertice": "LINHA",
        "tipo_inferido": tipo_inferido,
        "numero_linha": numero_linha,
        "filhos": [child] if not isinstance(child, list) else child
    }


# ============================================================================
# BASIC FUNCTIONALITY TESTS
# ============================================================================

def test_traverser_initialization():
    """Test that ASTTraverser initializes correctly."""
    manager = TACManager()
    traverser = ASTTraverser(manager)

    assert traverser.manager is manager
    assert traverser.instructions == []


def test_empty_ast():
    """Test processing an empty AST."""
    manager = TACManager()
    traverser = ASTTraverser(manager)

    ast = {"arvore_atribuida": []}
    instructions = traverser.generate_tac(ast)

    assert instructions == []


def test_empty_linha():
    """Test processing a LINHA node with no children."""
    manager = TACManager()
    traverser = ASTTraverser(manager)

    ast = {
        "arvore_atribuida": [
            {
                "tipo_vertice": "LINHA",
                "tipo_inferido": None,
                "numero_linha": 1,
                "filhos": []
            }
        ]
    }

    instructions = traverser.generate_tac(ast)
    assert instructions == []


# ============================================================================
# LITERAL HANDLING TESTS
# ============================================================================

def test_single_integer_literal():
    """Test processing a single integer literal."""
    manager = TACManager()
    traverser = ASTTraverser(manager)

    literal_node = create_literal_node("5", "numero_inteiro", 1)
    linha_node = create_linha_node(literal_node, 1, "int")

    ast = {"arvore_atribuida": [linha_node]}
    instructions = traverser.generate_tac(ast)

    assert len(instructions) == 1
    assert isinstance(instructions[0], TACAssignment)
    assert instructions[0].dest == "t0"
    assert instructions[0].source == "5"
    assert instructions[0].line == 1
    assert instructions[0].data_type == "int"


def test_single_real_literal():
    """Test processing a single real (float) literal."""
    manager = TACManager()
    traverser = ASTTraverser(manager)

    literal_node = create_literal_node("10.5", "numero_real", 2)
    linha_node = create_linha_node(literal_node, 2, "real")

    ast = {"arvore_atribuida": [linha_node]}
    instructions = traverser.generate_tac(ast)

    assert len(instructions) == 1
    assert isinstance(instructions[0], TACAssignment)
    assert instructions[0].dest == "t0"
    assert instructions[0].source == "10.5"
    assert instructions[0].data_type == "real"


def test_variable_reference():
    """Test that variable references don't generate assignment TAC."""
    manager = TACManager()
    traverser = ASTTraverser(manager)

    var_node = create_literal_node("X", "variavel", 1)

    result = traverser._handle_literal(var_node)

    # Variable references should just return the variable name
    assert result == "X"
    # No TAC instruction should be generated
    assert len(traverser.instructions) == 0


# ============================================================================
# ARITHMETIC OPERATIONS TESTS
# ============================================================================

def test_simple_addition():
    """
    Test simple addition: (5 3 +)

    Expected TAC:
        t0 = 5
        t1 = 3
        t2 = t0 + t1
    """
    manager = TACManager()
    traverser = ASTTraverser(manager)

    # Build AST for (5 3 +)
    left = create_literal_node("5", "numero_inteiro", 1)
    right = create_literal_node("3", "numero_inteiro", 1)
    arith_op = create_arith_op_node("+", left, right, 1)
    linha = create_linha_node(arith_op, 1, "int")

    ast = {"arvore_atribuida": [linha]}
    instructions = traverser.generate_tac(ast)

    assert len(instructions) == 3

    # t0 = 5
    assert isinstance(instructions[0], TACAssignment)
    assert instructions[0].dest == "t0"
    assert instructions[0].source == "5"

    # t1 = 3
    assert isinstance(instructions[1], TACAssignment)
    assert instructions[1].dest == "t1"
    assert instructions[1].source == "3"

    # t2 = t0 + t1
    assert isinstance(instructions[2], TACBinaryOp)
    assert instructions[2].result == "t2"
    assert instructions[2].operand1 == "t0"
    assert instructions[2].operator == "+"
    assert instructions[2].operand2 == "t1"


@pytest.mark.parametrize("operator,left_val,right_val", [
    ("+", "5", "3"),
    ("-", "10", "7"),
    ("*", "4", "6"),
    ("/", "15", "3"),
    ("|", "10.0", "2.0"),  # Real division
    ("%", "23", "5"),  # Modulo
    ("^", "2", "8"),  # Power
])
def test_all_arithmetic_operators(operator, left_val, right_val):
    """Test all arithmetic operators: +, -, *, /, |, %, ^"""
    manager = TACManager()
    traverser = ASTTraverser(manager)

    # Determine subtipo based on values
    subtipo = "numero_real" if "." in left_val else "numero_inteiro"

    left = create_literal_node(left_val, subtipo, 1)
    right = create_literal_node(right_val, subtipo, 1)
    arith_op = create_arith_op_node(operator, left, right, 1)
    linha = create_linha_node(arith_op, 1)

    ast = {"arvore_atribuida": [linha]}
    instructions = traverser.generate_tac(ast)

    assert len(instructions) == 3

    # Check the binary operation has correct operator
    assert isinstance(instructions[2], TACBinaryOp)
    assert instructions[2].operator == operator


def test_multiplication_real_numbers():
    """
    Test multiplication with real numbers: (10.5 2.0 *)

    Expected TAC:
        t0 = 10.5
        t1 = 2.0
        t2 = t0 * t1
    """
    manager = TACManager()
    traverser = ASTTraverser(manager)

    left = create_literal_node("10.5", "numero_real", 2)
    right = create_literal_node("2.0", "numero_real", 2)
    arith_op = create_arith_op_node("*", left, right, 2)
    linha = create_linha_node(arith_op, 2, "real")

    ast = {"arvore_atribuida": [linha]}
    instructions = traverser.generate_tac(ast)

    assert len(instructions) == 3
    assert instructions[0].data_type == "real"
    assert instructions[1].data_type == "real"
    assert instructions[2].operator == "*"


# ============================================================================
# VARIABLES IN EXPRESSIONS TESTS
# ============================================================================

def test_addition_with_variable():
    """
    Test addition with variable: (X 5 +)

    Expected TAC:
        # X is just referenced, no assignment
        t0 = 5
        t1 = X + t0
    """
    manager = TACManager()
    traverser = ASTTraverser(manager)

    left = create_literal_node("X", "variavel", 13)
    right = create_literal_node("5", "numero_inteiro", 13)
    arith_op = create_arith_op_node("+", left, right, 13)
    linha = create_linha_node(arith_op, 13, "int")

    ast = {"arvore_atribuida": [linha]}
    instructions = traverser.generate_tac(ast)

    # Only 2 instructions: t0 = 5, then t1 = X + t0
    assert len(instructions) == 2

    # t0 = 5
    assert isinstance(instructions[0], TACAssignment)
    assert instructions[0].source == "5"

    # t1 = X + t0
    assert isinstance(instructions[1], TACBinaryOp)
    assert instructions[1].operand1 == "X"
    assert instructions[1].operator == "+"
    assert instructions[1].operand2 == "t0"


def test_subtraction_with_variables():
    """
    Test subtraction with two variables: (A X -)

    Expected TAC:
        t0 = A - X
    """
    manager = TACManager()
    traverser = ASTTraverser(manager)

    left = create_literal_node("A", "variavel", 14)
    right = create_literal_node("X", "variavel", 14)
    arith_op = create_arith_op_node("-", left, right, 14)
    linha = create_linha_node(arith_op, 14, "int")

    ast = {"arvore_atribuida": [linha]}
    instructions = traverser.generate_tac(ast)

    # Only 1 instruction: t0 = A - X
    assert len(instructions) == 1

    assert isinstance(instructions[0], TACBinaryOp)
    assert instructions[0].operand1 == "A"
    assert instructions[0].operator == "-"
    assert instructions[0].operand2 == "X"


# ============================================================================
# NESTED EXPRESSIONS TESTS
# ============================================================================

def test_nested_expression():
    """
    Test nested expression: ((5 3 +) (2 4 *) *)

    This represents: (5+3) * (2*4)

    Expected TAC:
        t0 = 5
        t1 = 3
        t2 = t0 + t1
        t3 = 2
        t4 = 4
        t5 = t3 * t4
        t6 = t2 * t5
    """
    manager = TACManager()
    traverser = ASTTraverser(manager)

    # Build (5 3 +)
    left_left = create_literal_node("5", "numero_inteiro", 22)
    left_right = create_literal_node("3", "numero_inteiro", 22)
    left_add = create_arith_op_node("+", left_left, left_right, 22)

    # Build (2 4 *)
    right_left = create_literal_node("2", "numero_inteiro", 22)
    right_right = create_literal_node("4", "numero_inteiro", 22)
    right_mul = create_arith_op_node("*", right_left, right_right, 22)

    # Build top-level multiplication
    top_mul = create_arith_op_node("*", left_add, right_mul, 22)
    linha = create_linha_node(top_mul, 22, "int")

    ast = {"arvore_atribuida": [linha]}
    instructions = traverser.generate_tac(ast)

    assert len(instructions) == 7

    # Verify sequence
    assert instructions[0].dest == "t0"  # t0 = 5
    assert instructions[1].dest == "t1"  # t1 = 3
    assert instructions[2].result == "t2"  # t2 = t0 + t1
    assert instructions[3].dest == "t3"  # t3 = 2
    assert instructions[4].dest == "t4"  # t4 = 4
    assert instructions[5].result == "t5"  # t5 = t3 * t4
    assert instructions[6].result == "t6"  # t6 = t2 * t5

    # Verify final operation
    assert instructions[6].operand1 == "t2"
    assert instructions[6].operator == "*"
    assert instructions[6].operand2 == "t5"


def test_deeply_nested_expression():
    """
    Test deeply nested expression: (((5 3 +) 2 *) 1 -)

    This represents: ((5+3) * 2) - 1

    Expected TAC:
        t0 = 5
        t1 = 3
        t2 = t0 + t1
        t3 = 2
        t4 = t2 * t3
        t5 = 1
        t6 = t4 - t5
    """
    manager = TACManager()
    traverser = ASTTraverser(manager)

    # Build (5 3 +)
    inner_left = create_literal_node("5", "numero_inteiro", 1)
    inner_right = create_literal_node("3", "numero_inteiro", 1)
    inner_add = create_arith_op_node("+", inner_left, inner_right, 1)

    # Build ((5 3 +) 2 *)
    mid_right = create_literal_node("2", "numero_inteiro", 1)
    mid_mul = create_arith_op_node("*", inner_add, mid_right, 1)

    # Build (((5 3 +) 2 *) 1 -)
    outer_right = create_literal_node("1", "numero_inteiro", 1)
    outer_sub = create_arith_op_node("-", mid_mul, outer_right, 1)

    linha = create_linha_node(outer_sub, 1, "int")
    ast = {"arvore_atribuida": [linha]}
    instructions = traverser.generate_tac(ast)

    assert len(instructions) == 7
    assert instructions[6].result == "t6"
    assert instructions[6].operator == "-"


# ============================================================================
# MULTIPLE LINES TESTS
# ============================================================================

def test_multiple_lines():
    """
    Test processing multiple lines in sequence.

    Line 1: (5 3 +)
    Line 2: (10 2 *)
    """
    manager = TACManager()
    traverser = ASTTraverser(manager)

    # Line 1: (5 3 +)
    l1_left = create_literal_node("5", "numero_inteiro", 1)
    l1_right = create_literal_node("3", "numero_inteiro", 1)
    l1_op = create_arith_op_node("+", l1_left, l1_right, 1)
    linha1 = create_linha_node(l1_op, 1, "int")

    # Line 2: (10 2 *)
    l2_left = create_literal_node("10", "numero_inteiro", 2)
    l2_right = create_literal_node("2", "numero_inteiro", 2)
    l2_op = create_arith_op_node("*", l2_left, l2_right, 2)
    linha2 = create_linha_node(l2_op, 2, "int")

    ast = {"arvore_atribuida": [linha1, linha2]}
    instructions = traverser.generate_tac(ast)

    # Line 1 generates 3 instructions, Line 2 generates 3 instructions
    assert len(instructions) == 6

    # Verify line numbers are preserved
    assert instructions[0].line == 1
    assert instructions[1].line == 1
    assert instructions[2].line == 1
    assert instructions[3].line == 2
    assert instructions[4].line == 2
    assert instructions[5].line == 2


# ============================================================================
# LINE NUMBER TRACKING TESTS
# ============================================================================

def test_line_number_preservation():
    """Test that line numbers are correctly preserved in TAC."""
    manager = TACManager()
    traverser = ASTTraverser(manager)

    left = create_literal_node("100", "numero_inteiro", 42)
    right = create_literal_node("50", "numero_inteiro", 42)
    arith_op = create_arith_op_node("+", left, right, 42)
    linha = create_linha_node(arith_op, 42, "int")

    ast = {"arvore_atribuida": [linha]}
    instructions = traverser.generate_tac(ast)

    # All instructions should have line number 42
    assert all(instr.line == 42 for instr in instructions)


# ============================================================================
# STATISTICS TESTS
# ============================================================================

def test_statistics():
    """Test that statistics are correctly tracked."""
    manager = TACManager()
    traverser = ASTTraverser(manager)

    # Generate some TAC
    left = create_literal_node("5", "numero_inteiro", 1)
    right = create_literal_node("3", "numero_inteiro", 1)
    arith_op = create_arith_op_node("+", left, right, 1)
    linha = create_linha_node(arith_op, 1, "int")

    ast = {"arvore_atribuida": [linha]}
    traverser.generate_tac(ast)

    stats = traverser.get_statistics()

    assert stats["total_instructions"] == 3
    assert stats["temp_count"] == 3  # t0, t1, t2
    assert stats["label_count"] == 0  # No labels yet


# ============================================================================
# REAL AST SNIPPET TESTS
# ============================================================================

def test_real_ast_line_1():
    """
    Test with real AST snippet from arvore_atribuida.json - Line 1.

    Line 1: (5 3 +)
    """
    manager = TACManager()
    traverser = ASTTraverser(manager)

    ast = {
        "arvore_atribuida": [
            {
                "tipo_vertice": "LINHA",
                "tipo_inferido": "int",
                "numero_linha": 1,
                "filhos": [
                    {
                        "tipo_vertice": "ARITH_OP",
                        "tipo_inferido": None,
                        "numero_linha": 1,
                        "filhos": [
                            {
                                "tipo_vertice": "LINHA",
                                "tipo_inferido": None,
                                "numero_linha": 1,
                                "filhos": [],
                                "valor": "5",
                                "subtipo": "numero_inteiro"
                            },
                            {
                                "tipo_vertice": "LINHA",
                                "tipo_inferido": None,
                                "numero_linha": 1,
                                "filhos": [],
                                "valor": "3",
                                "subtipo": "numero_inteiro"
                            }
                        ],
                        "operador": "+"
                    }
                ]
            }
        ]
    }

    instructions = traverser.generate_tac(ast)

    assert len(instructions) == 3
    assert instructions[0].to_string() == "t0 = 5"
    assert instructions[1].to_string() == "t1 = 3"
    assert instructions[2].to_string() == "t2 = t0 + t1"


def test_real_ast_line_2():
    """
    Test with real AST snippet - Line 2: (10.5 2.0 *)
    """
    manager = TACManager()
    traverser = ASTTraverser(manager)

    ast = {
        "arvore_atribuida": [
            {
                "tipo_vertice": "LINHA",
                "tipo_inferido": "real",
                "numero_linha": 2,
                "filhos": [
                    {
                        "tipo_vertice": "ARITH_OP",
                        "tipo_inferido": None,
                        "numero_linha": 2,
                        "filhos": [
                            {
                                "tipo_vertice": "LINHA",
                                "tipo_inferido": None,
                                "numero_linha": 2,
                                "filhos": [],
                                "valor": "10.5",
                                "subtipo": "numero_real"
                            },
                            {
                                "tipo_vertice": "LINHA",
                                "tipo_inferido": None,
                                "numero_linha": 2,
                                "filhos": [],
                                "valor": "2.0",
                                "subtipo": "numero_real"
                            }
                        ],
                        "operador": "*"
                    }
                ]
            }
        ]
    }

    instructions = traverser.generate_tac(ast)

    assert len(instructions) == 3
    assert instructions[0].data_type == "real"
    assert instructions[1].data_type == "real"
    assert instructions[2].to_string() == "t2 = t0 * t1"


# ============================================================================
# POST-ORDER VERIFICATION TESTS
# ============================================================================

def test_post_order_traversal():
    """
    Verify that traversal is indeed post-order (children before parents).

    For (5 3 +), the order should be:
    1. Visit 5 (left child)
    2. Visit 3 (right child)
    3. Visit + (parent)
    """
    manager = TACManager()
    traverser = ASTTraverser(manager)

    left = create_literal_node("5", "numero_inteiro", 1)
    right = create_literal_node("3", "numero_inteiro", 1)
    arith_op = create_arith_op_node("+", left, right, 1)
    linha = create_linha_node(arith_op, 1, "int")

    ast = {"arvore_atribuida": [linha]}
    instructions = traverser.generate_tac(ast)

    # Post-order: children (5, 3) processed before parent (+)
    # So we should have: t0=5, t1=3, THEN t2=t0+t1
    assert instructions[0].to_string() == "t0 = 5"  # Left child
    assert instructions[1].to_string() == "t1 = 3"  # Right child
    assert instructions[2].to_string() == "t2 = t0 + t1"  # Parent


# ============================================================================
# PYTEST FIXTURES
# ============================================================================

@pytest.fixture
def fresh_traverser():
    """Fixture providing a fresh ASTTraverser with new TACManager."""
    manager = TACManager()
    return ASTTraverser(manager)


def test_with_fresh_traverser_fixture(fresh_traverser):
    """Test using the fresh_traverser fixture."""
    assert fresh_traverser.instructions == []
    assert fresh_traverser.manager.get_temp_count() == 0


# ============================================================================
# COMPARISON AND LOGICAL OPERATIONS STUB TESTS
# ============================================================================

def test_comparison_operation_stub():
    """
    Test comparison operation stub (Issue 1.5 - not fully implemented).

    Line 7: (5.5 3.2 >)
    """
    manager = TACManager()
    traverser = ASTTraverser(manager)

    ast = {
        "arvore_atribuida": [
            {
                "tipo_vertice": "LINHA",
                "tipo_inferido": "boolean",
                "numero_linha": 7,
                "filhos": [
                    {
                        "tipo_vertice": "COMP_OP",
                        "tipo_inferido": None,
                        "numero_linha": 7,
                        "filhos": [
                            {
                                "tipo_vertice": "LINHA",
                                "tipo_inferido": None,
                                "numero_linha": 7,
                                "filhos": [],
                                "valor": "5.5",
                                "subtipo": "numero_real"
                            },
                            {
                                "tipo_vertice": "LINHA",
                                "tipo_inferido": None,
                                "numero_linha": 7,
                                "filhos": [],
                                "valor": "3.2",
                                "subtipo": "numero_real"
                            }
                        ],
                        "operador": ">"
                    }
                ]
            }
        ]
    }

    instructions = traverser.generate_tac(ast)

    # Stub should still generate TAC
    assert len(instructions) == 3
    assert instructions[2].operator == ">"
    assert instructions[2].data_type == "boolean"


def test_logical_operation_stub():
    """
    Test logical operation stub (Issue 1.5 - not fully implemented).
    """
    manager = TACManager()
    traverser = ASTTraverser(manager)

    # Simple (true false &&)
    left = create_literal_node("1", "numero_inteiro", 8)
    right = create_literal_node("0", "numero_inteiro", 8)

    logic_op = {
        "tipo_vertice": "LOGIC_OP",
        "tipo_inferido": None,
        "numero_linha": 8,
        "filhos": [left, right],
        "operador": "&&"
    }

    linha = create_linha_node(logic_op, 8, "boolean")
    ast = {"arvore_atribuida": [linha]}

    instructions = traverser.generate_tac(ast)

    # Stub should generate TAC
    assert len(instructions) == 3
    assert instructions[2].operator == "&&"


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

def test_control_flow_not_implemented():
    """Test that control flow operations raise NotImplementedError."""
    manager = TACManager()
    traverser = ASTTraverser(manager)

    control_node = {
        "tipo_vertice": "CONTROL_OP",
        "tipo_inferido": None,
        "numero_linha": 17,
        "operador": "WHILE",
        "filhos": []
    }

    with pytest.raises(NotImplementedError) as exc_info:
        traverser._handle_control_flow(control_node)

    assert "WHILE" in str(exc_info.value)
    assert "Issue 1.7" in str(exc_info.value)
