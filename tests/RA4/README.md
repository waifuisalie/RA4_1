# Phase 4 (RA4) Test Suite

This directory contains unit tests for Phase 4: Code Generation components.

## Test Files

### `test_tac_instructions.py`
Tests for TAC (Three Address Code) instruction classes.

**Tests:**
- ✓ TACAssignment - Simple assignment instructions
- ✓ TACBinaryOp - Binary operations (arithmetic, comparison, logical)
- ✓ TACUnaryOp - Unary operations (negation, logical NOT)
- ✓ TACLabel, TACGoto, TACIfGoto, TACIfFalseGoto - Control flow
- ✓ TACMemoryRead, TACMemoryWrite - Memory access
- ✓ TACCall, TACReturn - Function calls
- ✓ Complete TAC program generation
- ✓ Optimization scenario analysis
- ✓ JSON serialization/deserialization

### `test_tac_manager.py`
Tests for TAC Manager (temporary variable and label generation).

**Tests:**
- ✓ Temporary variable generation (t0, t1, t2, ...)
- ✓ Label generation (L0, L1, L2, ...)
- ✓ Counter reset functionality
- ✓ Uniqueness guarantees
- ✓ Statistics tracking
- ✓ Integration scenarios (expressions, control flow, loops)

## Running Tests

### Recommended: Using pytest (Unit Test Framework)

**Setup (first time only):**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Run all RA4 tests:**
```bash
# Activate venv first
source venv/bin/activate

# Run all Phase 4 tests
pytest tests/RA4/ -v

# Run specific test file
pytest tests/RA4/test_tac_instructions.py -v

# Run tests matching a pattern
pytest tests/RA4/ -k "binary_op" -v
```

**Additional pytest options:**
```bash
# Run with coverage report
pytest tests/RA4/ --cov=src/RA4 --cov-report=html

# Run with detailed output
pytest tests/RA4/ -vv

# Run and stop at first failure
pytest tests/RA4/ -x

# Run parametrized tests for specific operator
pytest tests/RA4/ -k "arithmetic_operators[+]" -v
```

### Alternative: Direct execution (legacy)
```bash
python tests/RA4/test_tac_instructions.py
```

## Expected Output

With pytest, you should see:
```
======================== test session starts =========================
platform linux -- Python 3.13.7, pytest-9.0.1, pluggy-1.6.0
collected 77 items

tests/RA4/test_tac_instructions.py::test_assignment_with_literal PASSED [ 1%]
tests/RA4/test_tac_instructions.py::test_assignment_with_variable PASSED [ 2%]
...
tests/RA4/test_tac_manager.py::test_with_populated_manager_fixture PASSED [100%]

======================== 77 passed in 0.08s ==========================
```

## Test Coverage

| Component | Coverage | Status |
|-----------|----------|--------|
| TAC Instruction Classes | 100% | ✅ Complete |
| TAC Manager (Temp/Label) | 100% | ✅ Complete |
| TAC Generation | 0% | 🔜 Pending |
| TAC Optimization | 0% | 🔜 Pending |
| Assembly Generation | 0% | 🔜 Pending |

## Adding New Tests

When adding new test files:

1. Create test file in `tests/RA4/`
2. Add proper imports:
   ```python
   import sys
   import os

   project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
   sys.path.insert(0, project_root)

   from src.RA4.functions.python import ...
   ```
3. Follow naming convention: `test_*.py`
4. Update this README with test description

## Issue Tracking

- [x] Issue 1.1: TAC Instruction Classes ✅ Complete
- [x] Issue 1.2: Temporary/Label Management ✅ Complete
- [ ] Issue 1.3: AST Traversal Engine 🔜 Next
- [ ] Issue 1.4-1.7: TAC Generation Logic
- [ ] Issue 1.8: File Output

---

Last Updated: 2025-11-21
