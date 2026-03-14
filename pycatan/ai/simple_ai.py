"""
Simple AI module for PyCatan.

Provides a basic rule-based AI opponent.  For Milestone 3 this is a
placeholder that makes random / trivial decisions.  Future milestones
will replace this with a more strategic decision engine.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pycatan.game.player import Player
    from pycatan.game.board import Board


class SimpleAI:
    """A rudimentary AI that can take basic game actions."""

    def __init__(self, player: Player):
        self.player = player

    def decide_action(self, board: Board) -> str:
        """
        Choose an action for this turn.

        Currently picks randomly from a fixed list of possible actions.
        Returns a string label describing the chosen action.
        """
        # Placeholder action pool – will be context-sensitive later
        possible_actions = [
            "build_settlement",
            "build_road",
            "buy_development_card",
            "trade_resources",
            "pass",
        ]

        # TODO: Evaluate available resources before choosing an action
        # TODO: Prioritise settlement building when resources allow
        # TODO: Implement a scoring heuristic for each possible action
        # TODO: Consider board state (available vertices, opponent positions)

        action = random.choice(possible_actions)
        return action

    def choose_trade(self) -> dict | None:
        """
        Decide whether to propose a trade and what to offer.

        Returns a trade proposal dict, or None if the AI declines.
        """
        # TODO: Implement resource evaluation to decide trade offers
        # TODO: Implement port trading when the player owns a harbour
        return None

    def choose_robber_placement(self, board: Board) -> tuple[int, int] | None:
        """
        Choose where to move the robber when a 7 is rolled.

        Currently returns None (no move).
        """
        # TODO: Pick the hex that most harms the leading opponent
        return None

    def __repr__(self) -> str:
        return f"SimpleAI(player={self.player.name!r})"


if __name__ == "__main__":
    from pycatan.game.player import Player
    from pycatan.game.board import Board

    ai_player = Player("CPU", "grey", is_ai=True)
    board = Board()
    board.generate()

    ai = SimpleAI(ai_player)
    decision = ai.decide_action(board)
    print(f"AI ({ai_player.name}) decided to: {decision}")
