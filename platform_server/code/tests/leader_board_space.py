import sys
import random
import string
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Adjusting paths
sys.path.append(str(Path(__file__).resolve().parents[3]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

try:
    from platform_server.code.leaderboard import Leaderboard
except ImportError:
    print("Error: Could not import Leaderboard.")

def make_uuid(k=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))

# -----------------------------
# Space Measurement Utility
# -----------------------------
def get_deep_size(obj, seen=None):
    """
    Recursively finds the size of objects. 
    Important for custom classes like Leaderboard that hold other data structures.
    """
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)

    if isinstance(obj, dict):
        size += sum([get_deep_size(v, seen) for v in obj.values()])
        size += sum([get_deep_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_deep_size(vars(obj), seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_deep_size(i, seen) for i in obj])
    return size

def measure_space_complexity(n):
    lb = Leaderboard()
    uuids = [make_uuid() for _ in range(n)]
    scores = [random.randint(0, 10_000) for _ in range(n)]

    for u, s in zip(uuids, scores):
        lb.add_score(u, s)
    
    # Measure total memory footprint of the leaderboard object in bytes
    total_bytes = get_deep_size(lb)
    
    # Return size in Kilobytes for better readability
    return total_bytes / 1024

# -----------------------------
# Run Experiments
# -----------------------------
def run_space_experiments():
    # Linear growth in N
    sizes = [100, 500, 1000, 2000, 4000, 8000, 16000, 32000]
    memory_usage_kb = []

    for n in sizes:
        print(f"Measuring Space for N={n}...")
        memory_usage_kb.append(measure_space_complexity(n))

    return sizes, memory_usage_kb

# -----------------------------
# Plot Results
# -----------------------------
def plot_space_results(sizes, memory_kb):
    s = np.array(sizes)
    m = np.array(memory_kb)
    
    plt.figure(figsize=(10, 6))

    # Plot Actual Memory Usage
    plt.plot(s, m, 'mo-', label="Leaderboard Memory Usage (KB)")

    # --- Add Reference Line for O(N) ---
    # Memory should grow linearly with the number of players
    slope = (m[-1] - m[0]) / (s[-1] - s[0])
    intercept = m[0] - slope * s[0]
    plt.plot(s, slope * s + intercept, '--', color='gray', alpha=0.5, label="O(N) Linear Trend")

    plt.xlabel("Number of players (N)")
    plt.ylabel("Memory Usage (KB)")
    plt.title("Leaderboard Space Complexity Analysis")
    plt.legend()
    plt.grid(True, ls="-", alpha=0.2)

    print("\nPlotting complete. Saving to leaderboard_space.png")
    plt.savefig("leaderboard_space.png")
    plt.show()

if __name__ == "__main__":
    sizes, memory_kb = run_space_experiments()
    plot_space_results(sizes, memory_kb)