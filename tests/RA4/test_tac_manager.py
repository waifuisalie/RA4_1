"""
Unit Tests for TAC Manager

Tests the TACManager class for temporary variable and label generation.

Run with: pytest tests/RA4/test_tac_manager.py -v
"""

import sys
import os
import pytest

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from src.RA4.functions.python.tac_manager import TACManager


# ============================================================================
# BASIC FUNCTIONALITY TESTS
# ============================================================================

def test_tac_manager_initialization():
    """Test that TACManager initializes with counters at 0."""
    manager = TACManager()

    assert manager.get_temp_count() == 0
    assert manager.get_label_count() == 0


def test_first_temp_is_t0():
    """Test that the first temporary variable is t0."""
    manager = TACManager()
    temp = manager.new_temp()

    assert temp == "t0"
    assert manager.get_temp_count() == 1


def test_first_label_is_L0():
    """Test that the first label is L0."""
    manager = TACManager()
    label = manager.new_label()

    assert label == "L0"
    assert manager.get_label_count() == 1


# ============================================================================
# TEMPORARY VARIABLE GENERATION TESTS
# ============================================================================

def test_temp_sequence():
    """Test that temporaries are generated in correct sequence: t0, t1, t2, ..."""
    manager = TACManager()

    temps = [manager.new_temp() for _ in range(10)]
    expected = [f"t{i}" for i in range(10)]

    assert temps == expected


def test_temp_uniqueness():
    """Test that each call to new_temp() returns a unique variable."""
    manager = TACManager()

    temps = [manager.new_temp() for _ in range(100)]

    # Check all temps are unique
    assert len(temps) == len(set(temps))
    # Check they are in correct sequence
    assert temps == [f"t{i}" for i in range(100)]


@pytest.mark.parametrize("count", [1, 5, 10, 50, 100])
def test_temp_generation_counts(count):
    """Test that temp counter correctly tracks the number of temps generated."""
    manager = TACManager()

    for _ in range(count):
        manager.new_temp()

    assert manager.get_temp_count() == count


# ============================================================================
# LABEL GENERATION TESTS
# ============================================================================

def test_label_sequence():
    """Test that labels are generated in correct sequence: L0, L1, L2, ..."""
    manager = TACManager()

    labels = [manager.new_label() for _ in range(10)]
    expected = [f"L{i}" for i in range(10)]

    assert labels == expected


def test_label_uniqueness():
    """Test that each call to new_label() returns a unique label."""
    manager = TACManager()

    labels = [manager.new_label() for _ in range(100)]

    # Check all labels are unique
    assert len(labels) == len(set(labels))
    # Check they are in correct sequence
    assert labels == [f"L{i}" for i in range(100)]


@pytest.mark.parametrize("count", [1, 5, 10, 50, 100])
def test_label_generation_counts(count):
    """Test that label counter correctly tracks the number of labels generated."""
    manager = TACManager()

    for _ in range(count):
        manager.new_label()

    assert manager.get_label_count() == count


# ============================================================================
# MIXED GENERATION TESTS
# ============================================================================

def test_temps_and_labels_independent():
    """Test that temp and label counters are independent."""
    manager = TACManager()

    # Generate some temps
    t0 = manager.new_temp()
    t1 = manager.new_temp()

    # Generate some labels
    l0 = manager.new_label()
    l1 = manager.new_label()

    # Generate more temps
    t2 = manager.new_temp()

    # Generate more labels
    l2 = manager.new_label()

    assert t0 == "t0"
    assert t1 == "t1"
    assert t2 == "t2"
    assert l0 == "L0"
    assert l1 == "L1"
    assert l2 == "L2"
    assert manager.get_temp_count() == 3
    assert manager.get_label_count() == 3


def test_interleaved_generation():
    """Test generating temps and labels in interleaved fashion."""
    manager = TACManager()

    results = []
    results.append(manager.new_temp())   # t0
    results.append(manager.new_label())  # L0
    results.append(manager.new_temp())   # t1
    results.append(manager.new_label())  # L1
    results.append(manager.new_temp())   # t2
    results.append(manager.new_label())  # L2

    assert results == ["t0", "L0", "t1", "L1", "t2", "L2"]


# ============================================================================
# RESET FUNCTIONALITY TESTS
# ============================================================================

def test_reset_counters_resets_temp():
    """Test that reset_counters() resets the temp counter to 0."""
    manager = TACManager()

    # Generate some temps
    manager.new_temp()  # t0
    manager.new_temp()  # t1
    manager.new_temp()  # t2

    assert manager.get_temp_count() == 3

    # Reset
    manager.reset_counters()

    assert manager.get_temp_count() == 0
    assert manager.new_temp() == "t0"


def test_reset_counters_resets_label():
    """Test that reset_counters() resets the label counter to 0."""
    manager = TACManager()

    # Generate some labels
    manager.new_label()  # L0
    manager.new_label()  # L1
    manager.new_label()  # L2

    assert manager.get_label_count() == 3

    # Reset
    manager.reset_counters()

    assert manager.get_label_count() == 0
    assert manager.new_label() == "L0"


def test_reset_counters_resets_both():
    """Test that reset_counters() resets both temp and label counters."""
    manager = TACManager()

    # Generate some of each
    manager.new_temp()   # t0
    manager.new_temp()   # t1
    manager.new_label()  # L0
    manager.new_label()  # L1
    manager.new_label()  # L2

    assert manager.get_temp_count() == 2
    assert manager.get_label_count() == 3

    # Reset
    manager.reset_counters()

    assert manager.get_temp_count() == 0
    assert manager.get_label_count() == 0
    assert manager.new_temp() == "t0"
    assert manager.new_label() == "L0"


def test_multiple_resets():
    """Test that reset_counters() can be called multiple times."""
    manager = TACManager()

    for _ in range(5):
        # Generate some items
        manager.new_temp()
        manager.new_label()

        # Reset and verify
        manager.reset_counters()
        assert manager.get_temp_count() == 0
        assert manager.get_label_count() == 0


# ============================================================================
# STATISTICS TESTS
# ============================================================================

def test_statistics_initial_state():
    """Test that statistics are correct in initial state."""
    manager = TACManager()

    stats = manager.get_statistics()

    assert stats["current_temp_count"] == 0
    assert stats["current_label_count"] == 0
    assert stats["total_temps_created"] == 0
    assert stats["total_labels_created"] == 0


def test_statistics_after_generation():
    """Test that statistics correctly track generated temps and labels."""
    manager = TACManager()

    # Generate 5 temps and 3 labels
    for _ in range(5):
        manager.new_temp()
    for _ in range(3):
        manager.new_label()

    stats = manager.get_statistics()

    assert stats["current_temp_count"] == 5
    assert stats["current_label_count"] == 3
    assert stats["total_temps_created"] == 5
    assert stats["total_labels_created"] == 3


def test_statistics_persist_across_reset():
    """Test that total statistics persist across reset_counters()."""
    manager = TACManager()

    # First program: 3 temps, 2 labels
    for _ in range(3):
        manager.new_temp()
    for _ in range(2):
        manager.new_label()

    manager.reset_counters()

    # Second program: 4 temps, 5 labels
    for _ in range(4):
        manager.new_temp()
    for _ in range(5):
        manager.new_label()

    stats = manager.get_statistics()

    # Current counts should reflect second program
    assert stats["current_temp_count"] == 4
    assert stats["current_label_count"] == 5

    # Total counts should include both programs
    assert stats["total_temps_created"] == 7  # 3 + 4
    assert stats["total_labels_created"] == 7  # 2 + 5


# ============================================================================
# STRING REPRESENTATION TESTS
# ============================================================================

def test_repr():
    """Test that __repr__ returns informative string."""
    manager = TACManager()

    manager.new_temp()
    manager.new_temp()
    manager.new_label()

    repr_str = repr(manager)

    assert "TACManager" in repr_str
    assert "temp_counter=2" in repr_str
    assert "label_counter=1" in repr_str


# ============================================================================
# INTEGRATION SCENARIO TESTS
# ============================================================================

def test_simple_expression_scenario():
    """
    Test a realistic scenario: generating TAC for expression (5 3 +).

    Expected TAC:
        t0 = 5
        t1 = 3
        t2 = t0 + t1
    """
    manager = TACManager()

    temp1 = manager.new_temp()  # For literal 5
    temp2 = manager.new_temp()  # For literal 3
    temp3 = manager.new_temp()  # For result of addition

    assert temp1 == "t0"
    assert temp2 == "t1"
    assert temp3 == "t2"
    assert manager.get_temp_count() == 3


def test_if_statement_scenario():
    """
    Test a realistic scenario: generating TAC for if statement.

    Expected pattern:
        [condition evaluation using temps]
        if condition goto L0
        [else block]
        goto L1
        L0:
        [then block]
        L1:
    """
    manager = TACManager()

    # Condition evaluation might use temps
    cond_temp = manager.new_temp()

    # Labels for control flow
    then_label = manager.new_label()
    end_label = manager.new_label()

    assert cond_temp == "t0"
    assert then_label == "L0"
    assert end_label == "L1"


def test_loop_scenario():
    """
    Test a realistic scenario: generating TAC for a loop.

    Expected pattern:
        L0:  (loop start)
        [loop body with temps]
        [condition check]
        if condition goto L0
        L1:  (loop end)
    """
    manager = TACManager()

    loop_start = manager.new_label()

    # Loop body might use several temps
    temp1 = manager.new_temp()
    temp2 = manager.new_temp()
    cond_temp = manager.new_temp()

    loop_end = manager.new_label()

    assert loop_start == "L0"
    assert temp1 == "t0"
    assert temp2 == "t1"
    assert cond_temp == "t2"
    assert loop_end == "L1"


def test_multiple_programs_scenario():
    """
    Test processing multiple programs sequentially.
    Each program should start with t0 and L0.
    """
    manager = TACManager()

    # First program
    temp1_prog1 = manager.new_temp()
    label1_prog1 = manager.new_label()

    assert temp1_prog1 == "t0"
    assert label1_prog1 == "L0"

    # Reset for second program
    manager.reset_counters()

    # Second program should start from 0
    temp1_prog2 = manager.new_temp()
    label1_prog2 = manager.new_label()

    assert temp1_prog2 == "t0"
    assert label1_prog2 == "L0"

    # But total statistics should reflect both programs
    stats = manager.get_statistics()
    assert stats["total_temps_created"] == 2
    assert stats["total_labels_created"] == 2


# ============================================================================
# PYTEST FIXTURES
# ============================================================================

@pytest.fixture
def fresh_manager():
    """Fixture providing a fresh TACManager instance for each test."""
    return TACManager()


@pytest.fixture
def populated_manager():
    """Fixture providing a TACManager with some temps and labels already generated."""
    manager = TACManager()
    manager.new_temp()  # t0
    manager.new_temp()  # t1
    manager.new_label()  # L0
    return manager


def test_with_fresh_manager_fixture(fresh_manager):
    """Test using the fresh_manager fixture."""
    assert fresh_manager.get_temp_count() == 0
    assert fresh_manager.get_label_count() == 0


def test_with_populated_manager_fixture(populated_manager):
    """Test using the populated_manager fixture."""
    assert populated_manager.get_temp_count() == 2
    assert populated_manager.get_label_count() == 1

    # Generate next items
    assert populated_manager.new_temp() == "t2"
    assert populated_manager.new_label() == "L1"
