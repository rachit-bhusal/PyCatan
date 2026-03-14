"""
GUI module for PyCatan.

Provides a Tkinter-based graphical interface that renders the hex board,
player information, and basic game controls.  This is an early-stage UI;
many visual elements are placeholders.
"""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pycatan.game.game_manager import GameManager

# Colour map: terrain type → fill colour
TERRAIN_COLOURS: dict[str, str] = {
    "hills":     "#c45a2d",
    "forest":    "#2d8c3c",
    "mountains": "#7a7a7a",
    "fields":    "#e8c840",
    "pasture":   "#90d050",
    "desert":    "#e8d8a0",
}

HEX_SIZE = 40


def _hex_corners(cx: float, cy: float, size: float) -> list[tuple[float, float]]:
    """Return the six corner coordinates of a flat-topped hexagon."""
    corners = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        corners.append((cx + size * math.cos(angle_rad),
                         cy + size * math.sin(angle_rad)))
    return corners


class CatanGUI:
    """Main application window for PyCatan."""

    def __init__(self, game_manager: GameManager):
        self.gm = game_manager

        self.root = tk.Tk()
        self.root.title("PyCatan – Settlers of Catan")
        self.root.configure(bg="#1a3a5c")
        self.root.resizable(False, False)

        self._build_layout()

    # --- layout -------------------------------------------------------------

    def _build_layout(self) -> None:
        # Board canvas (left)
        self.canvas = tk.Canvas(
            self.root, width=560, height=500, bg="#4a90c4", highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

        # Side panel (right)
        side = tk.Frame(self.root, bg="#1a3a5c", width=240)
        side.grid(row=0, column=1, sticky="n", padx=(0, 10), pady=10)

        # -- Info label
        self.info_label = tk.Label(
            side, text="PyCatan", font=("Segoe UI", 16, "bold"),
            fg="white", bg="#1a3a5c",
        )
        self.info_label.pack(pady=(0, 10))

        # -- Player cards
        self.player_frames: dict[str, dict] = {}
        for player in self.gm.players:
            self._create_player_card(side, player)

        # -- Dice area
        dice_frame = tk.Frame(side, bg="#1a3a5c")
        dice_frame.pack(pady=15)

        self.dice_label = tk.Label(
            dice_frame, text="🎲  –", font=("Segoe UI", 18),
            fg="white", bg="#1a3a5c",
        )
        self.dice_label.pack()

        self.roll_btn = tk.Button(
            dice_frame, text="Roll Dice", font=("Segoe UI", 11, "bold"),
            bg="#e8c840", fg="#1a1a1a", activebackground="#d4b530",
            width=14, command=self._on_roll_dice,
        )
        self.roll_btn.pack(pady=6)

        # -- Status bar
        self.status_var = tk.StringVar(value="Press Roll Dice to begin your turn.")
        status_bar = tk.Label(
            self.root, textvariable=self.status_var,
            font=("Segoe UI", 10), fg="white", bg="#12304a",
            anchor="w", padx=8, pady=4,
        )
        status_bar.grid(row=3, column=0, columnspan=2, sticky="ew")

        # TODO: Add buttons for Build Settlement, Build Road, Trade
        # TODO: Add a turn-end button
        # TODO: Add a game log / event feed panel

    def _create_player_card(self, parent: tk.Frame, player) -> None:
        """Add a small card showing player info to the side panel."""
        frame = tk.Frame(parent, bg="#244b6e", bd=1, relief="groove")
        frame.pack(fill="x", pady=3)

        header = tk.Label(
            frame, text=f"  {player.name}",
            font=("Segoe UI", 11, "bold"), fg=player.colour, bg="#244b6e",
            anchor="w",
        )
        header.pack(fill="x", padx=4, pady=(4, 0))

        detail = tk.Label(
            frame,
            text=f"  VP: {player.victory_points}  |  Cards: {player.resource_total()}",
            font=("Segoe UI", 9), fg="#c0d0e0", bg="#244b6e", anchor="w",
        )
        detail.pack(fill="x", padx=4, pady=(0, 4))

        self.player_frames[player.name] = {"frame": frame, "detail": detail}

    # --- drawing ------------------------------------------------------------

    def draw_board(self) -> None:
        """Render all hexes on the canvas."""
        self.canvas.delete("all")

        origin_x, origin_y = 280, 250

        for h in self.gm.board.hexes:
            # Axial → pixel (flat-topped hex)
            cx = origin_x + HEX_SIZE * (3 / 2 * h.q)
            cy = origin_y + HEX_SIZE * (math.sqrt(3) * (h.r + h.q / 2))

            corners = _hex_corners(cx, cy, HEX_SIZE - 2)
            colour = TERRAIN_COLOURS.get(h.terrain, "#cccccc")

            self.canvas.create_polygon(
                corners, fill=colour, outline="#1a3a5c", width=2,
            )

            # Number token
            if h.number_token is not None:
                token_fg = "#cc0000" if h.number_token in (6, 8) else "#1a1a1a"
                self.canvas.create_oval(
                    cx - 12, cy - 12, cx + 12, cy + 12,
                    fill="#f5f0e0", outline="#8a7a50",
                )
                self.canvas.create_text(
                    cx, cy, text=str(h.number_token),
                    font=("Segoe UI", 10, "bold"), fill=token_fg,
                )

            # Robber indicator
            if h.has_robber:
                self.canvas.create_text(
                    cx, cy, text="⛌", font=("Segoe UI", 16), fill="#1a1a1a",
                )

        # TODO: Draw vertices (dots) at hex intersections for settlement spots
        # TODO: Draw edges between vertices for road placement
        # TODO: Highlight selectable positions during build phase

    # --- callbacks ----------------------------------------------------------

    def _on_roll_dice(self) -> None:
        total = self.gm.roll_dice()
        die1, die2 = self.gm.dice.last_roll
        self.dice_label.config(text=f"🎲  {die1} + {die2} = {total}")

        player = self.gm.current_player()
        self.gm.distribute_resources(total)

        if player.is_ai:
            self.gm.handle_ai_turn(player)

        self._refresh_players()
        self.gm.next_turn()
        next_p = self.gm.current_player()
        self.status_var.set(f"{next_p.name}'s turn — press Roll Dice.")

        # TODO: Disable roll button until current player ends turn
        # TODO: Enable build / trade buttons after rolling

    def _refresh_players(self) -> None:
        """Update the player information cards."""
        for player in self.gm.players:
            info = self.player_frames.get(player.name)
            if info:
                info["detail"].config(
                    text=f"  VP: {player.victory_points}  |  Cards: {player.resource_total()}"
                )

    # --- main loop ----------------------------------------------------------

    def run(self) -> None:
        """Start the Tkinter main loop."""
        self.gm.start_game()
        self.draw_board()
        self.root.mainloop()
