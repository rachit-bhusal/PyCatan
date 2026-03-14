"""
PyCatan – Main Entry Point

Launches the PyCatan game with a GUI window and one AI opponent.
Run this file to start the application:

    python -m pycatan.main
"""

from pycatan.game.game_manager import GameManager
from pycatan.ui.gui import CatanGUI


def main() -> None:
    print("=" * 50)
    print("  PyCatan – Settlers of Catan (Early Build)")
    print("=" * 50)

    gm = GameManager(human_name="Player 1", num_ai=1)
    gui = CatanGUI(gm)
    gui.run()


if __name__ == "__main__":
    main()
