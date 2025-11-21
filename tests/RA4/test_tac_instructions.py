"""
Test suite for TAC instruction classes

This file tests all TAC instruction types to ensure they:
1. Generate correct string representation (to_string)
2. Generate correct JSON representation (to_dict)
3. Correctly identify defined variables (defines_variable)
4. Correctly identify used variables (uses_variables)

Run with pytest:
    pytest tests/RA4/test_tac_instructions.py -v

Or run all RA4 tests:
    pytest tests/RA4/ -v
"""

import sys
import os
import json
import pytest

# Add project root to path to allow imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Import TAC instruction classes
from src.RA4.functions.python.tac_instructions import (
    TACInstruction,
    TACAssignment,
    TACCopy,
    TACBinaryOp,
    TACUnaryOp,
    TACLabel,
    TACGoto,
    TACIfGoto,
    TACIfFalseGoto,
    TACMemoryRead,
    TACMemoryWrite,
    TACCall,
    TACReturn,
    instruction_from_dict,
)


# ============================================================================
# TEST: ASSIGNMENT INSTRUCTIONS
# ============================================================================

def test_assignment_with_literal():
    """Test TACAssignment with literal value"""
    instr = TACAssignment("t0", "5", line=1, data_type="int")

    assert instr.to_string() == "t0 = 5"
    assert instr.defines_variable == "t0"
    assert instr.uses_variables == []

    # Test JSON serialization
    data = instr.to_dict()
    assert data["type"] == "assignment"
    assert data["dest"] == "t0"
    assert data["source"] == "5"
    assert data["line"] == 1
    assert data["data_type"] == "int"


def test_assignment_with_variable():
    """Test TACAssignment with variable"""
    instr = TACAssignment("t1", "X", line=2, data_type="int")

    assert instr.to_string() == "t1 = X"
    assert instr.defines_variable == "t1"
    assert instr.uses_variables == ["X"]


def test_copy_instruction():
    """Test TACCopy instruction"""
    instr = TACCopy("a", "b", line=3, data_type="int")

    assert instr.to_string() == "a = b"
    assert instr.defines_variable == "a"
    assert instr.uses_variables == ["b"]


# ============================================================================
# TEST: OPERATION INSTRUCTIONS
# ============================================================================

def test_binary_op_with_temporaries():
    """Test TACBinaryOp with temporary variables"""
    instr = TACBinaryOp("t2", "t0", "+", "t1", line=3, data_type="int")

    assert instr.to_string() == "t2 = t0 + t1"
    assert instr.defines_variable == "t2"
    assert instr.uses_variables == ["t0", "t1"]


def test_binary_op_comparison():
    """Test TACBinaryOp with comparison operator"""
    instr = TACBinaryOp("t3", "X", ">", "5", line=4, data_type="boolean")

    assert instr.to_string() == "t3 = X > 5"
    assert instr.defines_variable == "t3"
    assert instr.uses_variables == ["X"]  # "5" is constant, not included


def test_binary_op_real_division():
    """Test TACBinaryOp with real division"""
    instr = TACBinaryOp("t4", "10.5", "|", "2.0", line=5, data_type="real")

    assert instr.to_string() == "t4 = 10.5 | 2.0"
    assert instr.defines_variable == "t4"
    assert instr.uses_variables == []  # Both operands are constants


def test_binary_op_all_operators():
    """Test TACBinaryOp with all supported operators"""
    operators = ["+", "-", "*", "/", "|", "%", "^", ">", "<", ">=", "<=", "==", "!=", "&&", "||"]

    for op in operators:
        instr = TACBinaryOp("t0", "a", op, "b", line=1)
        assert op in instr.to_string()


def test_unary_op_negation():
    """Test TACUnaryOp with negation"""
    instr = TACUnaryOp("t5", "-", "X", line=6, data_type="int")

    assert instr.to_string() == "t5 = -X"
    assert instr.defines_variable == "t5"
    assert instr.uses_variables == ["X"]


def test_unary_op_logical_not():
    """Test TACUnaryOp with logical NOT"""
    instr = TACUnaryOp("t6", "!", "condition", line=7, data_type="boolean")

    assert instr.to_string() == "t6 = !condition"
    assert instr.defines_variable == "t6"
    assert instr.uses_variables == ["condition"]


# ============================================================================
# TEST: CONTROL FLOW INSTRUCTIONS
# ============================================================================

def test_label():
    """Test TACLabel instruction"""
    label = TACLabel("L1", line=8)

    assert label.to_string() == "L1:"
    assert label.defines_variable is None
    assert label.uses_variables == []


def test_goto():
    """Test TACGoto instruction"""
    goto = TACGoto("L1", line=9)

    assert goto.to_string() == "goto L1"
    assert goto.defines_variable is None
    assert goto.uses_variables == []


def test_if_goto():
    """Test TACIfGoto instruction"""
    if_goto = TACIfGoto("t5", "L2", line=10)

    assert if_goto.to_string() == "if t5 goto L2"
    assert if_goto.defines_variable is None
    assert if_goto.uses_variables == ["t5"]


def test_if_false_goto():
    """Test TACIfFalseGoto instruction"""
    if_false = TACIfFalseGoto("t6", "L3", line=11)

    assert if_false.to_string() == "ifFalse t6 goto L3"
    assert if_false.defines_variable is None
    assert if_false.uses_variables == ["t6"]


def test_if_goto_with_constant_condition():
    """Test TACIfGoto with constant condition"""
    if_goto = TACIfGoto("0", "L1", line=12)

    assert if_goto.to_string() == "if 0 goto L1"
    assert if_goto.uses_variables == []  # "0" is constant


# ============================================================================
# TEST: MEMORY ACCESS INSTRUCTIONS
# ============================================================================

def test_memory_read():
    """Test TACMemoryRead instruction"""
    mem_read = TACMemoryRead("t7", "X", line=12, data_type="int")

    assert mem_read.to_string() == "t7 = MEM[X]"
    assert mem_read.defines_variable == "t7"
    assert mem_read.uses_variables == ["X"]

    # Test JSON serialization
    data = mem_read.to_dict()
    assert data["type"] == "memory_read"
    assert data["result"] == "t7"
    assert data["address"] == "X"


def test_memory_write():
    """Test TACMemoryWrite instruction"""
    mem_write = TACMemoryWrite("Y", "t8", line=13, data_type="int")

    assert mem_write.to_string() == "MEM[Y] = t8"
    assert mem_write.defines_variable == "Y"
    assert mem_write.uses_variables == ["t8"]


# ============================================================================
# TEST: FUNCTION INSTRUCTIONS
# ============================================================================

def test_call():
    """Test TACCall instruction"""
    call = TACCall("t9", "factorial", 1, line=14, data_type="int")

    assert call.to_string() == "t9 = call factorial, 1"
    assert call.defines_variable == "t9"
    assert call.uses_variables == []


def test_return():
    """Test TACReturn instruction"""
    ret = TACReturn("t10", line=15, data_type="int")

    assert ret.to_string() == "return t10"
    assert ret.defines_variable is None
    assert ret.uses_variables == ["t10"]


def test_return_with_constant():
    """Test TACReturn with constant value"""
    ret = TACReturn("42", line=16, data_type="int")

    assert ret.to_string() == "return 42"
    assert ret.uses_variables == []  # "42" is constant


# ============================================================================
# TEST: COMPLETE PROGRAM EXAMPLES
# ============================================================================

def test_complete_tac_program():
    """Test generating a complete TAC program for: (5 3 +)"""
    instructions = [
        TACAssignment("t0", "5", line=1, data_type="int"),
        TACAssignment("t1", "3", line=1, data_type="int"),
        TACBinaryOp("t2", "t0", "+", "t1", line=1, data_type="int"),
    ]

    # Verify string representation
    assert instructions[0].to_string() == "t0 = 5"
    assert instructions[1].to_string() == "t1 = 3"
    assert instructions[2].to_string() == "t2 = t0 + t1"

    # Verify JSON serialization
    tac_json = {"instructions": [instr.to_dict() for instr in instructions]}
    assert len(tac_json["instructions"]) == 3
    assert tac_json["instructions"][0]["type"] == "assignment"
    assert tac_json["instructions"][2]["type"] == "binary_op"


def test_variable_analysis():
    """Test variable usage analysis"""
    instructions = [
        TACAssignment("t0", "5", line=1, data_type="int"),
        TACAssignment("t1", "3", line=1, data_type="int"),
        TACBinaryOp("t2", "t0", "+", "t1", line=1, data_type="int"),
    ]

    all_defined = set()
    all_used = set()

    for instr in instructions:
        if instr.defines_variable:
            all_defined.add(instr.defines_variable)
        all_used.update(instr.uses_variables)

    assert all_defined == {"t0", "t1", "t2"}
    assert all_used == {"t0", "t1"}
    assert all_defined - all_used == {"t2"}  # t2 is defined but never used (dead code)


# ============================================================================
# TEST: OPTIMIZATION SCENARIOS
# ============================================================================

def test_constant_folding_detection():
    """Test detection of constant folding opportunities"""
    # This instruction can be folded at compile time: 2 + 3 = 5
    instr = TACBinaryOp("t0", "2", "+", "3", line=1, data_type="int")

    # Both operands are constants
    assert TACInstruction.is_constant("2")
    assert TACInstruction.is_constant("3")
    assert instr.uses_variables == []  # No variables used


def test_dead_code_detection():
    """Test detection of dead code"""
    instructions = [
        TACAssignment("t0", "2", line=1, data_type="int"),
        TACAssignment("t1", "3", line=2, data_type="int"),
        TACBinaryOp("t2", "t0", "+", "t1", line=3, data_type="int"),
        TACAssignment("t3", "10", line=4, data_type="int"),  # Dead: t3 never used
        TACBinaryOp("t4", "t2", "*", "2", line=5, data_type="int"),
    ]

    defined_vars = {}
    used_vars = set()

    for i, instr in enumerate(instructions):
        if instr.defines_variable:
            defined_vars[instr.defines_variable] = i
        used_vars.update(instr.uses_variables)

    # t3 is defined but never used
    assert "t3" in defined_vars
    assert "t3" not in used_vars


# ============================================================================
# TEST: JSON SERIALIZATION
# ============================================================================

def test_serialization_roundtrip():
    """Test JSON serialization and deserialization"""
    original = TACBinaryOp("t5", "X", "+", "10", line=20, data_type="int")

    # Serialize to dict
    data = original.to_dict()

    # Deserialize back
    restored = instruction_from_dict(data)

    # Verify they match
    assert original.to_string() == restored.to_string()
    assert original.defines_variable == restored.defines_variable
    assert original.uses_variables == restored.uses_variables


def test_serialization_all_instruction_types():
    """Test serialization for all instruction types"""
    instructions = [
        TACAssignment("t0", "5", line=1),
        TACCopy("a", "b", line=2),
        TACBinaryOp("t1", "a", "+", "b", line=3),
        TACUnaryOp("t2", "-", "c", line=4),
        TACLabel("L1", line=5),
        TACGoto("L1", line=6),
        TACIfGoto("t3", "L2", line=7),
        TACIfFalseGoto("t4", "L3", line=8),
        TACMemoryRead("t5", "X", line=9),
        TACMemoryWrite("Y", "t6", line=10),
        TACCall("t7", "func", 2, line=11),
        TACReturn("t8", line=12),
    ]

    for original in instructions:
        data = original.to_dict()
        restored = instruction_from_dict(data)
        assert original.to_string() == restored.to_string()


# ============================================================================
# TEST: HELPER METHODS
# ============================================================================

def test_is_constant_method():
    """Test the is_constant static method"""
    # Integer constants
    assert TACInstruction.is_constant("0")
    assert TACInstruction.is_constant("42")
    assert TACInstruction.is_constant("-5")

    # Float constants
    assert TACInstruction.is_constant("3.14")
    assert TACInstruction.is_constant("10.5")
    assert TACInstruction.is_constant("-2.718")

    # Not constants (variables)
    assert not TACInstruction.is_constant("X")
    assert not TACInstruction.is_constant("temp")
    assert not TACInstruction.is_constant("t0")


def test_defines_variable_property():
    """Test defines_variable property for all instruction types"""
    # Should define variables
    assert TACAssignment("t0", "5", line=1).defines_variable == "t0"
    assert TACBinaryOp("t1", "a", "+", "b", line=1).defines_variable == "t1"
    assert TACUnaryOp("t2", "-", "c", line=1).defines_variable == "t2"
    assert TACMemoryRead("t3", "X", line=1).defines_variable == "t3"
    assert TACMemoryWrite("Y", "t4", line=1).defines_variable == "Y"
    assert TACCall("t5", "func", 1, line=1).defines_variable == "t5"

    # Should NOT define variables
    assert TACLabel("L1", line=1).defines_variable is None
    assert TACGoto("L1", line=1).defines_variable is None
    assert TACIfGoto("t0", "L1", line=1).defines_variable is None
    assert TACIfFalseGoto("t0", "L1", line=1).defines_variable is None
    assert TACReturn("t0", line=1).defines_variable is None


def test_uses_variables_property():
    """Test uses_variables property correctly filters constants"""
    # Should include variables only
    instr1 = TACBinaryOp("t0", "X", "+", "5", line=1)
    assert instr1.uses_variables == ["X"]  # "5" is constant, excluded

    instr2 = TACBinaryOp("t1", "10", "*", "20", line=1)
    assert instr2.uses_variables == []  # Both constants, empty list

    instr3 = TACBinaryOp("t2", "a", "-", "b", line=1)
    assert instr3.uses_variables == ["a", "b"]  # Both variables


# ============================================================================
# PYTEST MARKERS AND PARAMETRIZATION
# ============================================================================

@pytest.mark.parametrize("operator", ["+", "-", "*", "/", "|", "%", "^"])
def test_arithmetic_operators(operator):
    """Test all arithmetic operators"""
    instr = TACBinaryOp("t0", "a", operator, "b", line=1, data_type="int")
    assert operator in instr.to_string()
    assert instr.defines_variable == "t0"
    assert instr.uses_variables == ["a", "b"]


@pytest.mark.parametrize("operator", [">", "<", ">=", "<=", "==", "!="])
def test_comparison_operators(operator):
    """Test all comparison operators"""
    instr = TACBinaryOp("t0", "a", operator, "b", line=1, data_type="boolean")
    assert operator in instr.to_string()
    assert instr.defines_variable == "t0"


@pytest.mark.parametrize("operator", ["&&", "||"])
def test_logical_operators(operator):
    """Test logical operators"""
    instr = TACBinaryOp("t0", "a", operator, "b", line=1, data_type="boolean")
    assert operator in instr.to_string()


# ============================================================================
# PYTEST FIXTURES (for future use)
# ============================================================================

@pytest.fixture
def sample_tac_program():
    """Fixture providing a sample TAC program"""
    return [
        TACAssignment("t0", "5", line=1, data_type="int"),
        TACAssignment("t1", "3", line=1, data_type="int"),
        TACBinaryOp("t2", "t0", "+", "t1", line=1, data_type="int"),
    ]


def test_with_fixture(sample_tac_program):
    """Example test using pytest fixture"""
    assert len(sample_tac_program) == 3
    assert sample_tac_program[0].to_string() == "t0 = 5"
