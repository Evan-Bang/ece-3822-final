import time
import random
import string
import matplotlib.pyplot as plt
import numpy as np
import os 
import sys
from pathlib import Path

# Adjusting paths for your specific environment
sys.path.append(str(Path(__file__).resolve().parents[3]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

try:
    from platform_server.code.leaderboard import Leaderboard
except ImportError:
    print("Error: Could not import Leaderboard. Please check your import paths.")

# -----------------------------
# Helper: generate fake UUIDs
# -----------------------------
def make_uuid(k=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))

# -----------------------------
# Benchmark utilities (Per-Operation)
# -----------------------------
def measure_add_complexity(n):
    lb = Leaderboard()
    uuids = [make_uuid() for _ in range(n)]
    scores = [random.randint(0, 10_000) for _ in range(n)]

    start = time.perf_counter()
    for u, s in zip(uuids, scores):
        lb.add_score(u, s)
    end = time.perf_counter()
    
    # Return average time per single addition
    return (end - start) / n

def measure_sort_complexity(n):
    lb = Leaderboard()
    for _ in range(n):
        lb.add_score(make_uuid(), random.randint(0, 10_000))

    # We measure the full sort once for this N
    start = time.perf_counter()
    lb.get_all_sorted()
    end = time.perf_counter()
    
    return end - start

def measure_lookup_complexity(n):
    lb = Leaderboard()
    uuids = [make_uuid() for _ in range(n)]
    for u in uuids:
        lb.add_score(u, random.randint(0, 10_000))

    # Sample 1000 lookups to get a stable average
    sample_size = 1000
    sample_keys = random.choices(uuids, k=sample_size)

    start = time.perf_counter()
    for k in sample_keys:
        lb.get_player_score(k)
    end = time.perf_counter()

    # Return average time per single lookup
    return (end - start) / sample_size

# -----------------------------
# Run experiments
# -----------------------------
def run_experiments():
    # Larger range helps distinguish O(log n) from O(1)
    sizes = [100, 500, 1000, 2000, 4000, 8000, 16000]

    add_per_op = []
    sort_total = []
    lookup_per_op = []

    for n in sizes:
        print(f"Benchmarking N={n}...")
        add_per_op.append(measure_add_complexity(n))
        sort_total.append(measure_sort_complexity(n))
        lookup_per_op.append(measure_lookup_complexity(n))

    return sizes, add_per_op, sort_total, lookup_per_op

# -----------------------------
# Plot results
# -----------------------------
def plot_results(sizes, add_t, sort_t, lookup_t):
    s = np.array(sizes)
    plt.figure(figsize=(12, 8))

    # Plot Actual Data
    plt.plot(s, add_t, 'ro-', label="add_score (avg per op)")
    plt.plot(s, sort_t, 'go-', label="get_all_sorted (total)")
    plt.plot(s, lookup_t, 'bo-', label="get_player_score (avg per op)")

    # --- Add Reference Lines for Comparison ---
    # O(1) Reference (Horizontal line)
    plt.plot(s, [add_t[0]] * len(s), '--', color='gray', alpha=0.5, label="O(1) Trend")

    # O(N log N) Reference (Expected for sorting)
    # We scale it to match the starting point of the sort data
    expected_nlogn = s * np.log2(s)
    scale_factor = sort_t[0] / (s[0] * np.log2(s[0]))
    plt.plot(s, expected_nlogn * scale_factor, ':', color='green', alpha=0.5, label="O(N log N) Trend")

    # Formatting
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Number of players (N)")
    plt.ylabel("Time (seconds)")
    plt.title("Leaderboard Complexity Analysis (Log-Log Scale)")
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)

    print("\nPlotting complete. Saving to leaderboard_complexity.png")
    plt.savefig("leaderboard_complexity.png")
    plt.show()

if __name__ == "__main__":
    sizes, add_t, sort_t, lookup_t = run_experiments()
    plot_results(sizes, add_t, sort_t, lookup_t)