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

    def rank(self, game_state: GameState, compositions: List[Composition], strategy_name: str):

        results = []

        for comp in compositions:

            result = self.evaluator.evaluate(game_state, comp)

            strategy_score = self.strategy_modifier(result.score, comp, strategy_name)
            meta_score = self.meta_modifier(comp)
            final_score = strategy_score + meta_score

            result.score = round(final_score, 2)
            results.append(result)

        results.sort(key=lambda r: r.score, reverse=True)
        return results

    def strategy_modifier(self, score: float, comp: Composition, strategy_name: str) -> float:

        modifier = 0.0

        if strategy_name == "Reroll":
            if comp.recommended_level <= 6:
                modifier += 1.5
            else:
                modifier -= 1.0

        elif strategy_name == "Fast8":
            if comp.recommended_level >= 8:
                modifier += 2.0
            else:
                modifier -= 0.5

        elif strategy_name == "Tempo":
            modifier += 0.5

        return score + modifier

    def meta_modifier(self, comp: Composition) -> float:

        score = 0.0

        score += (comp.winrate - 0.5) * 4

        if comp.pickrate > 0.25:
            score -= 1.0
        elif comp.pickrate < 0.10:
            score += 0.5

        return score

