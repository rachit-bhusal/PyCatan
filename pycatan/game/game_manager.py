"""
Game Manager module for PyCatan.

Orchestrates the overall game flow: player turns, dice rolls,
resource distribution, and win-condition checking.  This is the
central controller that ties all other modules together.
"""

from __future__ import annotations

from pycatan.game.board import Board
from pycatan.game.player import Player, RESOURCE_TYPES
from pycatan.ai.simple_ai import SimpleAI
from pycatan.utils.dice import Dice


class GameManager:
    """
    Controls the flow of a PyCatan game session.

    Manages the turn cycle, invokes AI decisions, and (eventually)
    enforces game rules.
    """

    PLAYER_COLOURS = ["red", "blue", "green", "orange"]

    def __init__(self, human_name: str = "Player 1", num_ai: int = 1):
        self.board = Board()
        self.dice = Dice()
        self.players: list[Player] = []
        self.ai_controllers: dict[str, SimpleAI] = {}
        self.current_turn: int = 0
        self.game_over: bool = False
        self.winner: Player | None = None

        self._setup_players(human_name, num_ai)

    # --- setup --------------------------------------------------------------

    def _setup_players(self, human_name: str, num_ai: int) -> None:
        """Create the human player and AI opponents."""
        human = Player(human_name, self.PLAYER_COLOURS[0])
        self.players.append(human)

        for i in range(num_ai):
            colour = self.PLAYER_COLOURS[i + 1]
            ai_player = Player(f"CPU {i + 1}", colour, is_ai=True)
            self.players.append(ai_player)
            self.ai_controllers[ai_player.name] = SimpleAI(ai_player)

    def start_game(self) -> None:
        """Initialise the board and prepare for the first turn."""
        self.board.generate()
        self.current_turn = 0
        self.game_over = False
        self.winner = None
        print("[GameManager] Board generated. Game started!")
        print(f"[GameManager] Players: {[p.name for p in self.players]}")

        # TODO: Implement initial settlement/road placement phase
        # TODO: Distribute starting resources based on initial settlements

    # --- turn cycle ----------------------------------------------------------

    def current_player(self) -> Player:
        return self.players[self.current_turn % len(self.players)]

    def next_turn(self) -> None:
        """Advance to the next player's turn."""
        self.current_turn += 1
        player = self.current_player()
        print(f"\n--- Turn {self.current_turn}: {player.name}'s turn ---")

    def roll_dice(self) -> int:
        """Roll the dice and return the total."""
        result = self.dice.roll()
        total = self.dice.total()
        print(f"[Dice] Rolled {result[0]} + {result[1]} = {total}")
        return total

    def distribute_resources(self, roll_total: int) -> None:
        """
        Hand out resources to players based on the dice roll.

        This is a simplified placeholder – full logic requires checking
        which players have settlements adjacent to the producing hexes.
        """
        producing_hexes = self.board.hexes_for_roll(roll_total)
        if not producing_hexes:
            print(f"[Resources] No hexes produce for roll {roll_total}.")
            return

        for h in producing_hexes:
            print(f"[Resources] {h.terrain} hex at ({h.q},{h.r}) produces {h.resource}")

        # TODO: Check settlement adjacency to determine which players receive resources
        # TODO: Award correct quantities (1 per settlement, 2 per city)
        # TODO: Handle resource bank depletion

    def handle_ai_turn(self, player: Player) -> None:
        """Let the AI controller for *player* take its turn."""
        ai = self.ai_controllers.get(player.name)
        if ai is None:
            return
        action = ai.decide_action(self.board)
        print(f"[AI] {player.name} decides to: {action}")

        # TODO: Execute the chosen action (build, trade, etc.)
        # TODO: Validate action against game rules

    def check_win_condition(self) -> bool:
        """Check if any player has reached 10 victory points."""
        for player in self.players:
            if player.has_won():
                self.game_over = True
                self.winner = player
                print(f"\n*** {player.name} wins with {player.victory_points} VP! ***")
                return True
        return False

    # TODO: Implement full turn loop (roll → distribute → build/trade → end turn)
    # TODO: Implement robber logic when a 7 is rolled
    # TODO: Implement development-card purchasing and usage
    # TODO: Implement longest-road and largest-army tracking

    def play_one_round(self) -> None:
        """Execute a single demonstration round for all players."""
        for _ in self.players:
            self.next_turn()
            player = self.current_player()
            total = self.roll_dice()
            self.distribute_resources(total)

            if player.is_ai:
                self.handle_ai_turn(player)

            if self.check_win_condition():
                return

    def __repr__(self) -> str:
        status = "OVER" if self.game_over else "IN PROGRESS"
        return f"GameManager(turn={self.current_turn}, status={status})"


if __name__ == "__main__":
    gm = GameManager("Alice", num_ai=2)
    gm.start_game()
    gm.play_one_round()
