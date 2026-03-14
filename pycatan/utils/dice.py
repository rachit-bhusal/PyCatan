"""
Dice module for PyCatan.

Handles rolling two six-sided dice, which is the core randomisation
mechanic in Settlers of Catan.  Each turn a player rolls two dice and
the sum determines which hexes produce resources.
"""

import random


class Dice:
    """Simulates a pair of standard six-sided dice."""

    def __init__(self):
        self.last_roll = (0, 0)

    def roll(self) -> tuple[int, int]:
        """Roll two dice and return the individual results as a tuple."""
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        self.last_roll = (die1, die2)
        return self.last_roll

    def total(self) -> int:
        """Return the sum of the most recent roll."""
        return sum(self.last_roll)

    # TODO: Add probability tracking / statistics for rolled values
    # TODO: Implement a "weighted" mode for testing specific scenarios

    def __repr__(self) -> str:
        return f"Dice(last_roll={self.last_roll}, total={self.total()})"


if __name__ == "__main__":
    dice = Dice()
    result = dice.roll()
    print(f"Rolled: {result[0]} + {result[1]} = {dice.total()}")
