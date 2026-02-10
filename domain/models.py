from dataclasses import dataclass
from typing import List


@dataclass
class Composition:
    """ compisition data: champions, items and synergies """

    id: str
    name: str

    core_champions: List[str]
    core_items: List[str]
    main_synergies: List[str]

    recommended_level: int


@dataclass
class EvaluationResult:
    composition_id: str
    composition_name: str
    score: float
    reasons: List[str]