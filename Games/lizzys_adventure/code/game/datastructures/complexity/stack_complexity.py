"""
stack_complexity.py - Analyze time complexity of Stack operations

Measures actual performance of Stack operations and compares to theoretical Big O.

Author: Emmanuel Morales
Date: February 19, 2026
Lab: Lab 4 - Time Travel with Stacks
"""

import sys
sys.path.append('../..')
from datastructures.stack import Stack
from datastructures.array import ArrayList
import time
import matplotlib.pyplot as plt
import numpy as np


def time_complexity_push():
    """
    Measure time complexity of Stack.push() by timing it for increasing n and plotting results.
    """
    print("Time Complexity of Stack.push()")
    iters = 100
    total_time = 0
    times = ArrayList()
    ns = [10, 25, 50, 100, 200, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    for n in ns:
        for i in range(iters):
            test_stack = Stack(1)
            for j in range(n):
                start_time = time.perf_counter()
                test_stack.push(j)
                end_time = time.perf_counter()
                total_time += (end_time - start_time)
        print("n:", n, "\t", f"Execution time: {total_time / iters:.6f} seconds")
        times.append(total_time/iters)
        total_time = 0
    
    # Plot results
    plt.figure(1)
    plt.plot(ns, times, label="push() time")

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
    plt.title("Time Complexity of Stack.push()")

def time_complexity_pop():
    """
    Measure time complexity of Stack.pop() by timing it for increasing n and plotting results.
    """
    print("Time Complexity of Stack.pop()")
    iters = 100
    total_time = 0
    times = ArrayList()
    ns = ns = [10, 25, 50, 100, 200, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    for n in ns:
        for i in range(iters):
            test_stack = Stack(n)
            for j in range(n):
                test_stack.push(j)
            for j in range(n):
                start_time = time.perf_counter()
                test_stack.pop()
                end_time = time.perf_counter()
                total_time += (end_time - start_time)
        print("n:", n, "\t", f"Execution time: {total_time / iters:.6f} seconds")
        times.append(total_time/iters)
        total_time = 0

    # Plot results
    plt.figure(2)
    plt.plot(ns, times, label="pop() time")

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
    plt.title("Time Complexity of Stack.pop()")

def space_complexity_push():
    """
    Measure space complexity of Stack.push() by tracking memory usage for increasing n and plotting results.
    """
    print("Space Complexity of Stack.push()")
    iters = 100
    total_peak = 0
    ns = [10, 25, 50, 100, 200, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    space_list = ArrayList()
    for n in ns:
        for i in range(iters):
            test_stack = Stack(1)
            for j in range(n):
                test_stack.push(j)
            m = sys.getsizeof(test_stack) # memory usage of stack
            total_peak += m
        print("n:", n, "\t", f"Memory: {(total_peak / iters)/ 1e6:.6f} MB")
        space_list.append(total_peak / iters)
        total_peak = 0
    
    # Plot results
    plt.figure(3)
    plt.plot(ns, space_list, label="push() space")

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
    plt.title("Space Complexity of Stack.push()")

def space_complexity_pop():
    """
    Measure space complexity of Stack.pop() by tracking memory usage for increasing n and plotting results.
    """
    print("Space Complexity of Stack.pop()")
    iters = 100
    total_peak = 0
    ns = ns = [10, 25, 50, 100, 200, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    space_list = ArrayList()
    for n in ns:
        for i in range(iters):
            test_stack = Stack(n)
            for j in range(n):
                test_stack.push(j)
            for j in range(n):
                test_stack.pop()
            m = sys.getsizeof(test_stack) # memory usage of stack
            total_peak += m
        print("n:", n, "\t", f"Memory: {(total_peak / iters)/ 1e6:.6f} MB")
        space_list.append(total_peak / iters)
        total_peak = 0
    
    # Plot results
    plt.figure(4)
    plt.plot(ns, space_list, label="pop() space")

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
    plt.title("Space Complexity of Stack.pop()")

def show_all_plots():
    plt.show()

def run_all_analysis():
    """Run all complexity analysis"""
    print("="*50)
    print("Running Complexity Analysis...")
    print("="*50)
    
    time_complexity_push()
    time_complexity_pop()
    space_complexity_push()
    space_complexity_pop()
    
    print("="*50)
    print("✓ COMPLETED COMPLEXITY ANALYSIS!")
    print("="*50)

if __name__ == "__main__":
    timer = time.time()
    run_all_analysis()
    print(f"Total run time = {time.time() - timer:.2f} seconds")
    show_all_plots()