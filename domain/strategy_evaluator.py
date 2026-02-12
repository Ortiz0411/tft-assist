from typing import List
from domain.game_state import GameState


class StrategyRecommendation:
    def __init__(self, name: str, score: float, reason: str):
        self.name = name
        self.score = score
        self.reason = reason


class StrategyEvaluator:

    def evaluate(self, game_state: GameState,) -> List[StrategyRecommendation]:

        strategies = []

        strategies.append(self.evaluate_reroll(game_state))
        strategies.append(self.evaluate_fast8(game_state))
        strategies.append(self.evaluate_tempo(game_state))

        return sorted(strategies, key=lambda s: s.score, reverse=True)


    def evaluate_reroll(self, game_state: GameState) -> StrategyRecommendation:

        score = 0
        reasons = []

        if game_state.level <= 6:
            score += 20
            reasons.append("Good level for reroll")

        if game_state.gold >= 30:
            score += 15
            reasons.append("Good gold for reroll")

        if game_state.health > 60:
            score += 10
            reasons.append("Good health for reroll")

        """
        if game_state.low_cost_pairs():
            score += 25
            reasons.append("Have low cost pairs")
        """

        return StrategyRecommendation("Reroll", score, ", ".join(reasons))

    def evaluate_fast8(self, game_state: GameState) -> StrategyRecommendation:

        score = 0
        reasons = []

        if game_state.gold >= 50:
            score += 25
            reasons.append("Good economy for fast8")

        if game_state.health >= 70:
            score += 20
            reasons.append("Good health for fast8")

        if game_state.level >= 7:
            score += 15
            reasons.append("good level for fast8")

        return StrategyRecommendation("Fast8", score, ", ".join(reasons))

    def evaluate_tempo(self, game_state: GameState) -> StrategyRecommendation:

        score = 0
        reasons = []

        if game_state.health < 40:
            score += 30
            reasons.append("Low health, need to stabilize")

        if game_state.gold < 20:
            score += 15
            reasons.append("Low economy")

        return StrategyRecommendation("Tempo", score, ", ".join(reasons))