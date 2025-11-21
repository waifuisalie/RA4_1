"""
TAC (Three Address Code) Instruction Classes

This module defines all TAC instruction types for the Phase 4 compiler.
Each instruction represents an intermediate code operation with at most 3 operands.

Author: Phase 4 - Code Generation Team
Project: RA4_Compiladores - Compiler for RPN Language targeting AVR Assembly
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod


class TACInstruction(ABC):
    """
    Abstract base class for all TAC instructions.

    All TAC instructions must implement:
    - to_string(): Human-readable TAC format for .md files
    - to_dict(): JSON-serializable format for .json files
    - defines_variable: Property returning variable defined (LHS), or None
    - uses_variables: Property returning list of variables used (RHS)
    """

    @abstractmethod
    def to_string(self) -> str:
        """Return human-readable TAC representation (for TAC.md)"""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Return JSON-serializable representation (for TAC.json)"""
        pass

    @property
    @abstractmethod
    def defines_variable(self) -> Optional[str]:
        """Return the variable defined by this instruction (LHS), or None"""
        pass

    @property
    @abstractmethod
    def uses_variables(self) -> List[str]:
        """Return list of variables used by this instruction (RHS)"""
        pass

    @staticmethod
    def is_constant(operand: str) -> bool:
        """
        Check if an operand is a constant literal (number).

        Args:
            operand: String operand to check

        Returns:
            True if operand is a numeric constant, False if it's a variable
        """
        try:
            float(operand)
            return True
        except ValueError:
            return False


# ============================================================================
# ASSIGNMENT INSTRUCTIONS
# ============================================================================

@dataclass
class TACAssignment(TACInstruction):
    """
    Simple assignment: dest = source
    Example: t0 = 5
             t1 = X
    """
    dest: str
    source: str
    line: int
    data_type: Optional[str] = None

    def to_string(self) -> str:
        return f"{self.dest} = {self.source}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "assignment",
            "dest": self.dest,
            "source": self.source,
            "line": self.line,
            "data_type": self.data_type
        }

    @property
    def defines_variable(self) -> Optional[str]:
        return self.dest

    @property
    def uses_variables(self) -> List[str]:
        # Only include source if it's a variable, not a constant
        if not self.is_constant(self.source):
            return [self.source]
        return []


@dataclass
class TACCopy(TACInstruction):
    """
    Copy operation: dest = source
    Example: a = b

    Note: Similar to TACAssignment but semantically represents
    copying a variable value (not assignment of literal/expression result)
    """
    dest: str
    source: str
    line: int
    data_type: Optional[str] = None

    def to_string(self) -> str:
        return f"{self.dest} = {self.source}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "copy",
            "dest": self.dest,
            "source": self.source,
            "line": self.line,
            "data_type": self.data_type
        }

    @property
    def defines_variable(self) -> Optional[str]:
        return self.dest

    @property
    def uses_variables(self) -> List[str]:
        if not self.is_constant(self.source):
            return [self.source]
        return []


# ============================================================================
# OPERATION INSTRUCTIONS
# ============================================================================

@dataclass
class TACBinaryOp(TACInstruction):
    """
    Binary operation: result = operand1 operator operand2

    Supported operators:
    - Arithmetic: +, -, *, /, | (real division), % (modulo), ^ (power)
    - Comparison: >, <, >=, <=, ==, !=
    - Logical: &&, ||

    Example: t2 = t0 + t1
             t3 = X > 5
    """
    result: str
    operand1: str
    operator: str
    operand2: str
    line: int
    data_type: Optional[str] = None

    def to_string(self) -> str:
        return f"{self.result} = {self.operand1} {self.operator} {self.operand2}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "binary_op",
            "result": self.result,
            "operand1": self.operand1,
            "operator": self.operator,
            "operand2": self.operand2,
            "line": self.line,
            "data_type": self.data_type
        }

    @property
    def defines_variable(self) -> Optional[str]:
        return self.result

    @property
    def uses_variables(self) -> List[str]:
        uses = []
        if not self.is_constant(self.operand1):
            uses.append(self.operand1)
        if not self.is_constant(self.operand2):
            uses.append(self.operand2)
        return uses


@dataclass
class TACUnaryOp(TACInstruction):
    """
    Unary operation: result = operator operand

    Supported operators:
    - Negation: - (arithmetic negation)
    - Logical NOT: ! (boolean negation)

    Example: t1 = -a
             t2 = !condition
    """
    result: str
    operator: str
    operand: str
    line: int
    data_type: Optional[str] = None

    def to_string(self) -> str:
        return f"{self.result} = {self.operator}{self.operand}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "unary_op",
            "result": self.result,
            "operator": self.operator,
            "operand": self.operand,
            "line": self.line,
            "data_type": self.data_type
        }

    @property
    def defines_variable(self) -> Optional[str]:
        return self.result

    @property
    def uses_variables(self) -> List[str]:
        if not self.is_constant(self.operand):
            return [self.operand]
        return []


# ============================================================================
# CONTROL FLOW INSTRUCTIONS
# ============================================================================

@dataclass
class TACLabel(TACInstruction):
    """
    Label declaration: name:

    Used as target for jump instructions.
    Convention: L0, L1, L2, ...

    Example: L1:
    """
    name: str
    line: int

    def to_string(self) -> str:
        return f"{self.name}:"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "label",
            "name": self.name,
            "line": self.line
        }

    @property
    def defines_variable(self) -> Optional[str]:
        return None  # Labels don't define variables

    @property
    def uses_variables(self) -> List[str]:
        return []  # Labels don't use variables


@dataclass
class TACGoto(TACInstruction):
    """
    Unconditional jump: goto target

    Example: goto L1
    """
    target: str
    line: int

    def to_string(self) -> str:
        return f"goto {self.target}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "goto",
            "target": self.target,
            "line": self.line
        }

    @property
    def defines_variable(self) -> Optional[str]:
        return None

    @property
    def uses_variables(self) -> List[str]:
        return []  # Target label is not a variable


@dataclass
class TACIfGoto(TACInstruction):
    """
    Conditional jump (jump if true): if condition goto target

    Jumps to target if condition evaluates to true (non-zero).

    Example: if t5 goto L1
    """
    condition: str
    target: str
    line: int

    def to_string(self) -> str:
        return f"if {self.condition} goto {self.target}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "if_goto",
            "condition": self.condition,
            "target": self.target,
            "line": self.line
        }

    @property
    def defines_variable(self) -> Optional[str]:
        return None

    @property
    def uses_variables(self) -> List[str]:
        if not self.is_constant(self.condition):
            return [self.condition]
        return []


@dataclass
class TACIfFalseGoto(TACInstruction):
    """
    Conditional jump (jump if false): ifFalse condition goto target

    Jumps to target if condition evaluates to false (zero).

    Example: ifFalse t5 goto L2
    """
    condition: str
    target: str
    line: int

    def to_string(self) -> str:
        return f"ifFalse {self.condition} goto {self.target}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "if_false_goto",
            "condition": self.condition,
            "target": self.target,
            "line": self.line
        }

    @property
    def defines_variable(self) -> Optional[str]:
        return None

    @property
    def uses_variables(self) -> List[str]:
        if not self.is_constant(self.condition):
            return [self.condition]
        return []


# ============================================================================
# MEMORY ACCESS INSTRUCTIONS
# ============================================================================

@dataclass
class TACMemoryRead(TACInstruction):
    """
    Memory read: result = MEM[address]

    Reads value from memory location 'address' into 'result'.
    Used for implementing the MEM command in RPN language.

    Example: t4 = MEM[X]
    """
    result: str
    address: str
    line: int
    data_type: Optional[str] = None

    def to_string(self) -> str:
        return f"{self.result} = MEM[{self.address}]"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "memory_read",
            "result": self.result,
            "address": self.address,
            "line": self.line,
            "data_type": self.data_type
        }

    @property
    def defines_variable(self) -> Optional[str]:
        return self.result

    @property
    def uses_variables(self) -> List[str]:
        # Address can be a variable name or constant
        if not self.is_constant(self.address):
            return [self.address]
        return []


@dataclass
class TACMemoryWrite(TACInstruction):
    """
    Memory write: MEM[address] = value

    Writes 'value' to memory location 'address'.
    Used for implementing the (V MEM) command in RPN language.

    Example: MEM[X] = t5
    """
    address: str
    value: str
    line: int
    data_type: Optional[str] = None

    def to_string(self) -> str:
        return f"MEM[{self.address}] = {self.value}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "memory_write",
            "address": self.address,
            "value": self.value,
            "line": self.line,
            "data_type": self.data_type
        }

    @property
    def defines_variable(self) -> Optional[str]:
        # Memory write defines the memory location
        return self.address

    @property
    def uses_variables(self) -> List[str]:
        if not self.is_constant(self.value):
            return [self.value]
        return []


# ============================================================================
# FUNCTION/PROCEDURE INSTRUCTIONS
# ============================================================================

@dataclass
class TACCall(TACInstruction):
    """
    Function call: result = call function_name, num_params

    Calls function with specified number of parameters.
    Parameters are assumed to be pushed onto stack/registers before call.

    Example: t1 = call factorial, 1
    """
    result: str
    function_name: str
    num_params: int
    line: int
    data_type: Optional[str] = None

    def to_string(self) -> str:
        return f"{self.result} = call {self.function_name}, {self.num_params}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "call",
            "result": self.result,
            "function_name": self.function_name,
            "num_params": self.num_params,
            "line": self.line,
            "data_type": self.data_type
        }

    @property
    def defines_variable(self) -> Optional[str]:
        return self.result

    @property
    def uses_variables(self) -> List[str]:
        # Function calls may use parameters, but those are tracked separately
        # in parameter passing instructions (not shown here)
        return []


@dataclass
class TACReturn(TACInstruction):
    """
    Return statement: return value

    Returns from current function with specified value.

    Example: return t10
             return 42
    """
    value: str
    line: int
    data_type: Optional[str] = None

    def to_string(self) -> str:
        return f"return {self.value}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "return",
            "value": self.value,
            "line": self.line,
            "data_type": self.data_type
        }

    @property
    def defines_variable(self) -> Optional[str]:
        return None  # Return doesn't define a variable

    @property
    def uses_variables(self) -> List[str]:
        if not self.is_constant(self.value):
            return [self.value]
        return []


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def instruction_from_dict(data: Dict[str, Any]) -> TACInstruction:
    """
    Factory function to create TAC instruction from dictionary.

    Useful for deserializing TAC instructions from JSON files.

    Args:
        data: Dictionary with instruction data (must have 'type' key)

    Returns:
        Appropriate TACInstruction subclass instance

    Raises:
        ValueError: If instruction type is unknown
    """
    instr_type = data.get("type")

    if instr_type == "assignment":
        return TACAssignment(
            dest=data["dest"],
            source=data["source"],
            line=data["line"],
            data_type=data.get("data_type")
        )
    elif instr_type == "copy":
        return TACCopy(
            dest=data["dest"],
            source=data["source"],
            line=data["line"],
            data_type=data.get("data_type")
        )
    elif instr_type == "binary_op":
        return TACBinaryOp(
            result=data["result"],
            operand1=data["operand1"],
            operator=data["operator"],
            operand2=data["operand2"],
            line=data["line"],
            data_type=data.get("data_type")
        )
    elif instr_type == "unary_op":
        return TACUnaryOp(
            result=data["result"],
            operator=data["operator"],
            operand=data["operand"],
            line=data["line"],
            data_type=data.get("data_type")
        )
    elif instr_type == "label":
        return TACLabel(
            name=data["name"],
            line=data["line"]
        )
    elif instr_type == "goto":
        return TACGoto(
            target=data["target"],
            line=data["line"]
        )
    elif instr_type == "if_goto":
        return TACIfGoto(
            condition=data["condition"],
            target=data["target"],
            line=data["line"]
        )
    elif instr_type == "if_false_goto":
        return TACIfFalseGoto(
            condition=data["condition"],
            target=data["target"],
            line=data["line"]
        )
    elif instr_type == "memory_read":
        return TACMemoryRead(
            result=data["result"],
            address=data["address"],
            line=data["line"],
            data_type=data.get("data_type")
        )
    elif instr_type == "memory_write":
        return TACMemoryWrite(
            address=data["address"],
            value=data["value"],
            line=data["line"],
            data_type=data.get("data_type")
        )
    elif instr_type == "call":
        return TACCall(
            result=data["result"],
            function_name=data["function_name"],
            num_params=data["num_params"],
            line=data["line"],
            data_type=data.get("data_type")
        )
    elif instr_type == "return":
        return TACReturn(
            value=data["value"],
            line=data["line"],
            data_type=data.get("data_type")
        )
    else:
        raise ValueError(f"Unknown TAC instruction type: {instr_type}")
