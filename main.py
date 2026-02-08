from domain.game_state import GameState, LobbySynergies

def main():

    lobby = LobbySynergies(
        synergies={
            "mages": 2,
            "tanks": 4
        }
    )

    game_state = GameState(
        level=6,
        gold=52,
        health=60,
        champions=["aatrox", "azir", "garen"],
        items=["tear", "rabadon"],
        augments=["critic", "economy"],
        synergies=lobby
    )

    print(game_state)

if __name__ == "__main__":
    main()