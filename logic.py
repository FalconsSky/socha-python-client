import random

from socha import *


class Logic(IClientHandler):
    gameState: GameState

    def calculate_move(self) -> Move:
        possible_moves = self.gameState.possible_moves
        return possible_moves[random.randint(0, len(possible_moves) - 1)]

    def on_update(self, state: GameState):
        self.gameState = state

    def on_error(self, logMessage: str):
        ...


if __name__ == "__main__":
    Starter(logic=Logic())
