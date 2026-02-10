from typing import List
from domain.game_state import GameState
from domain.models import Composition, EvaluationResult


class CompositionEvaluator:
    """ Evaluate the game state to make recommendation based on items, champions, ... """

    def evaluate(self, game_state: GameState, comp: Composition) -> EvaluationResult:

        score = 0.0
        reasons = []

        # 1. Items
        matching_items = set(game_state.items) & set(comp.core_items)
        if matching_items:
            score += len(matching_items) * 1.5
            reasons.append(f"You have good core items: {', '.join(matching_items)}")

        # 2. Champions
        matching_champions = set(game_state.champions) & set(comp.core_champions)
        if matching_champions:
            score += len(matching_champions) * 1.0
            reasons.append(f"You have good core champions: {'. '.join(matching_champions)}")

        # 3. Level
        level_diff = comp.recommended_level - game_state.level
        if level_diff <= 0:
            score += 1.0
            reasons.append('Your level is good for the comp')
        else:
            score -= 1.0
            reasons.append(f'You are {level_diff} levels from the recommended level')

        # 4. Lobby pressure
        for synergy in comp.main_synergies:
            pressure = game_state.synergies.get_synergies(synergy)
            if pressure > 0:
                penalty = pressure * 0.7
                score -= penalty
                reasons.append(f'{synergy} is contested in the lobby.')

        return EvaluationResult(
            composition_id=comp.id,
            composition_name=comp.name,
            score=round(score, 2),
            reasons=reasons
        )


class CompositionRanker:

    def __init__(self, evaluator: CompositionEvaluator):
        self.evaluator = evaluator

    def rank(self, game_state: GameState, compositions: List[Composition]):

        results = []

        for comp in compositions:
            result = self.evaluator.evaluate(game_state, comp)
            results.append(result)

        results.sort(key=lambda r: r.score, reverse=True)
        return results