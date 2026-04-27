"""
array_complexity.py - Complexity Analysis of Dynamic Array Implementation 
    
Author: Emmanuel Morales
Date: February 10, 2026
Lab: Lab 3 - ArrayList and Inventory System
"""

import sys
sys.path.append('../..')
from datastructures.array import ArrayList
import time as time
import matplotlib.pyplot as plt
import numpy as np
import tracemalloc

def time_complexity_append():
    print("Time Complexity of ArrayList.append()")
    iters = 100
    total_time = 0
    times = ArrayList()
    ns = [10, 25, 50, 100, 200, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000, 75000, 100000]
    for n in ns:
        for i in range(iters):
            test_array = ArrayList(1)
            start_time = time.perf_counter()
            for j in range(n):
                test_array.append(j)
            end_time = time.perf_counter()
            total_time += (end_time - start_time)
        times.append(total_time/iters)        
        print("n:", n, "\t", f"Execution time: {total_time / iters:.6f} seconds")
        total_time = 0
    
    # Plot results
    plt.figure(1)
    plt.plot(ns, times, label="append() time")

    # Plot reference lines
    ns_ref = np.array(ns)
    min_times = min(times) # reference time for O(1)
    o1 = np.ones_like(ns_ref) # O(1)
    olog = np.log(ns_ref / ns_ref[0])  # O(log n)
    on = (ns_ref / ns_ref[0])  # O(n)
    onlogn = olog * on # O(n log n)
    onn = (ns_ref / ns_ref[0]) **2 # O(n^2)
    plt.plot(ns_ref, o1  * min_times    , label="O(1)"       , linestyle="dashed")
    plt.plot(ns_ref, olog * min_times   , label="O(log n)"   , linestyle="dashed")
    plt.plot(ns_ref, on  * min_times    , label="O(n)"       , linestyle="dashed")
    plt.plot(ns_ref, onlogn * min_times , label="O(n log n)" , linestyle="dashed")
    plt.plot(ns_ref, onn * min_times    , label="O(n^2)"     , linestyle="dashed")
    plt.xscale("log")
    plt.yscale("log")


    # Labels and title
    plt.xlabel("n")
    plt.ylabel("average time")
    plt.legend()
    plt.title("Time Complexity of ArrayList.append()")

def time_complexity_insert():
    print("Time Complexity of ArrayList.insert()")
    iters = 100
    total_time = 0
    times = ArrayList()
    ns = [10, 25, 50, 100, 200, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 5000]
    for n in ns:
        for i in range(iters):
            test_array = ArrayList(1)
            start_time = time.perf_counter()
            for j in range(n):
                test_array.insert(0, j)
            end_time = time.perf_counter()
            total_time += (end_time - start_time)
        times.append(total_time/iters)
        print("n:", n, "\t", f"Execution time: {total_time / iters:.6f} seconds")
        total_time = 0
    
    # Plot results
    plt.figure(2)
    plt.plot(ns, times, label="insert() time")

    # Plot reference lines
    ns_ref = np.array(ns)
    min_times = min(times) # reference time for O(1)
    o1 = np.ones_like(ns_ref) # O(1)
    olog = np.log(ns_ref / ns_ref[0])  # O(log n)
    on = (ns_ref / ns_ref[0])  # O(n)
    onlogn = olog * on # O(n log n)
    onn = (ns_ref / ns_ref[0]) **2 # O(n^2)
    plt.plot(ns_ref, o1  * min_times    , label="O(1)"       , linestyle="dashed")
    plt.plot(ns_ref, olog * min_times   , label="O(log n)"   , linestyle="dashed")
    plt.plot(ns_ref, on  * min_times    , label="O(n)"       , linestyle="dashed")
    plt.plot(ns_ref, onlogn * min_times , label="O(n log n)" , linestyle="dashed")
    plt.plot(ns_ref, onn * min_times    , label="O(n^2)"     , linestyle="dashed")
    plt.xscale("log")
    plt.yscale("log")


    # Labels and title
    plt.xlabel("n")
    plt.ylabel("average time")
    plt.legend()
    plt.title("Time Complexity of ArrayList.insert()")

def space_complexity_append():
    print("Space Complexity of ArrayList.append()")
    iters = 100
    total_peak = 0
    ns = [10, 25, 50, 100, 200, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000, 75000, 100000]
    space_list = ArrayList()
    for n in ns:
        for i in range(iters):
            tracemalloc.start()
            test_array = ArrayList(1)
            for j in range(n):
                test_array.append(j)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            total_peak += peak
        space_list.append(total_peak / iters)
        print("n:", n, "\t", f"Memory: {(total_peak / iters)/ 1e6:.4f} MB")
        total_peak = 0
    
    # Plot results
    plt.figure(3)
    plt.plot(ns, space_list, label="append() space")

    # Plot reference lines
    ns_ref = np.array(ns)
    min_space_list = min(space_list) # reference time for O(1)
    o1 = np.ones_like(ns_ref) # O(1)
    olog = np.log(ns_ref / ns_ref[0])  # O(log n)
    on = (ns_ref / ns_ref[0])  # O(n)
    onlogn = olog * on # O(n log n)
    onn = (ns_ref / ns_ref[0]) **2 # O(n^2)
    plt.plot(ns_ref, o1  * min_space_list    , label="O(1)"       , linestyle="dashed")
    plt.plot(ns_ref, olog * min_space_list   , label="O(log n)"   , linestyle="dashed")
    plt.plot(ns_ref, on  * min_space_list    , label="O(n)"       , linestyle="dashed")
    plt.plot(ns_ref, onlogn * min_space_list , label="O(n log n)" , linestyle="dashed")
    plt.plot(ns_ref, onn * min_space_list    , label="O(n^2)"     , linestyle="dashed")
    plt.xscale("log")
    plt.yscale("log")

    # Labels and title
    plt.xlabel("n")
    plt.ylabel("Memory (MB)")
    plt.legend()
    plt.title("Space Complexity of ArrayList.append()")

def space_complexity_insert():
    print("Space Complexity of ArrayList.insert()")
    iters = 100
    total_peak = 0
    ns = [10, 25, 50, 100, 200, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 5000]
    space_list = ArrayList()
    for n in ns:
        for i in range(iters):
            tracemalloc.start()
            test_array = ArrayList(1)
            for j in range(n):
                test_array.insert(j, j)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            total_peak += peak
        space_list.append(total_peak / iters)
        print("n:", n, "\t", f"Memory: {(total_peak / iters)/ 1e6:.4f} MB")
        total_peak = 0
    
    # Plot results
    plt.figure(4)
    plt.plot(ns, space_list, label="insert() space")

    # Plot reference lines
    ns_ref = np.array(ns)
    min_space_list = min(space_list) # reference time for O(1)
    o1 = np.ones_like(ns_ref) # O(1)
    olog = np.log(ns_ref / ns_ref[0])  # O(log n)
    on = (ns_ref / ns_ref[0])  # O(n)
    onlogn = olog * on # O(n log n)
    onn = (ns_ref / ns_ref[0]) **2 # O(n^2)
    plt.plot(ns_ref, o1  * min_space_list    , label="O(1)"       , linestyle="dashed")
    plt.plot(ns_ref, olog * min_space_list   , label="O(log n)"   , linestyle="dashed")
    plt.plot(ns_ref, on  * min_space_list    , label="O(n)"       , linestyle="dashed")
    plt.plot(ns_ref, onlogn * min_space_list , label="O(n log n)" , linestyle="dashed")
    plt.plot(ns_ref, onn * min_space_list    , label="O(n^2)"     , linestyle="dashed")
    plt.xscale("log")
    plt.yscale("log")


   # Labels and title
    plt.xlabel("n")
    plt.ylabel("Memory (MB)")
    plt.legend()
    plt.title("Space Complexity of ArrayList.insert()")

def show_all_plots():
    plt.show()

def run_all_analysis():
    """Run all complexity analysis"""
    print("="*50)
    print("Running Complexity Analysis...")
    print("="*50)
    
    time_complexity_append()
    time_complexity_insert()
    space_complexity_append()
    space_complexity_insert()
    
    print("="*50)
    print("✓ COMPLETED COMPLEXITY ANALYSIS!")
    print("="*50)

if __name__ == "__main__":
    timer = time.time()
    run_all_analysis()
    print(f"Total run time = {time.time() - timer:.2f} seconds")
    show_all_plots()