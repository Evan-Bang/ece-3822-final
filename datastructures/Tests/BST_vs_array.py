import time
import random
import matplotlib.pyplot as plt
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.BST import BST
from datastructures.array import ArrayList

# Assuming these are your class names
from datastructures.BST import BST 
from datastructures.array import ArrayList

def brute_force_range(array_list, low, high):
    """Linear scan to find elements within range."""
    results = ArrayList()
    for i in range(len(array_list)):
        val = array_list[i]
        if low <= val <= high:
            results.append(val)
    return results

def run_range_benchmark():
    sizes = [1000, 5000, 10000, 20000, 40000]
    bst_times = []
    array_times = []
    
    # We will search for a fixed-width range in the middle
    lower_bound = 4500
    upper_bound = 5500

    for n in sizes:
        print(f"Testing N={n}...")
        
        # Create data
        data = [random.randint(0, 10000) for _ in range(n)]
        
        # Build BST
        tree = BST()
        for x in data:
            tree.insert(x)
            
        # Build ArrayList
        arr = ArrayList()
        for x in data:
            arr.append(x)
            
        # 1. Benchmark Array 
        start_arr = time.perf_counter()
        test = brute_force_range(arr, lower_bound, upper_bound)
        array_times.append(time.perf_counter() - start_arr)
        
        # 2. Benchmark BST Range Search
        start_bst = time.perf_counter()
        test = tree.range_query(lower_bound, upper_bound)
        bst_times.append(time.perf_counter() - start_bst)

    # --- Plotting ---
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, array_times, 'ro-', label="Dynamic Array (Linear Scan)")
    plt.plot(sizes, bst_times, 'go-', label="BST")
    
    plt.title("Range Search Performance: BST vs. Dynamic Array")
    plt.xlabel("Number of Elements (N)")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.savefig("bst_vs_array_range.png")
    print("\n Graph saved as 'bst_vs_array_range.png'")
    plt.show()

if __name__ == "__main__":
    run_range_benchmark()