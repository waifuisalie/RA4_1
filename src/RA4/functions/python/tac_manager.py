"""
TAC Manager - Temporary Variable and Label Management

This module provides utilities for generating unique temporary variables and labels
during TAC (Three Address Code) generation.
"""

from typing import Dict, Any


class TACManager:
    """
    Manager for generating unique temporary variables and labels for TAC generation.

    This class maintains counters for temporary variables (t0, t1, t2, ...)
    and labels (L0, L1, L2, ...) 

    Usage:
        manager = TACManager()
        temp1 = manager.new_temp()  # Returns "t0"
        temp2 = manager.new_temp()  # Returns "t1"
        label1 = manager.new_label()  # Returns "L0"

        # Reset for new program
        manager.reset_counters()
        temp3 = manager.new_temp()  # Returns "t0" again
    """

    def __init__(self):
        """Initialize the TAC manager with counters set to 0."""
        self._temp_counter = 0
        self._label_counter = 0
        self._total_temps_created = 0
        self._total_labels_created = 0

    def new_temp(self) -> str:
        """
        Generate a new unique temporary variable name.

        Follows the convention: t0, t1, t2, ...

        Returns:
            str: A unique temporary variable name (e.g., "t0", "t1", etc.)

        Example:
            >>> manager = TACManager()
            >>> manager.new_temp()
            't0'
            >>> manager.new_temp()
            't1'
        """
        temp_name = f"t{self._temp_counter}"
        self._temp_counter += 1
        self._total_temps_created += 1
        return temp_name

    def new_label(self) -> str:
        """
        Generate a new unique label name.

        Follows the convention: L0, L1, L2, ...

        Returns:
            str: A unique label name (e.g., "L0", "L1", etc.)

        Example:
            >>> manager = TACManager()
            >>> manager.new_label()
            'L0'
            >>> manager.new_label()
            'L1'
        """
        label_name = f"L{self._label_counter}"
        self._label_counter += 1
        self._total_labels_created += 1
        return label_name

    def reset_counters(self) -> None:
        """
        Reset the temporary variable and label counters to 0.

        This should be called when starting to process a new program
        to ensure temporary and label names start from t0 and L0.

        Note: This does NOT reset the total statistics counters.

        Example:
            >>> manager = TACManager()
            >>> manager.new_temp()  # Returns "t0"
            't0'
            >>> manager.new_temp()  # Returns "t1"
            't1'
            >>> manager.reset_counters()
            >>> manager.new_temp()  # Returns "t0" again
            't0'
        """
        self._temp_counter = 0
        self._label_counter = 0

    def get_temp_count(self) -> int:
        """
        Get the current temporary variable counter value.

        Returns:
            int: The next temporary variable number to be generated

        Example:
            >>> manager = TACManager()
            >>> manager.new_temp()
            't0'
            >>> manager.get_temp_count()
            1
        """
        return self._temp_counter

    def get_label_count(self) -> int:
        """
        Get the current label counter value.

        Returns:
            int: The next label number to be generated

        Example:
            >>> manager = TACManager()
            >>> manager.new_label()
            'L0'
            >>> manager.get_label_count()
            1
        """
        return self._label_counter

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about temporary variables and labels created.

        Returns:
            dict: Statistics including:
                - current_temp_count: Current temp counter value
                - current_label_count: Current label counter value
                - total_temps_created: Total temps created (across resets)
                - total_labels_created: Total labels created (across resets)

        Example:
            >>> manager = TACManager()
            >>> manager.new_temp()
            't0'
            >>> manager.new_label()
            'L0'
            >>> manager.get_statistics()
            {'current_temp_count': 1, 'current_label_count': 1, 'total_temps_created': 1, 'total_labels_created': 1}
        """
        return {
            "current_temp_count": self._temp_counter,
            "current_label_count": self._label_counter,
            "total_temps_created": self._total_temps_created,
            "total_labels_created": self._total_labels_created
        }

    def __repr__(self) -> str:
        """
        String representation of the TACManager.

        Returns:
            str: A string showing current counter values
        """
        return (f"TACManager(temp_counter={self._temp_counter}, "
                f"label_counter={self._label_counter}, "
                f"total_temps={self._total_temps_created}, "
                f"total_labels={self._total_labels_created})")
