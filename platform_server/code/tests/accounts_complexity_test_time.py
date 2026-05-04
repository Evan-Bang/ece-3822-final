import random
import string
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import shutil
import sys
import tracemalloc
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

try:
    import platform_server.code.accounts as accounts_mod
    from platform_server.code.accounts import AccountManager
except ImportError:
    print("Error: Could not import AccountManager. Please check your import paths.")
    sys.exit(1)

# -----------------------------
# Configuration
# -----------------------------
TEST_DATA_DIR = "./test_user_data"

def setup_test_folder():
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)
    os.makedirs(TEST_DATA_DIR)
    with open(os.path.join(TEST_DATA_DIR, "name_id.json"), "w") as f:
        f.write("{}")

def bytes_to_kb(b):
    return b / 1024

# -----------------------------
# Space Benchmarking Logic
# -----------------------------
def run_space_benchmark(sizes):
    """
    Measures peak memory (KB) consumed by each operation type:
      - Account Creation : peak heap during bulk create
      - Authentication   : peak heap during bulk auth (50 samples)
      - Prefix Search    : peak heap during bulk prefix search (100 samples)
      - Manager Object   : baseline heap of the populated AccountManager itself
    """
    create_mem   = []   # KB — peak during creation phase
    auth_mem     = []   # KB — peak during auth phase
    prefix_mem   = []   # KB — peak during prefix-search phase
    manager_mem  = []   # KB — heap held by the manager after N accounts loaded

    original_path = accounts_mod.user_data_path

    try:
        accounts_mod.user_data_path = TEST_DATA_DIR

        for n in sizes:
            print(f"Testing N={n}...")
            setup_test_folder()

            names = [
                ''.join(random.choices(string.ascii_lowercase, k=10))
                for _ in range(n)
            ]

            # ── 1. Account Creation ──────────────────────────────────────────
            manager = AccountManager()
            tracemalloc.start()
            for name in names:
                manager.create_account(name, "pass")
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            create_mem.append(bytes_to_kb(peak))

            # ── 2. Manager Object Size (after N accounts) ────────────────────
            # Re-instantiate so we measure a clean load, not creation overhead
            tracemalloc.start()
            loaded_manager = AccountManager()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            # current reflects the live heap of the loaded manager
            manager_mem.append(bytes_to_kb(current))

            # ── 3. Authentication (50 samples) ───────────────────────────────
            sample_size = min(n, 50)
            tracemalloc.start()
            for name in names[:sample_size]:
                loaded_manager.authenticate(name, "pass")
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            auth_mem.append(bytes_to_kb(peak))

            # ── 4. Prefix Search (100 samples) ───────────────────────────────
            search_samples = [name[:2] for name in random.choices(names, k=100)]
            tracemalloc.start()
            for pref in search_samples:
                loaded_manager.prefix_search_account(pref)
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            prefix_mem.append(bytes_to_kb(peak))

    finally:
        accounts_mod.user_data_path = original_path
        if os.path.exists(TEST_DATA_DIR):
            shutil.rmtree(TEST_DATA_DIR)

    return create_mem, auth_mem, prefix_mem, manager_mem

# -----------------------------
# Plotting
# -----------------------------
def plot_space_results(sizes, create_mem, auth_mem, prefix_mem, manager_mem):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("AccountManager — Space Complexity Analysis", fontsize=16, fontweight="bold")

    datasets = [
        (axes[0, 0], create_mem,  "Account Creation",  "#e74c3c"),
        (axes[0, 1], auth_mem,    "Authentication — 50 samples", "#3498db"),
        (axes[1, 0], prefix_mem,  "Prefix Search — 100 samples", "#2ecc71"),
        (axes[1, 1], manager_mem, "AccountManager object", "#9b59b6"),
    ]

    for ax, data, title, color in datasets:
        ax.plot(sizes, data, "o-", color=color, linewidth=2, markersize=6)
        ax.fill_between(sizes, data, alpha=0.15, color=color)

        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_xlabel("Number of Accounts (N)")
        ax.set_ylabel("Peak Memory (KB)")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)

    plt.tight_layout()
    out_path = "account_manager_space_complexity.png"
    plt.savefig(out_path, dpi=150)
    print(f"\nPlot saved → {out_path}")
    plt.show()


if __name__ == "__main__":
    test_sizes = [10, 50, 100, 250, 500, 1000, 2000, 5000]

    c_mem, a_mem, p_mem, m_mem = run_space_benchmark(test_sizes)

    plot_space_results(test_sizes, c_mem, a_mem, p_mem, m_mem)