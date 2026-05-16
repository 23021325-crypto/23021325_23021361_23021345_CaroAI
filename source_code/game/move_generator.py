from __future__ import annotations
from typing import List, Tuple
from config import BOARD_SIZE, EMPTY, HUMAN, AI, MAX_CANDIDATE_MOVES
from game.board import Board, Move

DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]

def nearby_empty_moves(board: Board, radius: int = 2) -> List[Move]:
    if not board.has_any_stone():
        center = board.size // 2
        return [(center, center)]
    candidates = set()
    for r in range(board.size):
        for c in range(board.size):
            if board.grid[r][c] != EMPTY:
                for dr in range(-radius, radius + 1):
                    for dc in range(-radius, radius + 1):
                        nr, nc = r + dr, c + dc
                        if board.inside(nr, nc) and board.grid[nr][nc] == EMPTY:
                            candidates.add((nr, nc))
    return list(candidates)

def find_winning_moves(board: Board, player: str) -> List[Move]:
    wins: List[Move] = []
    for r, c in nearby_empty_moves(board, radius=1):
        board.make_move(r, c, player)
        if board.check_winner() == player:
            wins.append((r, c))
        board.undo_move(r, c)
    return wins

def _count_line(board: Board, row: int, col: int, dr: int, dc: int, player: str) -> Tuple[int, int]:
    count = 0
    open_end = 0
    r, c = row + dr, col + dc
    while board.inside(r, c) and board.grid[r][c] == player:
        count += 1
        r += dr
        c += dc
    if board.inside(r, c) and board.grid[r][c] == EMPTY:
        open_end = 1
    return count, open_end

def local_move_score(board: Board, move: Move, player: str) -> int:
    row, col = move
    opponent = HUMAN if player == AI else AI
    center = board.size // 2
    score = 30 - (abs(row - center) + abs(col - center))
    # Attack score for this move
    for dr, dc in DIRECTIONS:
        left, open_l = _count_line(board, row, col, -dr, -dc, player)
        right, open_r = _count_line(board, row, col, dr, dc, player)
        chain = left + right + 1
        open_ends = open_l + open_r
        if chain >= 4:
            score += 100000
        elif chain == 3:
            score += 6000 if open_ends == 2 else 2500
        elif chain == 2:
            score += 900 if open_ends == 2 else 350
        elif chain == 1 and open_ends == 2:
            score += 70
    # Defense score if opponent would like this square
    for dr, dc in DIRECTIONS:
        left, open_l = _count_line(board, row, col, -dr, -dc, opponent)
        right, open_r = _count_line(board, row, col, dr, dc, opponent)
        chain = left + right + 1
        open_ends = open_l + open_r
        if chain >= 4:
            score += 90000
        elif chain == 3:
            score += 5200 if open_ends == 2 else 2200
        elif chain == 2:
            score += 700 if open_ends == 2 else 260
    return score

def generate_candidate_moves(board: Board, player: str = AI, radius: int = 2, max_moves: int = MAX_CANDIDATE_MOVES) -> List[Move]:
    if not board.has_any_stone():
        center = board.size // 2
        return [(center, center)]

    # Always check tactical winning/blocking moves first.
    own_wins = find_winning_moves(board, player)
    if own_wins:
        return own_wins[:max_moves]
    opponent = HUMAN if player == AI else AI
    blocks = find_winning_moves(board, opponent)
    if blocks:
        return blocks[:max_moves]

    candidates = nearby_empty_moves(board, radius=radius)
    ordered = sorted(candidates, key=lambda m: local_move_score(board, m, player), reverse=True)
    return ordered[:max_moves]
