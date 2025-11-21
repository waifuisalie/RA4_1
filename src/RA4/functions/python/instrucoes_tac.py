"""
Instruções TAC - Classes para código de três endereços.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod


class InstrucaoTAC(ABC):
    """Classe base para instruções TAC."""

    @abstractmethod
    def para_string(self) -> str:
        """Retorna representação textual."""
        pass

    @abstractmethod
    def para_dicionario(self) -> Dict[str, Any]:
        """Retorna dicionário para JSON."""
        pass

    @property
    @abstractmethod
    def define_variavel(self) -> Optional[str]:
        """Variável definida (lado esquerdo)."""
        pass

    @property
    @abstractmethod
    def usa_variaveis(self) -> List[str]:
        """Variáveis usadas (lado direito)."""
        pass

    @staticmethod
    def eh_constante(operando: str) -> bool:
        """Verifica se operando é número."""
        try:
            float(operando)
            return True
        except ValueError:
            return False


# --- ATRIBUIÇÃO ---

@dataclass
class TACAtribuicao(InstrucaoTAC):
    """Atribuição simples: destino = origem"""
    destino: str
    origem: str
    linha: int
    tipo_dado: Optional[str] = None

    def para_string(self) -> str:
        return f"{self.destino} = {self.origem}"

    def para_dicionario(self) -> Dict[str, Any]:
        return {
            "tipo": "atribuicao",
            "destino": self.destino,
            "origem": self.origem,
            "linha": self.linha,
            "tipo_dado": self.tipo_dado
        }

    @property
    def define_variavel(self) -> Optional[str]:
        return self.destino

    @property
    def usa_variaveis(self) -> List[str]:
        if not self.eh_constante(self.origem):
            return [self.origem]
        return []


@dataclass
class TACCopia(InstrucaoTAC):
    """Cópia de variável: destino = origem"""
    destino: str
    origem: str
    linha: int
    tipo_dado: Optional[str] = None

    def para_string(self) -> str:
        return f"{self.destino} = {self.origem}"

    def para_dicionario(self) -> Dict[str, Any]:
        return {
            "tipo": "copia",
            "destino": self.destino,
            "origem": self.origem,
            "linha": self.linha,
            "tipo_dado": self.tipo_dado
        }

    @property
    def define_variavel(self) -> Optional[str]:
        return self.destino

    @property
    def usa_variaveis(self) -> List[str]:
        if not self.eh_constante(self.origem):
            return [self.origem]
        return []


# --- OPERAÇÕES ---

@dataclass
class TACOperacaoBinaria(InstrucaoTAC):
    """Operação binária: resultado = op1 operador op2"""
    resultado: str
    operando1: str
    operador: str
    operando2: str
    linha: int
    tipo_dado: Optional[str] = None

    def para_string(self) -> str:
        return f"{self.resultado} = {self.operando1} {self.operador} {self.operando2}"

    def para_dicionario(self) -> Dict[str, Any]:
        return {
            "tipo": "operacao_binaria",
            "resultado": self.resultado,
            "operando1": self.operando1,
            "operador": self.operador,
            "operando2": self.operando2,
            "linha": self.linha,
            "tipo_dado": self.tipo_dado
        }

    @property
    def define_variavel(self) -> Optional[str]:
        return self.resultado

    @property
    def usa_variaveis(self) -> List[str]:
        usa = []
        if not self.eh_constante(self.operando1):
            usa.append(self.operando1)
        if not self.eh_constante(self.operando2):
            usa.append(self.operando2)
        return usa


@dataclass
class TACOperacaoUnaria(InstrucaoTAC):
    """Operação unária: resultado = operador operando"""
    resultado: str
    operador: str
    operando: str
    linha: int
    tipo_dado: Optional[str] = None

    def para_string(self) -> str:
        return f"{self.resultado} = {self.operador}{self.operando}"

    def para_dicionario(self) -> Dict[str, Any]:
        return {
            "tipo": "operacao_unaria",
            "resultado": self.resultado,
            "operador": self.operador,
            "operando": self.operando,
            "linha": self.linha,
            "tipo_dado": self.tipo_dado
        }

    @property
    def define_variavel(self) -> Optional[str]:
        return self.resultado

    @property
    def usa_variaveis(self) -> List[str]:
        if not self.eh_constante(self.operando):
            return [self.operando]
        return []


# --- CONTROLE DE FLUXO ---

@dataclass
class TACRotulo(InstrucaoTAC):
    """Rótulo: nome:"""
    nome: str
    linha: int

    def para_string(self) -> str:
        return f"{self.nome}:"

    def para_dicionario(self) -> Dict[str, Any]:
        return {
            "tipo": "rotulo",
            "nome": self.nome,
            "linha": self.linha
        }

    @property
    def define_variavel(self) -> Optional[str]:
        return None

    @property
    def usa_variaveis(self) -> List[str]:
        return []


@dataclass
class TACDesvio(InstrucaoTAC):
    """Desvio incondicional: goto alvo"""
    alvo: str
    linha: int

    def para_string(self) -> str:
        return f"goto {self.alvo}"

    def para_dicionario(self) -> Dict[str, Any]:
        return {
            "tipo": "desvio",
            "alvo": self.alvo,
            "linha": self.linha
        }

    @property
    def define_variavel(self) -> Optional[str]:
        return None

    @property
    def usa_variaveis(self) -> List[str]:
        return []


@dataclass
class TACSeDesvio(InstrucaoTAC):
    """Desvio se verdadeiro: if condicao goto alvo"""
    condicao: str
    alvo: str
    linha: int

    def para_string(self) -> str:
        return f"if {self.condicao} goto {self.alvo}"

    def para_dicionario(self) -> Dict[str, Any]:
        return {
            "tipo": "se_desvio",
            "condicao": self.condicao,
            "alvo": self.alvo,
            "linha": self.linha
        }

    @property
    def define_variavel(self) -> Optional[str]:
        return None

    @property
    def usa_variaveis(self) -> List[str]:
        if not self.eh_constante(self.condicao):
            return [self.condicao]
        return []


@dataclass
class TACSeNaoDesvio(InstrucaoTAC):
    """Desvio se falso: ifFalse condicao goto alvo"""
    condicao: str
    alvo: str
    linha: int

    def para_string(self) -> str:
        return f"ifFalse {self.condicao} goto {self.alvo}"

    def para_dicionario(self) -> Dict[str, Any]:
        return {
            "tipo": "se_nao_desvio",
            "condicao": self.condicao,
            "alvo": self.alvo,
            "linha": self.linha
        }

    @property
    def define_variavel(self) -> Optional[str]:
        return None

    @property
    def usa_variaveis(self) -> List[str]:
        if not self.eh_constante(self.condicao):
            return [self.condicao]
        return []


# --- MEMÓRIA ---

@dataclass
class TACLeituraMemoria(InstrucaoTAC):
    """Leitura de memória: resultado = MEM[endereco]"""
    resultado: str
    endereco: str
    linha: int
    tipo_dado: Optional[str] = None

    def para_string(self) -> str:
        return f"{self.resultado} = MEM[{self.endereco}]"

    def para_dicionario(self) -> Dict[str, Any]:
        return {
            "tipo": "leitura_memoria",
            "resultado": self.resultado,
            "endereco": self.endereco,
            "linha": self.linha,
            "tipo_dado": self.tipo_dado
        }

    @property
    def define_variavel(self) -> Optional[str]:
        return self.resultado

    @property
    def usa_variaveis(self) -> List[str]:
        if not self.eh_constante(self.endereco):
            return [self.endereco]
        return []


@dataclass
class TACEscritaMemoria(InstrucaoTAC):
    """Escrita em memória: MEM[endereco] = valor"""
    endereco: str
    valor: str
    linha: int
    tipo_dado: Optional[str] = None

    def para_string(self) -> str:
        return f"MEM[{self.endereco}] = {self.valor}"

    def para_dicionario(self) -> Dict[str, Any]:
        return {
            "tipo": "escrita_memoria",
            "endereco": self.endereco,
            "valor": self.valor,
            "linha": self.linha,
            "tipo_dado": self.tipo_dado
        }

    @property
    def define_variavel(self) -> Optional[str]:
        return self.endereco

    @property
    def usa_variaveis(self) -> List[str]:
        if not self.eh_constante(self.valor):
            return [self.valor]
        return []


# --- FUNÇÕES ---

@dataclass
class TACChamada(InstrucaoTAC):
    """Chamada de função: resultado = call funcao, n_params"""
    resultado: str
    nome_funcao: str
    num_parametros: int
    linha: int
    tipo_dado: Optional[str] = None

    def para_string(self) -> str:
        return f"{self.resultado} = call {self.nome_funcao}, {self.num_parametros}"

    def para_dicionario(self) -> Dict[str, Any]:
        return {
            "tipo": "chamada",
            "resultado": self.resultado,
            "nome_funcao": self.nome_funcao,
            "num_parametros": self.num_parametros,
            "linha": self.linha,
            "tipo_dado": self.tipo_dado
        }

    @property
    def define_variavel(self) -> Optional[str]:
        return self.resultado

    @property
    def usa_variaveis(self) -> List[str]:
        return []


@dataclass
class TACRetorno(InstrucaoTAC):
    """Retorno de função: return valor"""
    valor: str
    linha: int
    tipo_dado: Optional[str] = None

    def para_string(self) -> str:
        return f"return {self.valor}"

    def para_dicionario(self) -> Dict[str, Any]:
        return {
            "tipo": "retorno",
            "valor": self.valor,
            "linha": self.linha,
            "tipo_dado": self.tipo_dado
        }

    @property
    def define_variavel(self) -> Optional[str]:
        return None

    @property
    def usa_variaveis(self) -> List[str]:
        if not self.eh_constante(self.valor):
            return [self.valor]
        return []


# --- UTILITÁRIOS ---

def instrucao_de_dicionario(dados: Dict[str, Any]) -> InstrucaoTAC:
    """Cria instrução TAC a partir de dicionário (desserialização JSON)."""
    tipo_instr = dados.get("tipo")

    if tipo_instr == "atribuicao":
        return TACAtribuicao(
            destino=dados["destino"],
            origem=dados["origem"],
            linha=dados["linha"],
            tipo_dado=dados.get("tipo_dado")
        )
    elif tipo_instr == "copia":
        return TACCopia(
            destino=dados["destino"],
            origem=dados["origem"],
            linha=dados["linha"],
            tipo_dado=dados.get("tipo_dado")
        )
    elif tipo_instr == "operacao_binaria":
        return TACOperacaoBinaria(
            resultado=dados["resultado"],
            operando1=dados["operando1"],
            operador=dados["operador"],
            operando2=dados["operando2"],
            linha=dados["linha"],
            tipo_dado=dados.get("tipo_dado")
        )
    elif tipo_instr == "operacao_unaria":
        return TACOperacaoUnaria(
            resultado=dados["resultado"],
            operador=dados["operador"],
            operando=dados["operando"],
            linha=dados["linha"],
            tipo_dado=dados.get("tipo_dado")
        )
    elif tipo_instr == "rotulo":
        return TACRotulo(
            nome=dados["nome"],
            linha=dados["linha"]
        )
    elif tipo_instr == "desvio":
        return TACDesvio(
            alvo=dados["alvo"],
            linha=dados["linha"]
        )
    elif tipo_instr == "se_desvio":
        return TACSeDesvio(
            condicao=dados["condicao"],
            alvo=dados["alvo"],
            linha=dados["linha"]
        )
    elif tipo_instr == "se_nao_desvio":
        return TACSeNaoDesvio(
            condicao=dados["condicao"],
            alvo=dados["alvo"],
            linha=dados["linha"]
        )
    elif tipo_instr == "leitura_memoria":
        return TACLeituraMemoria(
            resultado=dados["resultado"],
            endereco=dados["endereco"],
            linha=dados["linha"],
            tipo_dado=dados.get("tipo_dado")
        )
    elif tipo_instr == "escrita_memoria":
        return TACEscritaMemoria(
            endereco=dados["endereco"],
            valor=dados["valor"],
            linha=dados["linha"],
            tipo_dado=dados.get("tipo_dado")
        )
    elif tipo_instr == "chamada":
        return TACChamada(
            resultado=dados["resultado"],
            nome_funcao=dados["nome_funcao"],
            num_parametros=dados["num_parametros"],
            linha=dados["linha"],
            tipo_dado=dados.get("tipo_dado")
        )
    elif tipo_instr == "retorno":
        return TACRetorno(
            valor=dados["valor"],
            linha=dados["linha"],
            tipo_dado=dados.get("tipo_dado")
        )
    else:
        raise ValueError(f"Tipo de instrução TAC desconhecido: {tipo_instr}")
