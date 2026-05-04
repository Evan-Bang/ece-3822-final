import time
import random
import string
import matplotlib.pyplot as plt
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.prefix_tree import prefix_tree
from datastructures.array import ArrayList

def generate_random_word(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def brute_force_find(word_list, prefix):
    """Simple linear scan through an array."""
    results = []
    for word in word_list:
        if word.startswith(prefix):
            results.append(word)
    return results

def run_prefix_benchmark():
    # Dataset sizes to test
    sizes = [1000, 5000, 10000, 20000, 40000]
    trie_times = []
    brute_times = []
    
    test_prefix = "app" # Prefix to search for

    for n in sizes:
        print(f"Testing N={n}...")
        
        # 1. Create Data
        raw_words = [generate_random_word() for _ in range(n)]
        # Ensure some matches exist
        raw_words.extend(["apple", "apply", "appointment", "appetite", "appreciate"])
        
        # 2. Build Trie
        trie = prefix_tree()
        for w in raw_words:
            trie.add_word(w)
            
        # 3. Benchmark Brute Force
        start_brute = time.perf_counter()
        _ = brute_force_find(raw_words, test_prefix)
        end_brute = time.perf_counter()
        brute_times.append(end_brute - start_brute)
        
        # 4. Benchmark Trie
        start_trie = time.perf_counter()
        _ = trie.find_words(test_prefix)
        end_trie = time.perf_counter()
        trie_times.append(end_trie - start_trie)

    # --- Plotting Results ---
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, brute_times, 'ro-', label="Brute Force (Linear Scan)")
    plt.plot(sizes, trie_times, 'bo-', label="Prefix Tree")
    
    plt.title("Search Performance: Trie vs. Brute Force Array")
    plt.xlabel("Number of Words in Dataset")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.savefig("prefix_comparison.png")
    print("\n Benchmark complete. Graph saved as 'prefix_comparison.png'")
    plt.show()

if __name__ == "__main__":
    run_prefix_benchmark()