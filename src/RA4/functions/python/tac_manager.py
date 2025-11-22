#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA4_1

from typing import Dict, Any

#########################
# CLASSE: TACManager
#########################

class TACManager:
    """
    Gerenciador de TAC - Responsável por gerar variáveis temporárias e labels únicos.
    Mantém contadores para t0, t1... e L0, L1...
    """

    def __init__(self):
        """Inicializa contadores zerados."""
        self._temp_counter = 0
        self._label_counter = 0
        self._total_temps_created = 0
        self._total_labels_created = 0

    def new_temp(self) -> str:
        """
        Gera e retorna uma nova variável temporária única (ex: 't0').
        """
        temp_name = f"t{self._temp_counter}"
        self._temp_counter += 1
        self._total_temps_created += 1
        return temp_name

    def new_label(self) -> str:
        """
        Gera e retorna um novo label único (ex: 'L0').
        """
        label_name = f"L{self._label_counter}"
        self._label_counter += 1
        self._total_labels_created += 1
        return label_name

    def reset_counters(self) -> None:
        """
        Reinicia os contadores de temporários e labels para 0.
        Útil ao iniciar o processamento de um novo programa.
        """
        self._temp_counter = 0
        self._label_counter = 0

    def get_temp_count(self) -> int:
        """Retorna o valor atual do contador de temporários."""
        return self._temp_counter

    def get_label_count(self) -> int:
        """Retorna o valor atual do contador de labels."""
        return self._label_counter

    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas de uso (contadores atuais e totais criados).
        """
        return {
            "current_temp_count": self._temp_counter,
            "current_label_count": self._label_counter,
            "total_temps_created": self._total_temps_created,
            "total_labels_created": self._total_labels_created
        }

    def __repr__(self) -> str:
        return (f"TACManager(temp_counter={self._temp_counter}, "
                f"label_counter={self._label_counter}, "
                f"total_temps={self._total_temps_created}, "
                f"total_labels={self._total_labels_created})")