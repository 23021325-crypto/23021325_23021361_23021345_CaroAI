from __future__ import annotations
import time
from dataclasses import dataclass
from typing import Optional
from config import AI, HUMAN, DEFAULT_DEPTH
from game.board import Board, Move
from game.move_generator import find_winning_moves, generate_candidate_moves
from ai.evaluator import evaluate_board
from ai.minimax import MinimaxAI
from ai.alpha_beta import AlphaBetaAI
from ai.learning import ExperienceMemory

@dataclass
class AIMoveInfo:
    move: Optional[Move]
    score: int
    nodes: int
    elapsed: float
    algorithm: str
    depth: int
    reason: str

class CaroAgent:
    def __init__(self, memory: Optional[ExperienceMemory] = None):
        self.memory = memory or ExperienceMemory()

    def choose_move(self, board: Board, algorithm: str = "Alpha-Beta", depth: int = DEFAULT_DEPTH, use_learning: bool = True) -> AIMoveInfo:
        start = time.perf_counter()

        # 1. Tactical shortcut: win immediately.
        wins = find_winning_moves(board, AI)
        if wins:
            elapsed = time.perf_counter() - start
            return AIMoveInfo(wins[0], 10_000_000, 1, elapsed, algorithm, depth, "Máy có nước thắng ngay")

        # 2. Tactical shortcut: block opponent's immediate win.
        blocks = find_winning_moves(board, HUMAN)
        if blocks:
            elapsed = time.perf_counter() - start
            return AIMoveInfo(blocks[0], 9_000_000, 1, elapsed, algorithm, depth, "Chặn người chơi thắng ngay")

        algorithm_key = algorithm.lower().replace(" ", "").replace("-", "")
        searcher = AlphaBetaAI(depth) if "alpha" in algorithm_key else MinimaxAI(depth)

        # Learning is applied at root so the core algorithm still follows the assignment.
        if use_learning:
            best_move = None
            best_score = -10**12
            nodes_total = 0
            state = board.serialize()
            for move in generate_candidate_moves(board, AI):
                board.make_move(move[0], move[1], AI)
                result = searcher.search(board, max(depth - 1, 0))
                board.undo_move(move[0], move[1])
                nodes_total += result.nodes
                score = result.score + int(self.memory.get_bonus(state, move) * 10)
                if score > best_score:
                    best_score = score
                    best_move = move
            elapsed = time.perf_counter() - start
            return AIMoveInfo(best_move, int(best_score), nodes_total, elapsed, algorithm, depth, "Tìm kiếm + điểm kinh nghiệm")

        result = searcher.search(board, depth)
        elapsed = time.perf_counter() - start
        return AIMoveInfo(result.move, result.score, result.nodes, elapsed, algorithm, depth, "Tìm kiếm thuần")
