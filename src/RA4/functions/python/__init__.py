"""
RA4 - Fase 4: Geração de Código TAC
"""

from .instrucoes_tac import (
    InstrucaoTAC,
    TACAtribuicao,
    TACCopia,
    TACOperacaoBinaria,
    TACOperacaoUnaria,
    TACRotulo,
    TACDesvio,
    TACSeDesvio,
    TACSeNaoDesvio,
    TACLeituraMemoria,
    TACEscritaMemoria,
    TACChamada,
    TACRetorno,
    instrucao_de_dicionario,
)

from .gerenciador_tac import GerenciadorTAC
from .percorredor_ast import PercorredorAST

from .saida_tac import (
    para_json,
    para_texto,
    salvar_json,
    salvar_texto,
    salvar_saida_tac,
)

from .gerador_tac import (
    gerarTAC,
    gerarTAC_de_dicionario,
    obter_tac_como_texto,
    obter_tac_com_linhas,
)

__all__ = [
    # Classe base
    "InstrucaoTAC",
    # Instruções
    "TACAtribuicao",
    "TACCopia",
    "TACOperacaoBinaria",
    "TACOperacaoUnaria",
    "TACRotulo",
    "TACDesvio",
    "TACSeDesvio",
    "TACSeNaoDesvio",
    "TACLeituraMemoria",
    "TACEscritaMemoria",
    "TACChamada",
    "TACRetorno",
    "instrucao_de_dicionario",
    # Gerenciadores
    "GerenciadorTAC",
    "PercorredorAST",
    # Saída
    "para_json",
    "para_texto",
    "salvar_json",
    "salvar_texto",
    "salvar_saida_tac",
    # Funções principais
    "gerarTAC",
    "gerarTAC_de_dicionario",
    "obter_tac_como_texto",
    "obter_tac_com_linhas",
]
