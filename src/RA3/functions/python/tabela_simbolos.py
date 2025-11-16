#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1

"""
Tabela de Símbolos para o Analisador Semântico RPN

Este módulo implementa a tabela de símbolos que rastreia todas as variáveis
(memórias) declaradas no programa, seus tipos, estado de inicialização e escopo.

Funcionalidades:
    - Adicionar novos símbolos com tipo e escopo
    - Buscar símbolos existentes
    - Atualizar estado de inicialização
    - Verificar se variável foi inicializada antes do uso
    - Gerenciamento de escopos (cada arquivo = escopo independente)
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
from src.RA3.functions.python import tipos


# ============================================================================
# ESTRUTURA DE DADOS PARA SÍMBOLOS
# ============================================================================

@dataclass
class SimboloInfo:
    """
    Informações sobre um símbolo (variável/memória) na tabela.

    Attributes:
        nome: Nome da variável (ex: 'VAR', 'CONTADOR', 'PI')
        tipo: Tipo do valor armazenado ('int' ou 'real')
        inicializada: True se a variável foi inicializada (teve valor atribuído)
        escopo: Nível de escopo (0 = global/arquivo)
        linha_declaracao: Linha onde a variável foi declarada/inicializada
        linha_ultimo_uso: Última linha onde a variável foi usada

    Examples:
        >>> simbolo = SimboloInfo(
        ...     nome='CONTADOR',
        ...     tipo='int',
        ...     inicializada=True,
        ...     escopo=0,
        ...     linha_declaracao=5
        ... )
        >>> simbolo.nome
        'CONTADOR'
    """
    nome: str
    tipo: str
    inicializada: bool = False
    escopo: int = 0
    linha_declaracao: Optional[int] = None
    linha_ultimo_uso: Optional[int] = None

    def __post_init__(self):
        """Validação após inicialização."""
        # Validar tipo
        if self.tipo not in tipos.TIPOS_NUMERICOS:
            raise ValueError(
                f"Tipo inválido para armazenamento: '{self.tipo}'. "
                f"Apenas {tipos.TIPOS_NUMERICOS} podem ser armazenados em memória."
            )

        # Nome deve ser uppercase (convenção da linguagem)
        if not self.nome.isupper():
            raise ValueError(
                f"Nome de variável deve ser uppercase: '{self.nome}'"
            )

    def __str__(self) -> str:
        """Representação legível do símbolo."""
        status = "inicializada" if self.inicializada else "NÃO inicializada"
        return (
            f"{self.nome}: {tipos.descricao_tipo(self.tipo)} "
            f"({status}, escopo={self.escopo})"
        )


# ============================================================================
# TABELA DE SÍMBOLOS
# ============================================================================

class TabelaSimbolos:
    """
    Gerencia todos os símbolos (variáveis/memórias) do programa.

    A tabela rastreia:
        - Todas as variáveis declaradas
        - Seus tipos (int ou real)
        - Estado de inicialização
        - Escopo (cada arquivo = escopo independente)

    Regras Importantes:
        - Variáveis devem ser inicializadas antes do uso (V MEM)
        - Usar variável não inicializada (MEM) = erro semântico
        - Cada arquivo tem seu próprio escopo (isolamento)
        - Apenas int e real podem ser armazenados (boolean proibido)

    Examples:
        >>> tabela = TabelaSimbolos()
        >>> _ = tabela.adicionarSimbolo('CONTADOR', 'int', inicializada=True, linha=5)
        >>> info = tabela.buscarSimbolo('CONTADOR')
        >>> print(info.tipo)
        int
        >>> tabela.verificar_inicializacao('CONTADOR')
        True
    """

    def __init__(self, escopo_inicial: int = 0):
        """
        Inicializa uma nova tabela de símbolos.

        Args:
            escopo_inicial: Nível de escopo inicial (padrão: 0 = global)
        """
        self._simbolos: Dict[str, SimboloInfo] = {}
        self._escopo_atual: int = escopo_inicial
        self._contador_acessos: Dict[str, int] = {}  # Para estatísticas

    @property
    def escopo_atual(self) -> int:
        """Retorna o nível de escopo atual."""
        return self._escopo_atual

    @property
    def simbolos(self) -> Dict[str, SimboloInfo]:
        """Retorna cópia do dicionário de símbolos (read-only)."""
        return self._simbolos.copy()

    def adicionarSimbolo(
        self,
        nome: str,
        tipo: str,
        inicializada: bool = False,
        linha: Optional[int] = None
    ) -> SimboloInfo:
        """
        Adiciona um novo símbolo à tabela ou atualiza existente.

        Se o símbolo já existe:
            - Atualiza o tipo (permite redeclaração)
            - Atualiza estado de inicialização
            - Mantém escopo original

        Args:
            nome: Nome da variável (deve ser uppercase)
            tipo: Tipo do valor ('int' ou 'real')
            inicializada: True se está sendo inicializada agora
            linha: Número da linha onde ocorreu a declaração

        Returns:
            SimboloInfo do símbolo adicionado/atualizado

        Raises:
            ValueError: Se tipo inválido ou nome não uppercase

        Examples:
            >>> tabela = TabelaSimbolos()
            >>> simbolo = tabela.adicionarSimbolo('VAR', 'int', True, 10)
            >>> simbolo.inicializada
            True
            >>> _ = tabela.adicionarSimbolo('VAR', 'real', True, 15)
            >>> simbolo_novo = tabela.buscarSimbolo('VAR')
            >>> simbolo_novo.tipo
            'real'
        """
        nome = nome.upper()  # Garantir uppercase

        # Validar tipo de armazenamento
        if not tipos.tipo_compativel_armazenamento(tipo):
            raise ValueError(
                f"Tipo '{tipo}' não pode ser armazenado em memória. "
                f"Apenas {tipos.TIPOS_NUMERICOS} são permitidos."
            )

        # Se já existe, atualizar
        if nome in self._simbolos:
            simbolo_existente = self._simbolos[nome]
            simbolo_existente.tipo = tipo
            if inicializada:
                simbolo_existente.inicializada = True
                if linha is not None:
                    simbolo_existente.linha_declaracao = linha
            return simbolo_existente

        # Criar novo símbolo
        simbolo = SimboloInfo(
            nome=nome,
            tipo=tipo,
            inicializada=inicializada,
            escopo=self._escopo_atual,
            linha_declaracao=linha
        )
        
        self._simbolos[nome] = simbolo
        self._contador_acessos[nome] = 0

        return simbolo

    def buscarSimbolo(self, nome: str) -> Optional[SimboloInfo]:
        """
        Busca um símbolo na tabela.

        Args:
            nome: Nome da variável (case-insensitive)

        Returns:
            SimboloInfo se encontrado, None caso contrário

        Examples:
            >>> tabela = TabelaSimbolos()
            >>> _ = tabela.adicionarSimbolo('VAR', 'int')
            >>> info = tabela.buscarSimbolo('VAR')
            >>> info.nome
            'VAR'
            >>> tabela.buscarSimbolo('INEXISTENTE') is None
            True
        """
        nome = nome.upper()
        return self._simbolos.get(nome)

    def existe(self, nome: str) -> bool:
        """
        Verifica se um símbolo existe na tabela.

        Args:
            nome: Nome da variável (case-insensitive)

        Returns:
            True se existe, False caso contrário

        Examples:
            >>> tabela = TabelaSimbolos()
            >>> _ = tabela.adicionarSimbolo('VAR', 'int')
            >>> tabela.existe('VAR')
            True
            >>> tabela.existe('INEXISTENTE')
            False
        """
        return nome.upper() in self._simbolos

    def marcar_inicializada(self, nome: str, linha: Optional[int] = None) -> bool:
        """
        Marca um símbolo como inicializado.

        Args:
            nome: Nome da variável
            linha: Linha onde foi inicializada

        Returns:
            True se marcado com sucesso, False se não encontrado

        Examples:
            >>> tabela = TabelaSimbolos()
            >>> _ = tabela.adicionarSimbolo('VAR', 'int', False)
            >>> tabela.marcar_inicializada('VAR', 10)
            True
            >>> tabela.verificar_inicializacao('VAR')
            True
        """
        simbolo = self.buscarSimbolo(nome)
        if simbolo is None:
            return False

        simbolo.inicializada = True
        if linha is not None:
            simbolo.linha_declaracao = linha

        return True

    def verificar_inicializacao(self, nome: str) -> bool:
        """
        Verifica se um símbolo foi inicializado.

        Regra Crítica: Usar (MEM) antes de (V MEM) = erro semântico

        Args:
            nome: Nome da variável

        Returns:
            True se inicializada, False se não existe ou não inicializada

        Examples:
            >>> tabela = TabelaSimbolos()
            >>> _ = tabela.adicionarSimbolo('VAR', 'int', True)
            >>> tabela.verificar_inicializacao('VAR')
            True
            >>> _ = tabela.adicionarSimbolo('UNINIT', 'int', False)
            >>> tabela.verificar_inicializacao('UNINIT')
            False
        """
        simbolo = self.buscarSimbolo(nome)
        if simbolo is None:
            return False
        return simbolo.inicializada

    def obter_tipo(self, nome: str) -> Optional[str]:
        """
        Obtém o tipo de um símbolo.

        Args:
            nome: Nome da variável

        Returns:
            Tipo da variável ('int' ou 'real'), ou None se não encontrada

        Examples:
            >>> tabela = TabelaSimbolos()
            >>> _ = tabela.adicionarSimbolo('VAR', 'real')
            >>> tabela.obter_tipo('VAR')
            'real'
            >>> tabela.obter_tipo('INEXISTENTE') is None
            True
        """
        simbolo = self.buscarSimbolo(nome)
        if simbolo is None:
            return None
        return simbolo.tipo

    def registrar_uso(self, nome: str, linha: Optional[int] = None) -> bool:
        """
        Registra o uso de uma variável (para estatísticas e rastreamento).

        Args:
            nome: Nome da variável
            linha: Linha onde foi usada

        Returns:
            True se registrado com sucesso, False se não encontrada

        Examples:
            >>> tabela = TabelaSimbolos()
            >>> _ = tabela.adicionarSimbolo('VAR', 'int')
            >>> tabela.registrar_uso('VAR', 20)
            True
        """
        simbolo = self.buscarSimbolo(nome)
        if simbolo is None:
            return False

        self._contador_acessos[nome.upper()] = \
            self._contador_acessos.get(nome.upper(), 0) + 1

        if linha is not None:
            simbolo.linha_ultimo_uso = linha

        return True

    def obter_numero_usos(self, nome: str) -> int:
        """
        Retorna quantas vezes uma variável foi usada.

        Args:
            nome: Nome da variável

        Returns:
            Número de usos (0 se não encontrada)

        Examples:
            >>> tabela = TabelaSimbolos()
            >>> _ = tabela.adicionarSimbolo('VAR', 'int')
            >>> tabela.registrar_uso('VAR')
            True
            >>> tabela.registrar_uso('VAR')
            True
            >>> tabela.obter_numero_usos('VAR')
            2
        """
        return self._contador_acessos.get(nome.upper(), 0)

    def limpar(self):
        """
        Limpa toda a tabela de símbolos.

        Útil ao processar novo arquivo (novo escopo independente).

        Examples:
            >>> tabela = TabelaSimbolos()
            >>> _ = tabela.adicionarSimbolo('VAR', 'int')
            >>> len(tabela.simbolos) > 0
            True
            >>> tabela.limpar()
            >>> len(tabela.simbolos)
            0
        """
        self._simbolos.clear()
        self._contador_acessos.clear()

    def listar_simbolos(self, apenas_inicializadas: bool = False) -> list[SimboloInfo]:
        """
        Lista todos os símbolos da tabela.

        Args:
            apenas_inicializadas: Se True, lista apenas variáveis inicializadas

        Returns:
            Lista de SimboloInfo

        Examples:
            >>> tabela = TabelaSimbolos()
            >>> _ = tabela.adicionarSimbolo('A', 'int', True)
            >>> _ = tabela.adicionarSimbolo('B', 'int', False)
            >>> len(tabela.listar_simbolos())
            2
            >>> len(tabela.listar_simbolos(apenas_inicializadas=True))
            1
        """
        simbolos = list(self._simbolos.values())

        if apenas_inicializadas:
            simbolos = [s for s in simbolos if s.inicializada]

        # Ordenar por nome
        simbolos.sort(key=lambda s: s.nome)

        return simbolos

    def gerar_relatorio(self) -> str:
        """
        Gera relatório textual da tabela de símbolos.

        Returns:
            String formatada com informações de todas as variáveis

        Examples:
            >>> tabela = TabelaSimbolos()
            >>> _ = tabela.adicionarSimbolo('VAR', 'int', True, 5)
            >>> print(tabela.gerar_relatorio())  # doctest: +ELLIPSIS
            ==================...
        """
        linhas = []
        linhas.append("=" * 70)
        linhas.append("TABELA DE SÍMBOLOS")
        linhas.append("=" * 70)
        linhas.append(f"Escopo atual: {self._escopo_atual}")
        linhas.append(f"Total de símbolos: {len(self._simbolos)}")
        linhas.append("-" * 70)

        if not self._simbolos:
            linhas.append("(vazia)")
        else:
            # Cabeçalho
            linhas.append(
                f"{'Nome':<15} {'Tipo':<10} {'Inicializada':<15} "
                f"{'Linha Decl.':<12} {'Usos':<6}"
            )
            linhas.append("-" * 70)

            # Símbolos
            for simbolo in sorted(self._simbolos.values(), key=lambda s: s.nome):
                status = "SIM" if simbolo.inicializada else "NÃO"
                linha_decl = str(simbolo.linha_declaracao) \
                    if simbolo.linha_declaracao else "-"
                usos = self._contador_acessos.get(simbolo.nome, 0)

                linhas.append(
                    f"{simbolo.nome:<15} {simbolo.tipo:<10} {status:<15} "
                    f"{linha_decl:<12} {usos:<6}"
                )

        linhas.append("=" * 70)
        return "\n".join(linhas)

    def __str__(self) -> str:
        """Representação string da tabela."""
        return self.gerar_relatorio()

    def __len__(self) -> int:
        """Número de símbolos na tabela."""
        return len(self._simbolos)

    def __contains__(self, nome: str) -> bool:
        """Permite usar 'in' operator."""
        return self.existe(nome)


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def inicializarTabelaSimbolos() -> TabelaSimbolos:
    """
    Cria e retorna uma nova tabela de símbolos vazia.

    Returns:
        Nova instância de TabelaSimbolos

    Examples:
        >>> tabela = inicializarTabelaSimbolos()
        >>> len(tabela)
        0
    """
    return TabelaSimbolos()


if __name__ == '__main__':
    # Testes básicos
    import doctest
    doctest.testmod()

    # Demonstração
    print("✅ Módulo tabela_simbolos.py carregado com sucesso!\n")

    # Criar tabela de exemplo
    tabela = TabelaSimbolos()

    # Adicionar alguns símbolos
    tabela.adicionarSimbolo('CONTADOR', tipos.TYPE_INT, inicializada=True, linha=5)
    tabela.adicionarSimbolo('PI', tipos.TYPE_REAL, inicializada=True, linha=10)
    tabela.adicionarSimbolo('TEMP', tipos.TYPE_INT, inicializada=False, linha=15)

    # Registrar usos
    tabela.registrar_uso('CONTADOR', 20)
    tabela.registrar_uso('CONTADOR', 25)
    tabela.registrar_uso('PI', 30)

    # Exibir relatório
    print(tabela.gerar_relatorio())
