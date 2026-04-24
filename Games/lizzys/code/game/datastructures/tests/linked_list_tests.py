"""
linked_list_tests.py - Test suite for Linked List implementation

Tests all Linked List methods with edge cases.

Author: Emmanuel Morales
Date: March 30th, 2026
Lab: Lab 5 NPC Patrol Paths with Linked Lists
"""

import sys
import math
sys.path.append('../..')
from datastructures.stack import Stack
from datastructures.array import ArrayList
from datastructures.waypoint import Waypoint
from datastructures.patrol_path import PatrolPath

def test_waypoint():
    """
    Test initialization, distance, pointers
    """
    print("Testing Waypoint...")    
    # Create a waypoint and check its attributes
    waypoint = Waypoint(10, 22, wait_time=3)
    assert waypoint.x == 10, "Waypoint x coordinate should be 10"
    assert waypoint.y == 22, "Waypoint y coordinate should be 22"
    assert waypoint.wait_time == 3, "Waypoint wait_time should be 3"
    assert waypoint.next is None, "Waypoint next should be None"
    assert waypoint.prev is None, "Waypoint prev should be None"
    
    # Test distance calculation
    distance = waypoint.distance_to(15, 24)
    expected_distance = math.sqrt((15 - 10) ** 2 + (24 - 22) ** 2)
    assert abs(distance - expected_distance) < 1e-6



    print("✓ Waypoint works correctly!")


def test_patrol_path_basic():
    """
    Test adding waypoints to a PatrolPath
    """
    print("Testing PatrolPath initializations...")
    
    # Create a one-way patrol path
    path = PatrolPath(patrol_type="one_way")

    # Check that patrol path is empty
    assert path.size == 0, "PatrolPath size should be 0 when initialized"
    assert path.is_empty(), "PatrolPath should be empty when initialized"

    # Add waypoints to the patrol path
    path.add_waypoint(1, 1, wait_time=1)
    path.add_waypoint(3, 3, wait_time=2)
    path.add_waypoint(5, 7, wait_time=3)
    path.add_waypoint(0, 0, wait_time=4)

    # Check the size of the patrol path
    assert path.size == 4, "PatrolPath size should be 4"
    assert not path.is_empty(), "PatrolPath should not be empty after adding waypoints"

    # Check the head and tail waypoints
    assert path.head.x == 1 and path.head.y == 1, "Head waypoint should be at (1, 1)"
    assert path.head.wait_time == 1, "Head waypoint wait_time should be 1"
    assert path.tail.x == 0 and path.tail.y == 0, "Tail waypoint should be at (0, 0)"
    assert path.tail.wait_time == 4, "Tail waypoint wait_time should be 4"

    print("✓ One way PatrolPath initialized correctly!")

    # Create a circular patrol path
    path = PatrolPath(patrol_type="circular")
    path.add_waypoint(1, 1, wait_time=1)
    path.add_waypoint(3, 3, wait_time=2)
    path.add_waypoint(5, 7, wait_time=3)
    path.add_waypoint(0, 0, wait_time=4)
    
    # Check the size of the patrol path
    assert path.size == 4, "PatrolPath size should be 4"
    
    # Check the head and tail waypoints
    assert path.head.x == 1 and path.head.y == 1, "Head waypoint should be at (1, 1)"
    assert path.tail.x == 0 and path.tail.y == 0, "Tail waypoint should be at (0, 0)"

    # Check the circular linking
    assert path.tail.next == path.head, "Tail's next should point to head in circular patrol"
    assert path.head.prev == path.tail, "Head's prev should point to tail in circular patrol"
    
    print("✓ Circular PatrolPath initialized correctly!")

    print("✓ PatrolPath initializations work correctly!")

def test_patrol_path_one_way():
    """
    Test one-way patrol path traversal
    """
    print("Testing one-way PatrolPath traversal...")
    
    # Create a one-way patrol path and add waypoints
    path = PatrolPath(patrol_type="one_way")
    path.add_waypoint(1, 1, wait_time=1)
    path.add_waypoint(3, 3, wait_time=2)
    path.add_waypoint(5, 7, wait_time=3)
    path.add_waypoint(0, 0, wait_time=4)

    # Traverse the patrol path and check waypoints
    waypoints = [(1, 1), (3, 3), (5, 7), (0, 0)]
    for (wp_x, wp_y) in waypoints:
        waypoint = path.get_next_waypoint()
        assert waypoint.x == wp_x and waypoint.y == wp_y, f"Expected to see waypoint at ({wp_x}, {wp_y}), but instead got ({waypoint.x}, {waypoint.y})"

    # After traversing all waypoints, get_next_waypoint should return None
    assert path.get_next_waypoint() is None, "Expected None after traversing all waypoints in one-way patrol"

    print("✓ One-way PatrolPath traversal works correctly!")

def test_patrol_path_circular():
    """
    Test circular patrol path traversal
    """
    print("Testing circular PatrolPath traversal...")
    
    # Create a circular patrol path and add waypoints
    path = PatrolPath(patrol_type="circular")
    path.add_waypoint(1, 1, wait_time=1)
    path.add_waypoint(3, 3, wait_time=2)
    path.add_waypoint(5, 7, wait_time=3)
    path.add_waypoint(0, 0, wait_time=4)

    # Traverse the patrol path twice and check waypoints
    waypoints = [(1, 1), (3, 3), (5, 7), (0, 0)]
    for loops in range(2): # loop through twice
        for (wp_x, wp_y) in waypoints:
            waypoint = path.get_next_waypoint()
            assert waypoint.x == wp_x and waypoint.y == wp_y, f"Expected to see waypoint at ({wp_x}, {wp_y}), but instead got ({waypoint.x}, {waypoint.y})"

    print("✓ Circular PatrolPath traversal works correctly!")

def test_patrol_path_back_and_forth():
    """
    Test back-and-forth patrol path traversal
    """
    print("Testing back-and-forth PatrolPath traversal...")
    
    # Create a back-and-forth patrol path and add waypoints
    path = PatrolPath(patrol_type="back_and_forth")
    path.add_waypoint(1, 1, wait_time=1)
    path.add_waypoint(3, 3, wait_time=2)
    path.add_waypoint(5, 7, wait_time=3)
    path.add_waypoint(0, 0, wait_time=4)

    # Traverse forward through the patrol path
    waypoints_forward = [(1, 1), (3, 3), (5, 7), (0, 0)]
    for (wp_x, wp_y) in waypoints_forward:
        waypoint = path.get_next_waypoint()
        assert waypoint.x == wp_x and waypoint.y == wp_y, f"Expected to see waypoint at ({wp_x}, {wp_y}), but instead got ({waypoint.x}, {waypoint.y})"
    assert path.direction == -1, "Expected direction to be -1 when back-and-forth patrol path begins to backtrack"

    # Traverse backward through the patrol path
    waypoints_backward = [(5, 7), (3, 3), (1, 1)]
    for (wp_x, wp_y) in waypoints_backward:
        waypoint = path.get_next_waypoint()
        assert waypoint.x == wp_x and waypoint.y == wp_y, f"Expected to see waypoint at ({wp_x}, {wp_y}), but instead got ({waypoint.x}, {waypoint.y})"

    # After traversing back to the start, get_next_waypoint should return None
    assert path.get_next_waypoint() is None, "Expected None after traversing back to the start in back-and-forth patrol"

    print("✓ Back-and-forth PatrolPath traversal works correctly!")

def test_patrol_path_reset():
    """
    Test resetting the patrol path
    """
    print("Testing PatrolPath reset...")
    
    # Create a patrol path and add waypoints
    path = PatrolPath(patrol_type="circular")
    path.add_waypoint(1, 1, wait_time=1)
    path.add_waypoint(3, 3, wait_time=2)
    path.add_waypoint(5, 7, wait_time=3)
    path.add_waypoint(0, 0, wait_time=4)

    # Traverse part way through the patrol path
    path.get_next_waypoint() # (1, 1)
    path.get_next_waypoint() # (3, 3)
    assert path.current.x == 5 and path.current.y == 7, "Expected current waypoint to be at (5, 7) before reset"

    # Reset the patrol path
    path.reset()

    # Current should be back at head after resetting
    assert path.current == path.head, "After a reset, current should be back at head"

    # Traverse again and check that we start from the beginning
    waypoint = path.get_next_waypoint()
    assert waypoint.x == 1 and waypoint.y == 1, "After reset, expected to see waypoint at (1, 1), but instead got ({waypoint.x}, {waypoint.y})"

    print("✓ PatrolPath reset works correctly!")

def test_patrol_path_edge_cases():
    """
    Test edge cases such as empty path, and single nodes
    """
    print("Testing PatrolPath edge cases...")
    
    # Test advancing empty patrol paths
    path = PatrolPath(patrol_type="one_way")
    assert path.get_next_waypoint() is None, "Expected None when getting the next waypoint from an empty patrol path"

    path = PatrolPath(patrol_type="circular")
    assert path.get_next_waypoint() is None, "Expected None when getting the next waypoint from an empty circular patrol path"

    path = PatrolPath(patrol_type="back_and_forth")
    assert path.get_next_waypoint() is None, "Expected None when getting the next waypoint from an empty back-and-forth patrol path"

    print("✓ Empty PatrolPath edge cases work correctly!")

    # Test single-node patrol path
    path = PatrolPath(patrol_type="one_way")
    path.add_waypoint(1, 1, wait_time=1)
    waypoint = path.get_next_waypoint()
    assert waypoint.x == 1 and waypoint.y == 1, "Expected to see waypoint at (1, 1) in single-node one-way patrol path"
    assert path.head == path.tail, "Expected in a single-node patrol path that the head, and tail still point to the same node after traversal"
    assert path.current == None, "Expected current to be None after traversing the only waypoint in a one-way patrol path"
    waypoint = path.get_next_waypoint()
    assert waypoint is None, "Expected None after traversing the only waypoint in a one-way patrol path"

    print("✓ Single-node one-way PatrolPath edge cases work correctly!")

    path = PatrolPath(patrol_type="circular")
    path.add_waypoint(1, 1, wait_time=1)
    assert path.head == path.tail == path.current, "Expected in a single-node circular patrol path that the head, tail, and current should all point to the same node"
    waypoint = path.get_next_waypoint()
    assert waypoint.x == 1 and waypoint.y == 1, "Expected to see waypoint at (1, 1) in single-node circular patrol path"
    assert path.head == path.tail == path.current, "Expected in a single-node circular patrol path that the head, tail, and current should all point to the same node"
    waypoint = path.get_next_waypoint()
    assert waypoint.x == 1 and waypoint.y == 1, "Expected to see waypoint at (1, 1) again in circular patrol path with one node"
    assert path.head == path.tail == path.current, "Expected in a single-node circular patrol path that the head, tail, and current should all point to the same node"

    print("✓ Single-node circular PatrolPath edge cases work correctly!")

    path = PatrolPath(patrol_type="back_and_forth")
    path.add_waypoint(1, 1, wait_time=1)
    waypoint = path.get_next_waypoint()
    assert waypoint.x == 1 and waypoint.y == 1, "Expected to see waypoint at (1, 1) in single-node back-and-forth patrol path"
    assert path.get_next_waypoint() is None, "Expected None after traversing the only waypoint in a back-and-forth patrol path"

    print("✓ Single-node back-and-forth PatrolPath edge cases work correctly!")

    print("✓ PatrolPath edge cases work correctly!")

def run_all_tests():
    """Run all linked list tests"""
    print("=" * 50)
    print("Running Linked List Tests")
    print("=" * 50)
    print()
    test_waypoint()
    test_patrol_path_basic()
    test_patrol_path_one_way()
    test_patrol_path_circular()
    test_patrol_path_back_and_forth()
    test_patrol_path_reset()
    test_patrol_path_edge_cases()
    print()
    print("=" * 50)
    print("✓ ALL TESTS PASSED!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()
