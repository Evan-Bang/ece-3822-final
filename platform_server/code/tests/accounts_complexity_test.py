import time
import random
import string
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import tempfile
from pathlib import Path
import sys

# Adjusting paths for your specific environment
sys.path.append(str(Path(__file__).resolve().parents[3]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

try:
    import platform_server.code.accounts as accounts_mod
    from platform_server.code.accounts import AccountManager
except ImportError:
    print("Error: Could not import Leaderboard. Please check your import paths.")


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

# -----------------------------
# Benchmarking Logic
# -----------------------------
def run_benchmark(sizes):
    create_results = []
    auth_results = []
    prefix_results = []

    original_path = accounts_mod.user_data_path
    
    try:
        accounts_mod.user_data_path = TEST_DATA_DIR

        for n in sizes:
            print(f"Testing N={n}...")
            setup_test_folder() 
            manager = AccountManager()
            
            # Generate random names
            names = [''.join(random.choices(string.ascii_lowercase, k=10)) for _ in range(n)]
            
            # 1. Benchmark Creation
            start = time.perf_counter()
            for name in names:
                manager.create_account(name, "pass")
            create_results.append((time.perf_counter() - start) / n)

            # 2. Benchmark Authentication (Sample of 50)
            start = time.perf_counter()
            sample_size = min(n, 50)
            for name in names[:sample_size]:
                manager.authenticate(name, "pass")
            auth_results.append((time.perf_counter() - start) / sample_size)

            # 3. Benchmark Prefix Search
            # We search for the first 2 letters of 100 random users
            # This should be lightning fast because it's in-memory (Trie)
            search_samples = [name[:2] for name in random.choices(names, k=100)]
            start = time.perf_counter()
            for pref in search_samples:
                manager.prefix_search_account(pref)
            prefix_results.append((time.perf_counter() - start) / 100)

    finally:
        accounts_mod.user_data_path = original_path
        if os.path.exists(TEST_DATA_DIR):
            shutil.rmtree(TEST_DATA_DIR)

    return create_results, auth_results, prefix_results

# -----------------------------
# Plotting
# -----------------------------
def plot_results(sizes, create_t, auth_t, prefix_t):
    plt.figure(figsize=(10, 6))
    
    plt.plot(sizes, create_t, 'ro-', label="Account Creation (Disk/Hash)")
    plt.plot(sizes, auth_t, 'bo-', label="Authentication (Disk/Hash)")
    plt.plot(sizes, prefix_t, 'go-', label="Prefix Search")
    
    plt.xlabel("Number of Players (N)")
    plt.ylabel("Time per Operation (Seconds)")
    plt.title("AccountManager Complexity Analysis")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("account_manager_complexity.png")
    plt.show()

if __name__ == "__main__":
    # Increased sizes slightly to better show the Trie's advantage
    test_sizes = [10, 50, 100, 250, 500, 1000,2000, 5000]
    c_res, a_res, p_res = run_benchmark(test_sizes)
    plot_results(test_sizes, c_res, a_res, p_res)