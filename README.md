# PyCatan – Simplified Settlers of Catan

A Python implementation of a simplified version of *Settlers of Catan*, featuring a graphical user interface and an AI opponent. This is a university coursework project currently under active development.

## Project Structure

```
pycatan/
├── main.py              # Application entry point
├── game/
│   ├── board.py         # Hex-grid board representation
│   ├── player.py        # Player model (resources, VP, inventory)
│   └── game_manager.py  # Turn cycle and game orchestration
├── ai/
│   └── simple_ai.py     # Rule-based AI opponent (placeholder)
├── ui/
│   └── gui.py           # Tkinter-based graphical interface
├── utils/
│   └── dice.py          # Dice rolling utility
└── assets/              # (Reserved for images/sounds)
```

## Current Status – Milestone 3

### Implemented

- **Board generation** – 19-hex board with randomised terrain and number tokens using axial coordinates.
- **Player model** – Resource tracking, victory-point management, and display helpers.
- **Dice rolling** – Two six-sided dice with result history.
- **Basic AI** – Placeholder AI that selects a random action each turn.
- **GUI window** – Tkinter interface that renders the hex board, player cards, and a dice-roll button.
- **Game manager** – Turn cycle skeleton connecting board, players, dice, and AI.

### In Progress

- Resource distribution after dice rolls (hexes identified, player adjacency not yet wired).
- Settlement and road placement on board vertices/edges.
- Robber movement on rolling a 7.

### Planned Features

- Full Catan rule enforcement (building costs, placement validation).
- Player-to-player and bank/port trading.
- Development cards (Knight, Victory Point, Road Building, etc.).
- Improved AI strategy with heuristic scoring.
- Longest Road / Largest Army tracking.
- Win-condition enforcement (first to 10 VP).
- Sound effects and improved visual assets.

## How to Run

**Requirements:** Python 3.11+ with Tkinter (included in standard Python distributions).

```bash
# Clone the repository
git clone <repo-url>
cd PyCatan

# Run the game
python -m pycatan.main
```

Individual modules can also be tested standalone:

```bash
python -m pycatan.utils.dice        # Roll dice demo
python -m pycatan.game.player       # Player model demo
python -m pycatan.game.board        # Board generation demo
python -m pycatan.ai.simple_ai      # AI decision demo
python -m pycatan.game.game_manager # Game manager demo
```
