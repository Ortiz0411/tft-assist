from domain.game_state import GameState, LobbySynergies
from domain.models import Composition
from domain.evaluation import CompositionEvaluator, CompositionRanker


def main():

    lobby = LobbySynergies(
        synergies={
            "mages": 1,
            "tanks": 2
        }
    )

    game_state = GameState(
        level=7,
        gold=40,
        health=60,
        champions=["ahri", "garen"],
        items=["rabadon"],
        augments=["jeweled_lotus"],
        synergies=lobby
    )

    comps = [
        Composition(
            id="mage_flex",
            name="Mage Flex",
            core_champions=["ahri", "lux"],
            core_items=["rabadon", "blue_buff"],
            main_synergies=["mages"],
            recommended_level=8
        ),
        Composition(
            id="bruiser_core",
            name="Bruiser Core",
            core_champions=["garen", "darius"],
            core_items=["sunfire"],
            main_synergies=["bruisers"],
            recommended_level=7
        )
    ]

    evaluator = CompositionEvaluator()
    ranker = CompositionRanker(evaluator)

    results = ranker.rank(game_state, comps)

    for r in results:
        print(f"{r.composition_name} → {r.score}")
        for reason in r.reasons:
            print("  -", reason)
        print()

if __name__ == "__main__":
    main()