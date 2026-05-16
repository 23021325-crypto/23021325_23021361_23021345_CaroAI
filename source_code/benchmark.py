from __future__ import annotations
import time
from config import RESULT_FILE
from ai.minimax import MinimaxAI
from ai.alpha_beta import AlphaBetaAI
from game.test_states import get_test_boards
from utils.logger import write_csv

DEPTHS = [1, 2, 3, 4]

def run_benchmark():
    rows = []
    for state_name, board in get_test_boards().items():
        for depth in DEPTHS:
            for alg_name, alg_cls in [("Minimax", MinimaxAI), ("Alpha-Beta", AlphaBetaAI)]:
                b = board.clone()
                ai = alg_cls(depth)
                start = time.perf_counter()
                result = ai.search(b, depth)
                elapsed = time.perf_counter() - start
                rows.append({
                    "Trang thai": state_name,
                    "Thuat toan": alg_name,
                    "Do sau": depth,
                    "Nuoc di": str(result.move),
                    "Diem danh gia": result.score,
                    "So trang thai da xet": result.nodes,
                    "Thoi gian (s)": round(elapsed, 6),
                })
                print(rows[-1])
    write_csv(RESULT_FILE, rows)
    print(f"Da ghi ket qua vao {RESULT_FILE}")

if __name__ == "__main__":
    run_benchmark()
