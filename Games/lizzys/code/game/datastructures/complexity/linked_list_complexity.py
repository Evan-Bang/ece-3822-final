"""
linked_list_complexity.py - Analyze time complexity of Linked List operations

Measures actual performance of Linked List operations and compares to theoretical Big O.

Author: Emmanuel Morales
Date: March 31st, 2026
Lab: Lab 5 - NPC Patrol Paths with Linked Lists
"""

import sys
sys.path.append('../..')
from datastructures.stack import Stack
from datastructures.array import ArrayList
from datastructures.waypoint import Waypoint
from datastructures.patrol_path import PatrolPath
import time
import matplotlib.pyplot as plt
import numpy as np
import tracemalloc

def time_complexity_add_waypoint():
    """
    Measure time complexity of PatrolPath.add_waypoint() by timing it for increasing n and plotting results.
    """
    print("Time Complexity of PatrolPath.add_waypoint()")
    iters = 100
    total_time = 0
    times = ArrayList()
    ns = [10, 25, 50, 100, 200, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000, 75000, 100000]
    for n in ns:
        for i in range(iters):
            # measure time to add n waypoints to a new PatrolPath
            path = PatrolPath(patrol_type="one_way")
            start_time = time.perf_counter()
            for j in range(n):
                path.add_waypoint(n, n, wait_time=n)
            end_time = time.perf_counter()
            # how long did it take to add n waypoints?
            total_time += (end_time - start_time)
        times.append(total_time/iters) # store average time per iteration
        print("n:", n, "\t", f"Execution time: {total_time / iters:.6f} seconds")
        total_time = 0

    # Plot results
    plt.figure(1)
    plt.plot(ns, times, label="add_waypoint() time")

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
    plt.title("Time Complexity of PatrolPath.add_waypoint()")


def time_complexity_get_next_waypoint():
    """
    Measure time complexity of PatrolPath.get_next_waypoint() by timing it for increasing n and plotting results.
    """
    print("Time Complexity of PatrolPath.get_next_waypoint()")
    iters = 100
    total_time = 0
    times = ArrayList()
    ns = [10, 25, 50, 100, 200, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000, 75000, 100000]
    for n in ns:
        for i in range(iters):
            # add n waypoints to a new PatrolPath
            path = PatrolPath(patrol_type="one_way")
            for j in range(n):
                path.add_waypoint(n, n, wait_time=n)
            # measure time to get next waypoint n times
            start_time = time.perf_counter()
            for j in range(n):
                path.get_next_waypoint()
            end_time = time.perf_counter()
            # how long did it take to get next waypoint n times?
            total_time += (end_time - start_time)
        times.append(total_time/iters) # store average time per iteration
        print("n:", n, "\t", f"Execution time: {total_time / iters:.6f} seconds")
        total_time = 0

    # Plot results
    plt.figure(2)
    plt.plot(ns, times, label="get_next_waypoint() time")

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
    plt.title("Time Complexity of PatrolPath.get_next_waypoint()")

def space_complexity_add_waypoint():
    """
    Measure space complexity of PatrolPath.add_waypoint() by tracking memory usage for increasing n and plotting results.
    """
    print("Space Complexity of PatrolPath.add_waypoint()")
    iters = 100
    total_peak = 0
    ns = [10, 25, 50, 100, 200, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000, 75000, 100000]
    space_list = ArrayList()
    for n in ns:
        for i in range(iters):
            # measure memory used to add n waypoints to a new PatrolPath
            tracemalloc.start()
            path = PatrolPath(patrol_type="one_way")
            for j in range(n):
                path.add_waypoint(n, n, wait_time=n)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            total_peak += peak
        space_list.append(total_peak/iters) # store average memory usage per iteration
        print("n:", n, "\t", f"Memory: {(total_peak / iters)/ 1e6:.6f} MB")
        total_peak = 0

    # Plot results
    plt.figure(3)
    plt.plot(ns, space_list, label="add_waypoint() space")

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
    plt.title("Space Complexity of PatrolPath.add_waypoint()")

def space_complexity_get_next_waypoint():
    """
    Measure space complexity of PatrolPath.get_next_waypoint() by tracking memory usage for increasing n and plotting results.
    """
    print("Space Complexity of PatrolPath.get_next_waypoint()")
    iters = 100
    total_peak = 0
    ns = [10, 25, 50, 100, 200, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000, 75000, 100000]
    space_list = ArrayList()
    for n in ns:
        for i in range(iters):
            path = PatrolPath(patrol_type="one_way")
            for j in range(n):
                path.add_waypoint(n, n, wait_time=n)
            # measure memory used to get next waypoint n times
            tracemalloc.start()
            for j in range(n):
                path.get_next_waypoint()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            total_peak += peak
        space_list.append(total_peak/iters) # store average memory usage per iteration
        print("n:", n, "\t", f"Memory: {(total_peak / iters)/ 1e6:.6f} MB")
        total_peak = 0

    # Plot results
    plt.figure(4)
    plt.plot(ns, space_list, label="get_next_waypoint() space")

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
    plt.title("Space Complexity of PatrolPath.get_next_waypoint()")

def show_all_plots():
    plt.show()

def run_all_analysis():
    """Run all complexity analysis"""
    print("="*50)
    print("Running Complexity Analysis...")
    print("="*50)
    
    time_complexity_add_waypoint()
    time_complexity_get_next_waypoint()
    space_complexity_add_waypoint()
    space_complexity_get_next_waypoint()
    
    print("="*50)
    print("✓ COMPLETED COMPLEXITY ANALYSIS!")
    print("="*50)

if __name__ == "__main__":
    timer = time.time()
    run_all_analysis()
    print(f"Total run time = {time.time() - timer:.2f} seconds")
    show_all_plots()