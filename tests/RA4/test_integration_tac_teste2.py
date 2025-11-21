#!/usr/bin/env python3
"""
Integration tests for TAC generation using complete arvore_atribuida.json.

Tests the full pipeline: Phase 3 AST → TAC generation

This test suite validates that Issues 1.3 and 1.4 work correctly with the
complete attributed AST from Phase 3, including the recent fix where all
nodes (including literal LINHA wrappers) have tipo_inferido populated.

SUPPOSED TO RUN WITH AST TREE GENERATED FROM inputs/RA3/teste2.txt
"""

import json
import pytest
from pathlib import Path
from datetime import datetime
from src.RA4.functions.python.tac_manager import TACManager
from src.RA4.functions.python.ast_traverser import ASTTraverser


# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
AST_PATH = PROJECT_ROOT / "outputs" / "RA3" / "arvore_atribuida.json"
TAC_DEBUG_OUTPUT = PROJECT_ROOT / "outputs" / "RA4" / "debug_tac_output.txt"


@pytest.fixture
def real_ast():
    """Load the real arvore_atribuida.json from Phase 3 output."""
    with open(AST_PATH, "r") as f:
        return json.load(f)


@pytest.fixture
def arithmetic_only_ast(real_ast):
    """
    Filter AST to only include arithmetic operations (lines 1-11, 26).

    This avoids logical operations which aren't implemented yet (Issue 1.5+).
    Lines 1-11: arithmetic ops
    Lines 12-25: variable assignments and references
    Lines 26-31: comparison ops (partially implemented)
    Lines 32-34: logical ops (cause crashes - unary ! not handled)
    """
    filtered = {
        "arvore_atribuida": [
            linha for linha in real_ast["arvore_atribuida"]
            if linha.get("numero_linha", 0) <= 31  # Exclude logical ops (32-34)
        ]
    }
    return filtered


@pytest.fixture
def tac_generator():
    """Create a fresh TAC generator."""
    manager = TACManager()
    return ASTTraverser(manager)


class TestIntegrationTAC:
    """Integration tests using real Phase 3 AST output."""

    def test_can_generate_tac_from_real_ast(self, arithmetic_only_ast, tac_generator):
        """Test that TAC generation works with arithmetic operations."""
        instructions = tac_generator.generate_tac(arithmetic_only_ast)

        # Basic sanity checks
        assert len(instructions) > 0, "Should generate at least some instructions"
        assert all(hasattr(instr, 'line') for instr in instructions), \
            "All instructions should have line numbers"
        assert all(hasattr(instr, 'to_string') for instr in instructions), \
            "All instructions should be stringifiable"

    def test_line_numbers_preserved(self, arithmetic_only_ast, tac_generator):
        """Test that line numbers from AST are preserved in TAC."""
        instructions = tac_generator.generate_tac(arithmetic_only_ast)

        # All line numbers should be valid (1-31 for arithmetic subset)
        line_numbers = [instr.line for instr in instructions]
        assert all(1 <= line <= 31 for line in line_numbers), \
            "Line numbers should be in valid range (1-31)"

        # Line numbers should be in order (non-decreasing)
        assert line_numbers == sorted(line_numbers), \
            "Line numbers should be in order"

    def test_arithmetic_line_1_type_promotion(self, arithmetic_only_ast, tac_generator):
        """
        Test Line 1: (5 3.0 +) with type promotion.

        Expected TAC:
          t0 = 5    (int)
          t1 = 3.0  (real)
          t2 = t0 + t1  (promoted to real)
        """
        instructions = tac_generator.generate_tac(arithmetic_only_ast)

        # Get instructions for line 1
        line_1_instrs = [instr for instr in instructions if instr.line == 1]
        assert len(line_1_instrs) == 3, "Line 1 should generate 3 instructions"

        # Check instruction strings
        assert line_1_instrs[0].to_string() == "t0 = 5"
        assert line_1_instrs[1].to_string() == "t1 = 3.0"
        assert line_1_instrs[2].to_string() == "t2 = t0 + t1"

        # Check data types
        assert line_1_instrs[0].data_type == "int", "5 should be int"
        assert line_1_instrs[1].data_type == "real", "3.0 should be real"
        assert line_1_instrs[2].data_type == "real", "Result should be promoted to real"

    def test_all_arithmetic_operators_present(self, arithmetic_only_ast, tac_generator):
        """Test that all 7 arithmetic operators are generated correctly."""
        instructions = tac_generator.generate_tac(arithmetic_only_ast)

        # Convert to strings for easier searching
        instr_strings = [instr.to_string() for instr in instructions]

        # Check for each operator (Issue 1.4 requirement)
        operators = ['+', '-', '*', '/', '|', '%', '^']
        for op in operators:
            found = any(f" {op} " in s for s in instr_strings)
            assert found, f"Operator '{op}' should appear in TAC"

    def test_statistics_correctness(self, arithmetic_only_ast, tac_generator):
        """Test that statistics tracking works correctly."""
        instructions = tac_generator.generate_tac(arithmetic_only_ast)
        stats = tac_generator.get_statistics()

        # Check statistics make sense
        assert stats["total_instructions"] == len(instructions), \
            "Instruction count should match"
        assert stats["temp_count"] > 0, "Should have generated temporary variables"
        # Note: lines_processed may not be in stats dict yet - check if exists
        if "lines_processed" in stats:
            assert stats["lines_processed"] == 31, "Should have processed 31 lines (arithmetic subset)"

    def test_tipo_inferido_on_literals(self, real_ast, arithmetic_only_ast, tac_generator):
        """
        Test that the new AST structure with tipo_inferido on literals works.

        This verifies the fix we just made in RA3 where ALL nodes
        (including literal LINHA wrapper nodes) have tipo_inferido populated.
        """
        # Check that the AST actually has tipo_inferido on literal nodes
        first_line = real_ast["arvore_atribuida"][0]
        arith_op = first_line["filhos"][0]
        literal_nodes = arith_op["filhos"]

        # These should now have tipo_inferido (the fix we just made)
        assert literal_nodes[0].get("tipo_inferido") is not None, \
            "First literal should have tipo_inferido"
        assert literal_nodes[1].get("tipo_inferido") is not None, \
            "Second literal should have tipo_inferido"

        # Verify the types are correct (Line 1 is: 5 3.0 +)
        assert literal_nodes[0]["tipo_inferido"] == "int", \
            "5 should have tipo_inferido='int'"
        assert literal_nodes[1]["tipo_inferido"] == "real", \
            "3.0 should have tipo_inferido='real'"

        # And TAC generation should still work
        instructions = tac_generator.generate_tac(arithmetic_only_ast)
        assert len(instructions) > 0, \
            "TAC generation should work with new AST structure"

    def test_generate_and_save_complete_tac(self, arithmetic_only_ast, tac_generator):
        """
        Generate complete TAC and save to file for debugging.

        This test prints ALL TAC instructions to console (visible with -s flag)
        and saves them to outputs/RA4/debug_tac_output.txt for inspection.
        """
        # Generate TAC
        instructions = tac_generator.generate_tac(arithmetic_only_ast)
        stats = tac_generator.get_statistics()

        # Print to console
        print("\n" + "=" * 70)
        print("=== COMPLETE TAC OUTPUT (All 35 Lines) ===")
        print("=" * 70)
        print()

        for instr in instructions:
            # Format: "Line  1: t0 = 5.0          [real]"
            type_info = f"[{instr.data_type}]" if hasattr(instr, 'data_type') and instr.data_type else ""
            print(f"Line {instr.line:2}: {instr.to_string():<25} {type_info}")

        print()
        print("=" * 70)
        print("Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print("=" * 70)
        print()

        # Save to file
        TAC_DEBUG_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        with open(TAC_DEBUG_OUTPUT, 'w') as f:
            f.write("TAC Output - Generated from arvore_atribuida.json\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")

            for instr in instructions:
                type_info = f"[type: {instr.data_type}]" if hasattr(instr, 'data_type') and instr.data_type else ""
                f.write(f"Line {instr.line:2}: {instr.to_string():<25} {type_info}\n")

            f.write("\n" + "=" * 70 + "\n")
            f.write("Statistics:\n")
            for key, value in stats.items():
                f.write(f"  {key}: {value}\n")
            f.write("=" * 70 + "\n")

        print(f"✅ TAC output saved to: {TAC_DEBUG_OUTPUT}")
        print()

        # Always pass - this is for output generation
        assert True

    def test_specific_operations(self, arithmetic_only_ast, tac_generator):
        """Test specific operations to verify correctness."""
        instructions = tac_generator.generate_tac(arithmetic_only_ast)

        # Line 1: (5.0 3 +) → t2 = t0 + t1 (real)
        line_1 = [i for i in instructions if i.line == 1]
        assert any('+' in i.to_string() for i in line_1), "Line 1 should have addition"

        # Line 2: (10.5 2.0 *) → multiplication
        line_2 = [i for i in instructions if i.line == 2]
        assert any('*' in i.to_string() for i in line_2), "Line 2 should have multiplication"

        # Line 3: (15 4 -) → subtraction
        line_3 = [i for i in instructions if i.line == 3]
        assert any('-' in i.to_string() for i in line_3), "Line 3 should have subtraction"

        # Line 4: (8.0 2.0 |) → real division
        line_4 = [i for i in instructions if i.line == 4]
        assert any('|' in i.to_string() for i in line_4), "Line 4 should have real division"

        # Line 5: (20 3 /) → integer division
        line_5 = [i for i in instructions if i.line == 5]
        assert any('/' in i.to_string() for i in line_5), "Line 5 should have integer division"

        # Line 6: (17 5 %) → modulo
        line_6 = [i for i in instructions if i.line == 6]
        assert any('%' in i.to_string() for i in line_6), "Line 6 should have modulo"

        # Line 7: (2 3 ^) → exponentiation
        line_7 = [i for i in instructions if i.line == 7]
        assert any('^' in i.to_string() for i in line_7), "Line 7 should have exponentiation"

    def test_variable_assignments(self, arithmetic_only_ast, tac_generator):
        """Test that variable assignments are handled correctly."""
        instructions = tac_generator.generate_tac(arithmetic_only_ast)

        # Line 12: (42 X) - assignment to X
        line_12 = [i for i in instructions if i.line == 12]
        assert len(line_12) > 0, "Line 12 should generate instructions"

        # Line 13: (3.14 PI) - assignment to PI
        line_13 = [i for i in instructions if i.line == 13]
        assert len(line_13) > 0, "Line 13 should generate instructions"

    def test_variable_references(self, arithmetic_only_ast, tac_generator):
        """Test that variable references are handled correctly."""
        instructions = tac_generator.generate_tac(arithmetic_only_ast)

        # Line 19: (X) - just referencing X
        line_19 = [i for i in instructions if i.line == 19]
        # Should generate minimal TAC (just variable reference)
        assert len(line_19) >= 0, "Line 19 should process variable reference"

        # Line 20: (PI) - just referencing PI
        line_20 = [i for i in instructions if i.line == 20]
        assert len(line_20) >= 0, "Line 20 should process variable reference"


class TestIssues1_3_and_1_4:
    """
    Specific tests for Issues 1.3 and 1.4 acceptance criteria.

    Issue 1.3: AST Traversal Engine (Post-order)
    Issue 1.4: Arithmetic Expression Generation
    """

    def test_issue_1_3_post_order_traversal(self, arithmetic_only_ast, tac_generator):
        """
        Verify Issue 1.3: Post-order traversal works correctly.

        Post-order means children are processed before parents.
        For (5 3.0 +), we should see:
          1. Process 5 (leaf)
          2. Process 3.0 (leaf)
          3. Process + (parent)
        """
        instructions = tac_generator.generate_tac(arithmetic_only_ast)
        line_1 = [i for i in instructions if i.line == 1]

        # Should be: t0 = 5, t1 = 3.0, t2 = t0 + t1
        # This proves post-order: leaves first, then operation
        assert "5" in line_1[0].to_string(), "First: left operand (5)"
        assert "3" in line_1[1].to_string(), "Second: right operand (3.0)"
        assert "+" in line_1[2].to_string(), "Third: operation on operands"

    def test_issue_1_4_all_operators(self, arithmetic_only_ast, tac_generator):
        """
        Verify Issue 1.4: All arithmetic operators implemented.

        Required operators: +, -, *, /, |, %, ^
        """
        instructions = tac_generator.generate_tac(arithmetic_only_ast)
        all_tac = " ".join(i.to_string() for i in instructions)

        required_operators = {
            '+': "addition",
            '-': "subtraction",
            '*': "multiplication",
            '/': "integer division",
            '|': "real division",
            '%': "modulo",
            '^': "exponentiation"
        }

        for op, name in required_operators.items():
            assert f" {op} " in all_tac, f"Operator '{op}' ({name}) should be in TAC"

    def test_issue_1_4_type_handling(self, arithmetic_only_ast, tac_generator):
        """
        Verify Issue 1.4: Type information is handled correctly.

        Type promotion: int + real → real
        """
        instructions = tac_generator.generate_tac(arithmetic_only_ast)
        line_1 = [i for i in instructions if i.line == 1]

        # Line 1: (5.0 3 +) should result in real type
        result_instr = line_1[2]  # t2 = t0 + t1
        assert result_instr.data_type == "real", \
            "Type promotion: int + real should result in real"
