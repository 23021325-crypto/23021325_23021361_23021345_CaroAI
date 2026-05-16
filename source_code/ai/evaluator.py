from __future__ import annotations
from config import EMPTY, HUMAN, AI
from game.board import Board

WIN_SCORE = 10_000_000
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]

WINDOW_SCORE = {
    (4, 0): 1_000_000,
    (3, 1): 30_000,
    (3, 0): 9_000,
    (2, 2): 4_000,
    (2, 1): 1_200,
    (1, 3): 100,
}

def evaluate_window(window, player: str) -> int:
    opponent = HUMAN if player == AI else AI
    p = window.count(player)
    o = window.count(opponent)
    e = window.count(EMPTY)
    if p > 0 and o > 0:
        return 0
    if p == 4:
        return WIN_SCORE
    if o == 4:
        return -WIN_SCORE
    attack = WINDOW_SCORE.get((p, e), 0)
    defend = WINDOW_SCORE.get((o, e), 0)
    # Defense is weighted slightly higher to avoid missing an opponent threat.
    return attack - int(defend * 1.12)

def evaluate_board(board: Board, player: str = AI) -> int:
    winner = board.check_winner()
    opponent = HUMAN if player == AI else AI
    if winner == player:
        return WIN_SCORE
    if winner == opponent:
        return -WIN_SCORE
    if winner == "DRAW":
        return 0

    total = 0
    n = board.size
    for r in range(n):
        for c in range(n):
            for dr, dc in DIRECTIONS:
                end_r = r + (3 * dr)
                end_c = c + (3 * dc)
                if 0 <= end_r < n and 0 <= end_c < n:
                    window = [board.grid[r + k * dr][c + k * dc] for k in range(4)]
                    total += evaluate_window(window, player)

    # Small center bonus makes early-game play more natural.
    center = n // 2
    for r in range(n):
        for c in range(n):
            if board.grid[r][c] == player:
                total += 12 - (abs(r - center) + abs(c - center))
            elif board.grid[r][c] == opponent:
                total -= 10 - (abs(r - center) + abs(c - center))
    return total
