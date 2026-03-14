"""
Player module for PyCatan.

Represents a single player in the game, tracking their resources,
settlements, roads, and victory points.
"""

from __future__ import annotations


# The five resource types in Settlers of Catan
RESOURCE_TYPES = ("brick", "lumber", "ore", "grain", "wool")


class Player:
    """A player in the game of Catan."""

    def __init__(self, name: str, colour: str, is_ai: bool = False):
        self.name = name
        self.colour = colour
        self.is_ai = is_ai

        # Resources held by this player – all start at zero
        self.resources: dict[str, int] = {r: 0 for r in RESOURCE_TYPES}

        self.victory_points: int = 0
        self.settlements: list = []   # TODO: Store actual board positions
        self.roads: list = []         # TODO: Store actual board edges

    # --- resource helpers ---------------------------------------------------

    def add_resource(self, resource: str, amount: int = 1) -> None:
        """Award *amount* of *resource* to this player."""
        if resource not in self.resources:
            raise ValueError(f"Unknown resource type: {resource}")
        self.resources[resource] += amount

    def remove_resource(self, resource: str, amount: int = 1) -> bool:
        """Remove *amount* of *resource*.  Returns False if insufficient."""
        if self.resources.get(resource, 0) < amount:
            return False
        self.resources[resource] -= amount
        return True

    def resource_total(self) -> int:
        """Return the total number of resource cards held."""
        return sum(self.resources.values())

    # TODO: Implement can_build_settlement() – check resource requirements
    # TODO: Implement can_build_road() – check resource requirements
    # TODO: Implement can_build_city() – check resource requirements
    # TODO: Implement trade_with(player, offer, request) for player trading

    # --- victory points -----------------------------------------------------

    def add_victory_point(self, points: int = 1) -> None:
        self.victory_points += points

    def has_won(self, target: int = 10) -> bool:
        """Check whether the player has reached the victory-point target."""
        return self.victory_points >= target

    # --- display ------------------------------------------------------------

    def resource_summary(self) -> str:
        """Return a human-readable summary of held resources."""
        parts = [f"{res}: {qty}" for res, qty in self.resources.items() if qty > 0]
        return ", ".join(parts) if parts else "no resources"

    def __repr__(self) -> str:
        return (
            f"Player(name={self.name!r}, colour={self.colour!r}, "
            f"vp={self.victory_points}, resources={self.resource_summary()})"
        )


if __name__ == "__main__":
    p = Player("Alice", "red")
    p.add_resource("brick", 3)
    p.add_resource("lumber", 2)
    print(p)
    print(f"Total cards: {p.resource_total()}")
