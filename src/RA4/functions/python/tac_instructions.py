# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA4_1

"""
Classes de Instruções TAC (Three Address Code)

Define todos os tipos de instrução TAC para o compilador da Fase 4.
Cada instrução representa uma operação de código intermediário com no máximo 3 operandos.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod


#########################
# CLASSE BASE ABSTRATA
#########################

class TACInstruction(ABC):
    """Classe base abstrata para todas as instruções TAC."""

    @abstractmethod
    def to_string(self) -> str:
        """Retorna representação TAC legível."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Retorna representação serializável em JSON."""
        pass

    @property
    @abstractmethod
    def defines_variable(self) -> Optional[str]:
        """Retorna variável definida pela instrução (LHS), ou None."""
        pass

    @property
    @abstractmethod
    def uses_variables(self) -> List[str]:
        """Retorna lista de variáveis usadas pela instrução (RHS)."""
        pass

    @staticmethod
    def is_constant(operand: str) -> bool:
        """Verifica se operando é constante numérica."""
        try:
            float(operand)
            return True
        except ValueError:
            return False


#########################
# INSTRUÇÕES DE ATRIBUIÇÃO
#########################

@dataclass
class TACAssignment(TACInstruction):
    """Atribuição simples: dest = source. Ex: t0 = 5"""
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
        if not self.is_constant(self.source):
            return [self.source]
        return []


@dataclass
class TACCopy(TACInstruction):
    """Cópia de variável: dest = source. Ex: a = b"""
    dest: str
    source: str
    line: int
    data_type: Optional[str] = None

    def to_string(self) -> str:
        # Validação rigorosa para evitar TAC inválido
        invalid_chars = ['(', ')', '[', ']', '{', '}', ';', ':', '.', ',']
        if (not self.dest or not self.source or
            any(char in self.dest for char in invalid_chars) or
            any(char in self.source for char in invalid_chars) or
            not self.dest.strip() or not self.source.strip()):
            return f"// Invalid TACCopy: {self.dest} = {self.source}"
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


#########################
# INSTRUÇÕES DE OPERAÇÃO
#########################

@dataclass
class TACBinaryOp(TACInstruction):
    """Operação binária: result = op1 operador op2. Operadores: +,-,*,/,|,%,^,>,<,>=,<=,==,!=,&&,||"""
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
    """Operação unária: result = operador operando. Operadores: - (negação), ! (NOT)"""
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


#########################
# INSTRUÇÕES DE CONTROLE DE FLUXO
#########################

@dataclass
class TACLabel(TACInstruction):
    """Declaração de label: name: Convenção: L0, L1, L2, ..."""
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
        return None

    @property
    def uses_variables(self) -> List[str]:
        return []


@dataclass
class TACGoto(TACInstruction):
    """Salto incondicional: goto target"""
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
        return []


@dataclass
class TACIfGoto(TACInstruction):
    """Salto condicional (se verdadeiro): if condição goto target"""
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
    """Salto condicional (se falso): ifFalse condição goto target"""
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


#########################
# INSTRUÇÕES DE ACESSO À MEMÓRIA
#########################

@dataclass
class TACMemoryRead(TACInstruction):
    """Leitura de memória: result = MEM[address]"""
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
        if not self.is_constant(self.address):
            return [self.address]
        return []


@dataclass
class TACMemoryWrite(TACInstruction):
    """Escrita em memória: MEM[address] = value"""
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
        return self.address

    @property
    def uses_variables(self) -> List[str]:
        if not self.is_constant(self.value):
            return [self.value]
        return []


#########################
# INSTRUÇÕES DE FUNÇÃO
#########################

@dataclass
class TACCall(TACInstruction):
    """Chamada de função: result = call nome_função, num_params"""
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
        return []


@dataclass
class TACReturn(TACInstruction):
    """Retorno de função: return valor"""
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
        return None

    @property
    def uses_variables(self) -> List[str]:
        if not self.is_constant(self.value):
            return [self.value]
        return []


#########################
# FUNÇÕES UTILITÁRIAS
#########################

def instruction_from_dict(data: Dict[str, Any]) -> TACInstruction:
    """Cria instrução TAC a partir de dicionário (deserialização JSON)."""
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
        raise ValueError(f"Tipo de instrução TAC desconhecido: {instr_type}")
