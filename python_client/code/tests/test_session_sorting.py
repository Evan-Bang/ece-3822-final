import time
import random
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Path & Module Ghosting
# ---------------------------------------------------------
current_file = Path(__file__).resolve()
CODE_DIR = str(current_file.parents[1]) 
PROJECT_ROOT = str(current_file.parents[3])

sys.path.insert(0, CODE_DIR)
sys.path.insert(0, PROJECT_ROOT)

mock_psh = MagicMock()
sys.modules["python_server_handler"] = mock_psh

# ---------------------------------------------------------
# 2. Imports
# ---------------------------------------------------------
try:
    from session_handler import SessionHandler
    from datastructures.array import ArrayList
    from datastructures.hash_table import HashTable
    print("✅ Success: All modules and data structures loaded.")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# ---------------------------------------------------------
# 3. Mock Data Logic
# ---------------------------------------------------------
class MockUserData:
    def __init__(self, handler):
        self.handler = handler
    def get_user_data(self, username):
        return {
            "success": True,
            "user_data": {
                "sessions": [
                    {"GAME": "Asteroids", "SCORE": 500,  "PLAYTIME": 120, "DATE": "2026-04-01"},
                    {"GAME": "Snake",     "SCORE": 1200, "PLAYTIME": 300, "DATE": "2026-04-02"},
                    {"GAME": "Asteroids", "SCORE": 2500, "PLAYTIME": 450, "DATE": "2026-04-03"},
                    {"GAME": "Tetris",    "SCORE": 800,  "PLAYTIME": 180, "DATE": "2026-04-04"},
                    {"GAME": "Snake",     "SCORE": 600,  "PLAYTIME": 90,  "DATE": "2026-04-05"},
                ]
            }
        }

mock_psh.UserData = MockUserData

# ---------------------------------------------------------
# 4. Benchmarking Functions
# ---------------------------------------------------------
def run_functional_checks():
    print("\n--- Running Functional Checks ---")
    sh = SessionHandler(MagicMock())
    sh.load("test_user")
    print(f"Total Sessions: {sh.total_sessions}")
    print(f"Best Score: {sh.best_score}")
    asteroids = sh.get_sessions(game="Asteroids")
    print(f"Filtering check: {len(asteroids)} Asteroids sessions found.")

def test_sorting_complexity(sizes):
    print("\n--- Benchmarking Merge Sort (O(n log n)) ---")
    sh = SessionHandler(MagicMock())
    sort_times = []
    for n in sizes:
        sh.sessions = ArrayList()
        for _ in range(n):
            s = HashTable()
            s.set("score", random.randint(0, 10000))
            sh.sessions.append(s)
        start = time.perf_counter()
        sh.sort_sessions(key="score", descending=True)
        elapsed = time.perf_counter() - start
        sort_times.append(elapsed)
        print(f"Sorted {n:5} items in {elapsed:.5f}s")
    return sort_times

def test_filtering_complexity(sizes):
    print("\n--- Benchmarking Linear Filter (O(n)) ---")
    sh = SessionHandler(MagicMock())
    filter_times = []
    for n in sizes:
        sh.sessions = ArrayList()
        for _ in range(n):
            s = HashTable()
            s.set("game", random.choice(["Asteroids", "Snake", "Tetris"]))
            sh.sessions.append(s)
        start = time.perf_counter()
        # Linear scan through all sessions
        _ = sh.get_sessions(game="Asteroids")
        elapsed = time.perf_counter() - start
        filter_times.append(elapsed)
        print(f"Filtered {n:5} items in {elapsed:.5f}s")
    return filter_times

# ---------------------------------------------------------
# 5. Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    run_functional_checks()
    
    # Shared sizes for direct comparison
    test_sizes = [100, 500, 1000, 2000, 4000, 6000]
    
    s_times = test_sorting_complexity(test_sizes)
    f_times = test_filtering_complexity(test_sizes)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    
    # Sorting plot (Log-Linear)
    plt.plot(test_sizes, s_times, 'go-', linewidth=2, label=r"Merge Sort $O(n \log n)$")
    
    # Filtering plot (Linear)
    plt.plot(test_sizes, f_times, 'bo-', linewidth=2, label=r"Filter $O(n)$")
    
    plt.xlabel("Number of Sessions (N)")
    plt.ylabel("Time (seconds)")
    plt.title("Session Operation Time Complexity")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    plt.savefig("sorting_vs_filtering.png")
    print("\n📈 Comparison graph saved as 'sorting_vs_filtering.png'")
    plt.show()