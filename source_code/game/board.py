from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from config import BOARD_SIZE, WIN_LENGTH, EMPTY, HUMAN, AI

Move = Tuple[int, int]

@dataclass
class Board:
    size: int = BOARD_SIZE
    grid: List[List[str]] = field(default_factory=lambda: [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)])

    def clone(self) -> "Board":
        b = Board(self.size)
        b.grid = [row[:] for row in self.grid]
        return b

    def reset(self) -> None:
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]

    def inside(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size

    def is_empty(self, row: int, col: int) -> bool:
        return self.inside(row, col) and self.grid[row][col] == EMPTY

    def make_move(self, row: int, col: int, player: str) -> bool:
        if self.is_empty(row, col):
            self.grid[row][col] = player
            return True
        return False

    def undo_move(self, row: int, col: int) -> None:
        if self.inside(row, col):
            self.grid[row][col] = EMPTY

    def get_empty_cells(self) -> List[Move]:
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == EMPTY]

    def has_any_stone(self) -> bool:
        return any(self.grid[r][c] != EMPTY for r in range(self.size) for c in range(self.size))

    def is_full(self) -> bool:
        return all(self.grid[r][c] != EMPTY for r in range(self.size) for c in range(self.size))

    def check_winner(self) -> Optional[str]:
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(self.size):
            for c in range(self.size):
                player = self.grid[r][c]
                if player == EMPTY:
                    continue
                for dr, dc in directions:
                    ok = True
                    for k in range(1, WIN_LENGTH):
                        nr, nc = r + dr * k, c + dc * k
                        if not self.inside(nr, nc) or self.grid[nr][nc] != player:
                            ok = False
                            break
                    if ok:
                        return player
        if self.is_full():
            return "DRAW"
        return None

    def serialize(self) -> str:
        return "".join("".join(row) for row in self.grid)

    @classmethod
    def from_rows(cls, rows: List[str]) -> "Board":
        b = cls(len(rows))
        b.grid = [list(row) for row in rows]
        return b

    def __str__(self) -> str:
        header = "   " + " ".join(str(i) for i in range(self.size))
        lines = [header]
        for i, row in enumerate(self.grid):
            lines.append(f"{i:2d} " + " ".join(row))
        return "\n".join(lines)
