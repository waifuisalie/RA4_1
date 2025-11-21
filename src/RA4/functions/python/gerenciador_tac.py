"""
Gerenciador TAC - Variáveis temporárias e rótulos.
"""

from typing import Dict, Any


class GerenciadorTAC:
    """Gerencia variáveis temporárias (t0, t1...) e rótulos (L0, L1...)."""

    def __init__(self):
        self._contador_temp = 0
        self._contador_rotulo = 0
        self._total_temps_criados = 0
        self._total_rotulos_criados = 0

    def nova_temp(self) -> str:
        """Gera nova variável temporária (t0, t1, t2...)."""
        nome_temp = f"t{self._contador_temp}"
        self._contador_temp += 1
        self._total_temps_criados += 1
        return nome_temp

    def novo_rotulo(self) -> str:
        """Gera novo rótulo (L0, L1, L2...)."""
        nome_rotulo = f"L{self._contador_rotulo}"
        self._contador_rotulo += 1
        self._total_rotulos_criados += 1
        return nome_rotulo

    def resetar_contadores(self) -> None:
        """Reseta contadores para novo programa (mantém estatísticas totais)."""
        self._contador_temp = 0
        self._contador_rotulo = 0

    def obter_contador_temp(self) -> int:
        """Retorna contador atual de temporários."""
        return self._contador_temp

    def obter_contador_rotulo(self) -> int:
        """Retorna contador atual de rótulos."""
        return self._contador_rotulo

    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso."""
        return {
            "contador_temp_atual": self._contador_temp,
            "contador_rotulo_atual": self._contador_rotulo,
            "total_temps_criados": self._total_temps_criados,
            "total_rotulos_criados": self._total_rotulos_criados
        }

    def __repr__(self) -> str:
        return (f"GerenciadorTAC(contador_temp={self._contador_temp}, "
                f"contador_rotulo={self._contador_rotulo}, "
                f"total_temps={self._total_temps_criados}, "
                f"total_rotulos={self._total_rotulos_criados})")
