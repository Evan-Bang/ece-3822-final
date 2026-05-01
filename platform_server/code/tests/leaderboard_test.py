'''
leaderboard_test.py
Author: Emmanuel Morales
Date: 4/26/2026

Leaderboard Testing
---------------------
Running this test will create temporary data files in a temporary directory, 
so it won't affect any existing data or create clutter. Automatically, the test will 
clean up the temporary files after it finishes, unless you run it with the --keep flag, 
in which case the files will remain in your system for you to inspect and/or delete.

Make sure to run this test from the root directory (ece-3822-final/) with:
python3 -m platform_server.code.tests.leaderboard_test

or with the --keep flag if you want to inspect the generated data files:
python3 -m platform_server.code.tests.leaderboard_test --keep

The test goes over:
- Adding a new score for a username not previously on the leaderboard
- Updating the score of a username already on the leaderboard with a higher score
- Updating the score of a username already on the leaderboard with a lower score
- Retrieving the top n players from the leaderboard
- Adding random scores for random usernames and retrieving the top player
- Retrieving from the leaderboard users who's scores are within a certain range from the leaderboard
- Querying the score of a specific user from the leaderboard
- Sorting the leaderboard by score
- Saving the leaderboard to a JSON file
- Loading the leaderboard from a JSON file
'''

import sys
import os
# setting path to use the root directory for imports
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
sys.path.insert(0, root_path)
# importing both the module and the class
from platform_server.code import leaderboard
from platform_server.code.leaderboard import Leaderboard
from datastructures.array import ArrayList
import random
import tempfile
import shutil
temp_user_data_path = tempfile.mkdtemp()

def random_letter():
    """
    Generate a random lowercase letter for testing.
    output string: "<letter>"
    """
    random_letter = random.choice('abcdefghijklmnopqrstuvwxyz')
    return random_letter

def random_username():
    """
    Generate a random username for testing.
    output string: "tu<letter><5-digit number>"
    """
    random_number = f"{random.randint(1, 99999):05d}"
    random_username = "tu" + random_letter() + random_number
    return random_username

def random_score():
    """
    Generate a random score for testing.
    output int: <number between 0 and 1000>
    """
    random_score = random.randint(0, 1000)
    return random_score

def test_create_leaderboard():
    """
    Test creating a new leaderboard and adding a score for a new username
    """
    print("   Testing creating a new leaderboard and adding a score for a new username...")
    lb = Leaderboard()
    # Test adding a new score for a username not previously on the leaderboard
    assert lb.add_score("user1", 100) == True, "Failed to add new score for user1"
    assert lb.score_table.get("user1") == 100, "Score for user1 not correctly stored in hash table"
    print(" ✓ Successfully created a new leaderboard and adding a score for a new username")

def test_update_leaderboard():
    """
    Test updating the score of a username already on the leaderboard with a higher and lower score
    """
    print("   Testing updating the score of a username already on the leaderboard...")
    lb = Leaderboard()
    lb.add_score("user1", 100)
    # Test updating the score of a username already on the leaderboard with a higher score
    assert lb.add_score("user1", 150) == True, "Failed to update score for user1 with a higher score"
    assert lb.score_table.get("user1") == 150, "Score for user1 not correctly updated in hash table"

    # Test updating the score of a username already on the leaderboard with a lower score
    assert lb.add_score("user1", 120) == False, "Incorrectly updated score for user1 with a lower score"
    assert lb.score_table.get("user1") == 150, "Score for user1 should not have been updated in hash table"
    print(" ✓ Successfully updated the score of a username already on the leaderboard")

def test_get_top_n():
    """
    Test retrieving the top n players from the leaderboard
    """
    print("   Testing retrieving the top n players from the leaderboard...")
    lb = Leaderboard()
    lb.add_score("user1", 150)
    # Test retrieving the top n players from the leaderboard
    lb.add_score("user2", 200)
    lb.add_score("user3", 50)
    top_players = lb.get_top_n(2)
    expected_top_players = ArrayList()
    expected_top_players.append(("user2", 200))
    expected_top_players.append(("user1", 150))
    assert top_players == expected_top_players, f"Expected top players {expected_top_players}, but got {top_players}"
    print(" ✓ Successfully retrieved the top n players from the leaderboard")

def test_top_from_random_scores(num_players=100):
    """
    Test adding random scores for random usernames and retrieving the top player
    """
    print("   Testing adding random scores for random usernames and retrieving the top n player...")
    lb = Leaderboard()
    top1_player = ArrayList()
    for players in range(num_players):
        username = random_username()
        score = random_score()
        lb.add_score(username, score)
        if len(top1_player) == 0 or score > top1_player[0][1]:
            top1_player.clear()
            top1_player.append((username, score))
    
    top_players = lb.get_top_n(1)
    assert len(top_players) == 1, f"Expected 1 top player, but got {len(top_players)}"
    assert top_players == top1_player, f"Expected top player {top1_player}, but got {top_players}"
    print(" ✓ Successfully added random scores for random usernames and retrieved the top n players")

def test_ranged_query():
    """
    Test retrieving users from the leaderboard within a score range
    """
    print("   Testing ranged queries from the leaderboard...")
    lb = Leaderboard()
    lb.add_score("user1", 100)
    lb.add_score("user2", 200)
    lb.add_score("user3", 300)
    lb.add_score("user4", 400)
    lb.add_score("user5", 500)

    # Test retrieving users with scores between 150 and 450
    expected_players = ArrayList()
    expected_players.append(("user2", 200))
    expected_players.append(("user3", 300))
    expected_players.append(("user4", 400))

    players_in_range = lb.ranged_query(150, 450)
    assert players_in_range == expected_players, f"Expected players in range {expected_players}, but got {players_in_range}"
    print(" ✓ Successfully retrieved the leaderboard users within the specified score range")

def test_query_specific_user(num_players=100):
    """
    Test querying the score of a specific user on the leaderboard
    """
    print("   Testing querying the score of a specific user on the leaderboard...")
    lb = Leaderboard()
    lb.add_score("user1", 100)
    for players in range(num_players):
        username = random_username()
        score = random_score()
        lb.add_score(username, score)
    lb.add_score("user2", 200)

    # Test querying the score of a specific user
    assert lb.get_player_score("user1") == 100, "Failed to retrieve correct score for user1"
    assert lb.get_player_score("user2") == 200, "Failed to retrieve correct score for user2"
    assert lb.get_player_score("user3") == None, "Expected None for non-existent user3, but got a value"
    print(" ✓ Successfully got the scores of specific users on the leaderboard")

def test_sort_leaderboard(num_players=100):
    """
    Test sorting the leaderboard by score
    """
    print("   Testing sorting the leaderboard by score...")
    lb = Leaderboard()
    for players in range(num_players):
        username = random_username()
        score = random_score()
        lb.add_score(username, score)
    sorted_leaderboard = lb.get_all_sorted()
    # Check that the leaderboard is sorted in ascending order by score
    for i in range(1, len(sorted_leaderboard)):
        assert sorted_leaderboard[i-1][1] <= sorted_leaderboard[i][1], f"Leaderboard is not sorted correctly. Got {sorted_leaderboard[i-1][1]} on index {i-1} and {sorted_leaderboard[i][1]} on index {i}"
    print(" ✓ Successfully sorted the leaderboard by score")

def test_save_and_load_json():
    """
    Test saving and loading the leaderboard to and from a JSON file
    """
    print("   Testing saving and loading the leaderboard to and from a JSON file...")
    lb = Leaderboard()
    lb.add_score("user1", 100)
    lb.add_score("user2", 200)
    lb.add_score("user3", 300)

    # Save the leaderboard to a JSON file
    lb.save_to_json(temp_user_data_path + "/test_leaderboard.json")

    # Create a new leaderboard and load the data from the JSON file
    loaded_lb = Leaderboard()
    loaded_lb.load_from_json(temp_user_data_path + "/test_leaderboard.json")

    # Check that the loaded leaderboard has the same scores as the original
    assert loaded_lb.get_player_score("user1") == 100, "Failed to load correct score for user1 from JSON"
    assert loaded_lb.get_player_score("user2") == 200, "Failed to load correct score for user2 from JSON"
    assert loaded_lb.get_player_score("user3") == 300, "Failed to load correct score for user3 from JSON"
    print(" ✓ Successfully saved and loaded the leaderboard to and from a JSON file")

def cleanup():
    """
    Clean up temporary user data files after testing.
    """
    shutil.rmtree(temp_user_data_path)
    print(" ✓ Cleaned up temporary user data files.")

if __name__ == "__main__":
    keep = "--keep" in sys.argv
    test_create_leaderboard()
    test_update_leaderboard()
    test_get_top_n()
    test_top_from_random_scores()
    test_ranged_query()
    test_query_specific_user()
    test_sort_leaderboard()
    # test_save_and_load_json() # DEPRECATED
    if not keep:
        cleanup()
    else:
        print("   Temporary user data files have been kept for inspection.")
    print(" ✓ All tests passed!")