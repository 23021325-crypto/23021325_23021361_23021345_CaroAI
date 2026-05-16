from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple
from config import AI, HUMAN
from game.board import Board, Move
from game.move_generator import generate_candidate_moves
from ai.evaluator import evaluate_board, WIN_SCORE

@dataclass
class SearchResult:
    move: Optional[Move]
    score: int
    nodes: int

class AlphaBetaAI:
    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth
        self.nodes = 0

    def search(self, board: Board, depth: Optional[int] = None) -> SearchResult:
        self.nodes = 0
        depth = self.max_depth if depth is None else depth
        score, move = self._alphabeta(board, depth, -WIN_SCORE * 2, WIN_SCORE * 2, True)
        return SearchResult(move, score, self.nodes)

    def _alphabeta(self, board: Board, depth: int, alpha: int, beta: int, maximizing: bool) -> Tuple[int, Optional[Move]]:
        self.nodes += 1
        winner = board.check_winner()
        if winner or depth == 0:
            return evaluate_board(board, AI), None

        player = AI if maximizing else HUMAN
        moves = generate_candidate_moves(board, player)
        if not moves:
            return evaluate_board(board, AI), None

        best_move = None
        if maximizing:
            best_score = -WIN_SCORE * 2
            for move in moves:
                board.make_move(move[0], move[1], AI)
                score, _ = self._alphabeta(board, depth - 1, alpha, beta, False)
                board.undo_move(move[0], move[1])
                if score > best_score:
                    best_score, best_move = score, move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move
        else:
            best_score = WIN_SCORE * 2
            for move in moves:
                board.make_move(move[0], move[1], HUMAN)
                score, _ = self._alphabeta(board, depth - 1, alpha, beta, True)
                board.undo_move(move[0], move[1])
                if score < best_score:
                    best_score, best_move = score, move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move
