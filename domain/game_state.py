from dataclasses import dataclass
from typing import Dict, List


@dataclass()
class LobbySynergies:
    """ Count how many synergies are in the lobby.
        Example: {'tanks': 3, 'mages': 2}"""

    synergies: Dict[str, int]

    def get_synergies(self, synergy: str) -> int:
        return self.synergies.get(synergy, 0)


@dataclass()
class GameState:
    """ Current state of the game """
    level: int
    gold: int
    health: int

    champions: List[str]
    items: List[str]
    augments: List[str]

    synergies: LobbySynergies