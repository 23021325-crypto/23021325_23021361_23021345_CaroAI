from __future__ import annotations
import json
import os
from typing import Dict, Tuple, List
from config import LEARNING_FILE

Move = Tuple[int, int]

class ExperienceMemory:
    """Simple post-game learning memory.

    This is not a neural network. It stores a score for (board_state, move).
    Winning games reinforce the selected moves; losing games penalize them.
    """

    def __init__(self, path: str = LEARNING_FILE):
        self.path = path
        self.data: Dict[str, float] = {}
        self.games_learned = 0
        self.load()

    def _key(self, state: str, move: Move) -> str:
        return f"{state}|{move[0]},{move[1]}"

    def load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                self.data = raw.get("values", {})
                self.games_learned = int(raw.get("games_learned", 0))
            except Exception:
                self.data = {}
                self.games_learned = 0

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"games_learned": self.games_learned, "values": self.data}, f, ensure_ascii=False, indent=2)

    def get_bonus(self, state: str, move: Move) -> float:
        return float(self.data.get(self._key(state, move), 0.0))

    def update_after_game(self, history: List[Tuple[str, Move]], result: str) -> None:
        if not history:
            return
        if result == "AI_WIN":
            reward = 35.0
        elif result == "HUMAN_WIN":
            reward = -45.0
        else:
            reward = 6.0
        # Later moves are more directly connected to the result.
        for idx, (state, move) in enumerate(history):
            weight = 0.6 + 0.4 * ((idx + 1) / len(history))
            key = self._key(state, move)
            self.data[key] = float(self.data.get(key, 0.0)) + reward * weight
            self.data[key] = max(-300.0, min(300.0, self.data[key]))
        self.games_learned += 1
        self.save()

    def clear(self) -> None:
        self.data = {}
        self.games_learned = 0
        self.save()
