"""
Board module for PyCatan.

Represents the Catan game board as a collection of hexagonal tiles.
Each hex has a terrain type (which determines the resource it produces)
and a number token (the dice total that triggers production).

The board uses axial coordinates (q, r) to address hexes, which is a
standard approach for hex-grid games.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field


# Terrain types and the resource each produces
TERRAIN_RESOURCES: dict[str, str | None] = {
    "hills":   "brick",
    "forest":  "lumber",
    "mountains": "ore",
    "fields":  "grain",
    "pasture": "wool",
    "desert":  None,       # the desert produces nothing
}

# Standard Catan terrain distribution (19 hexes)
TERRAIN_DISTRIBUTION: list[str] = (
    ["hills"] * 3
    + ["forest"] * 4
    + ["mountains"] * 3
    + ["fields"] * 4
    + ["pasture"] * 4
    + ["desert"] * 1
)

# Number tokens placed on non-desert hexes (standard order)
NUMBER_TOKENS: list[int] = [
    2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12,
]


@dataclass
class Hex:
    """A single hexagonal tile on the board."""
    q: int                          # axial column
    r: int                          # axial row
    terrain: str = "desert"
    number_token: int | None = None
    has_robber: bool = False

    @property
    def resource(self) -> str | None:
        return TERRAIN_RESOURCES.get(self.terrain)

    def __repr__(self) -> str:
        token = self.number_token if self.number_token else "-"
        return f"Hex({self.q},{self.r} {self.terrain} [{token}])"


@dataclass
class Board:
    """
    The Catan game board.

    Currently stores hexes only.  Vertices (intersections) and edges
    are planned for a future milestone.
    """
    hexes: list[Hex] = field(default_factory=list)

    # TODO: Add vertices (intersections) for settlement/city placement
    # TODO: Add edges for road placement
    # TODO: Add harbours / port trading logic

    def generate(self) -> None:
        """Build the standard 19-hex board with randomised terrain and tokens."""
        # Axial coordinates for a size-2 hex grid (radius 2 from centre)
        coords = [
            (q, r)
            for q in range(-2, 3)
            for r in range(-2, 3)
            if -2 <= q + r <= 2
        ]

        terrains = TERRAIN_DISTRIBUTION.copy()
        random.shuffle(terrains)

        tokens = NUMBER_TOKENS.copy()
        random.shuffle(tokens)

        self.hexes.clear()
        token_idx = 0
        for (q, r), terrain in zip(coords, terrains):
            if terrain == "desert":
                h = Hex(q, r, terrain, number_token=None, has_robber=True)
            else:
                h = Hex(q, r, terrain, number_token=tokens[token_idx])
                token_idx += 1
            self.hexes.append(h)

    def hexes_for_roll(self, roll_total: int) -> list[Hex]:
        """Return all hexes whose number token matches the dice total."""
        return [h for h in self.hexes if h.number_token == roll_total and not h.has_robber]

    # TODO: Implement get_adjacent_hexes(q, r) using axial neighbour offsets
    # TODO: Implement vertex / edge lookup for building validation
    # TODO: Implement robber movement logic

    def display(self) -> str:
        """Return a simple text representation of the board for debugging."""
        lines = []
        for h in self.hexes:
            token_str = str(h.number_token).rjust(2) if h.number_token else " -"
            robber = " [R]" if h.has_robber else ""
            lines.append(f"  ({h.q:+d},{h.r:+d})  {h.terrain:<10}  {token_str}{robber}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Board(hexes={len(self.hexes)})"


if __name__ == "__main__":
    board = Board()
    board.generate()
    print(board)
    print()
    print(board.display())
