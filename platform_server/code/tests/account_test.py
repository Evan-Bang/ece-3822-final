'''
account_test.py
Author: Emmanuel Morales
Date: 4/25/2026

Account Manager Testing
---------------------
Running this test will create temporary user data files in a temporary directory, 
so it won't affect any existing user data. Automatically, the test will clean up the 
temporary files after it finishes, unless you run it with the --keep flag, 
in which case the files will remain in your system for you to inspect and/or delete.
By default, the random account creation tests will use a fixed seed for reproducibility,
and only create 10 accounts for each of the two random test. If you want to specify a
particular seed for the random generation (for reproducibility), you can run the test with
the --seed flag followed by the desired seed value (numbers only). If you want to specify a
number of accounts to create for the random account creation tests, you can run the test with
the --num flag followed by the desired number of accounts (integers only).
Adding the --local flag let's you generate random profiles with random sessions on local user_data.

Make sure to run this test from the root directory (ece-3822-final/) with:
python3 -m platform_server.code.tests.account_test

If you want to keep the generated user data files for inspection, run with:
python3 -m platform_server.code.tests.account_test --keep

If you want to specify a random seed for the random account creation tests, run with:
python3 -m platform_server.code.tests.account_test --seed <seed_value>
e.g.:
python3 -m platform_server.code.tests.account_test --seed 12345

If you want to specify the number of accounts to create during the tests, run with:
python3 -m platform_server.code.tests.account_test --num <number_of_accounts>
e.g.:
python3 -m platform_server.code.tests.account_test --num 20

The test goes over:
- Creating a new account with a unique username
- Preventing duplicate usernames
- Authenticating with correct password
- Failing authentication with incorrect password
- Handling authentication for non-existent users
- Verifying the structure of the user data file after account creation
- Checking that the password is not stored in plaintext
- Creating multiple accounts with random usernames and passwords
- Preventing duplicate account creation with random usernames
'''

import sys
import os
import json
import random
import tempfile
import shutil
# setting path to use the root directory for imports
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, root_path)
# importing both the module and the class so I can reconfig the user_data_path for testing
from datastructures.array import ArrayList
from datastructures.hash_table import HashTable
from platform_server.code import accounts
from platform_server.code.accounts import AccountManager
from platform_server.code.accounts import Profile


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

def random_password():
    """
    Generate a random password for testing.
    output string: "<3-letters><5-digit number>"
    """
    random_letters = f"{random_letter()}{random_letter()}{random_letter()}"
    random_number = f"{random.randint(1, 99999):05d}"
    random_password = random_letters + random_number
    return random_password

def random_game():
    """
    Pick a random game from our list of games
    output string: one of "thellusoma", "surviving_1111", "lizzys_adventure"
    """
    random_game = random.choice(["thellusoma", "surviving_1111", "lizzys_adventure"])
    return random_game

def random_score():
    """
    Generate a random score for testing.
    output integer: mean of 100, standard deviation of 30
    """
    random_score = random.gauss(100, 30)
    random_score = int(random_score / 10) * 10
    random_score = max(0, min(150, random_score))
    return random_score

def random_playtime():
    """
    Generate a random playtime for testing.
    output integer: mean of 180, standard deviation of 30
    """
    random_playtime = random.gauss(180, 30)
    random_playtime = int(random_playtime)
    return random_playtime

def test_create_account():
    """
    Test creating a new account.
    """
    print ("   Testing account creation...")
    manager = AccountManager()
    manager.create_account("testuser", "password123")
    result = manager.accounts.get("testuser")
    assert hasattr(result, 'username') and hasattr(result, 'user_id'), "Account creation should return a Profile instance with 'username' and 'user_id' attributes."
    assert result.username == "testuser", f"Expected username to be 'testuser', but got '{result.username}' instead."
    assert result.user_id is not None, "A user_id should have been assigned."
    print(" ✓ Account creation worked correctly.")
    
def test_create_duplicate_account():
    """
    Test that duplicate usernames cannot be created.
    """
    print("   Testing duplicate account creation...")
    manager = AccountManager()
    manager.create_account("testuser", "password123")
    result = manager.create_account("testuser", "differentpass")
    assert result == 'False'
    print(" ✓ Duplicate account creation was successfully prevented.")

def test_authenticate_valid():
    """
    Test authentication with correct credentials.
    """
    print("   Testing valid authentication...")
    manager = AccountManager()
    new_profile = manager.create_account("anothertestuser", "password456")
    result = manager.authenticate("anothertestuser", "password456")
    assert result[0] == 'True'
    assert result[1] == 'Login successful'
    print(" ✓ Valid authentication worked correctly.")

def test_authenticate_invalid_password():
    """
    Test authentication with incorrect password.
    """
    print("   Testing invalid authentication...")
    manager = AccountManager()
    manager.create_account("testsomeuser", "password789")
    assert manager.authenticate("testsomeuser", "wrongpassword") == False
    print(" ✓ Invalid authentication worked correctly.")

def test_authenticate_nonexistent_user():
    """
    Test authentication for non-existent user.
    """
    print("   Testing authentication for non-existent user...")
    manager = AccountManager()
    try:
        result = manager.authenticate("nouser", "password123")
        assert result == False, f"Authentication for non-existent user should return False, but got {result} instead."
    except KeyError:
        assert True
    print(" ✓ Non-existent user authentication worked correctly.")

def test_user_data_structure():
    """
    Test that user data file is created correctly.
    """
    print("   Testing user data structure...")
    manager = AccountManager()
    manager.create_account("testthatuser", "password101112")
    with open(os.path.join(temp_user_data_path, "name_id.json"), "r") as f:
        data = json.load(f)
    assert "testthatuser" in data, f"Username 'testthatuser' should be in name_id.json, but it's not: {data}"
    user_id = data["testthatuser"]
    with open(os.path.join(temp_user_data_path, f"{user_id}.json"), "r") as f:
        user_data = json.load(f)
    assert user_data["USERNAME"] == "testthatuser"
    assert "PASSWORD_HASH" in user_data
    assert "GAME_HISTORY" in user_data
    print(" ✓ User data structure is correct.")

def test_add_session_to_profile():
    """
    Test adding a session to a profile.
    """
    print("   Testing adding session to profile...")
    manager = AccountManager()
    manager.create_account("sessiontestuser", "password321")
    new_profile = manager.accounts.get("sessiontestuser")
    session = new_profile.create_session(game="Thellusoma", time_played=42, score=9001)
    assert new_profile.sessions[0].game == "Thellusoma"
    assert new_profile.sessions[0].username == "sessiontestuser"
    assert new_profile.sessions[0].time_played == 42
    assert new_profile.sessions[0].score == 9001
    assert new_profile.sessions[0].id == 1
    new_profile.save_data() # check the saved data
    with open(new_profile.data_file, "r") as f:
        data = json.load(f)
        session_data = data['GAME_HISTORY']['SESSION_1']
        assert session_data['GAME'] == "Thellusoma"
        assert session_data['USERNAME'] == "sessiontestuser"
        assert session_data['PLAYTIME'] == 42
        assert session_data['SCORE'] == 9001
    print(" ✓ Adding session to profile worked correctly.")

def test_password_not_stored_in_plaintext():
    """
    Test that the password is not stored in plaintext.
    """
    print("   Testing password storage...")
    manager = AccountManager()
    manager.create_account("testthatuser", "password101112")
    with open(os.path.join(temp_user_data_path, "name_id.json"), "r") as f:
        data = json.load(f)
    user_id = data["testthatuser"]
    with open(os.path.join(temp_user_data_path, f"{user_id}.json"), "r") as f:
        user_data = json.load(f)
    assert user_data["PASSWORD_HASH"] != "password101112", "Password should not be stored in plaintext."
    assert ":" in user_data["PASSWORD_HASH"] # should be in format salt:hash
    print(" ✓ Password hash is stored correctly.")

def test_random_account_creation(seed=123456789,num_accounts=10):
    """
    Test creating multiple accounts with random usernames and passwords.
    """
    print("   Testing random account creation...")
    manager = AccountManager()
    random.seed(seed)
    for num in range(num_accounts):
        username = random_username()
        password = random_password()
        manager.create_account(username, password)
        new_profile = manager.accounts.get(username)
        assert hasattr(new_profile, 'username') and hasattr(new_profile, 'user_id'), "Account creation should return a Profile instance with 'username' and 'user_id' attributes."
        assert new_profile.username == username, f"Expected username to be '{username}', but got '{new_profile.username}' instead."
        assert new_profile.user_id is not None, "A user_id should have been assigned."
        result = manager.authenticate(username, password)
        assert result[0] == 'True'
        assert result[1] == 'Login successful'
    print(" ✓ Random account creation and authentication worked correctly.")

def test_duplicate_random_account_creation(seed=1234567890,num_accounts=10):
    """
    Test that creating accounts with random usernames does not allow duplicates.
    """
    print("   Testing duplicate random account creation...")
    manager = AccountManager()
    random.seed(seed)
    for num in range(num_accounts):
        username = random_username()
        password = random_password()
        manager.create_account(username, password)
        assert manager.create_account(username, password) == 'False'
    print(" ✓ Duplicate random account creation was successfully prevented.")

def test_random_sessions_addition(seed=12345678910, num_accounts=10):
    """
    Test adding sessions to profiles with random usernames. 
    """
    print("   Testing adding sessions to random profiles...")
    manager = AccountManager()
    random.seed(seed)
    new_user_num = 0
    for num in range(num_accounts):
        username = random_username()
        password = random_password()
        result = manager.create_account(username, password)
        if result != 'False':
            new_profile = manager.accounts.get(username)
            new_user_num += 1
            for amount in range(int(random.gauss(6, 2))):
                # Add a random session for the selected user
                game = random_game()
                playtime = random_playtime()
                score = random_score()
                session = new_profile.create_session(game=game, time_played=playtime, score=score)
            new_profile.save_data() # check the saved data
            with open(new_profile.data_file, "r") as f:
                data = json.load(f)
                for session in new_profile.sessions:
                    session_data = data['GAME_HISTORY'][f'SESSION_{session.id}']
                    assert session_data['GAME'] == session.game
                    assert session_data['USERNAME'] == session.username
                    assert session_data['PLAYTIME'] == session.time_played
                    assert session_data['SCORE'] == session.score
    print(" ✓ Adding sessions to random profiles worked correctly.")
    if local:
        print(f"{new_user_num} new users were created and added to the existing user data")

def random_sessions_addition(seed=12345678910, num_accounts=10):
    """
    Test adding sessions to profiles with random usernames. 
    """
    print("   Testing adding sessions to random existing profiles...")
    manager = AccountManager()
    random.seed(seed)
    for num in range(num_accounts):
        username = random_username()
        password = random_password()
        new_profile = manager.create_account(username, password)
        for amount in range(random.randint(1,10)):
            # Add a random session for the selected user
            game = random_game()
            playtime = random_playtime()
            score = random_score()
            session = new_profile.create_session(game=game, time_played=playtime, score=score)
        new_profile.save_data() # check the saved data
        with open(new_profile.data_file, "r") as f:
            data = json.load(f)
            for session in new_profile.sessions:
                session_data = data['GAME_HISTORY'][f'SESSION_{session.id}']
                assert session_data['GAME'] == session.game
                assert session_data['USERNAME'] == session.username
                assert session_data['PLAYTIME'] == session.time_played
                assert session_data['SCORE'] == session.score
    print(" ✓ Adding sessions to random existing profiles worked correctly.")

def local_test_manny(seed=12345678910):
        manager = AccountManager()
        random.seed(seed)
        username = 'tuf08092'
        password = 'nullptr'
        profile = Profile(username, manager.ids)
        amount = 10
        for sessions in range(amount):
            game = random_game()
            playtime = random_playtime()
            score = random_score()
            session = profile.create_session(game=game, time_played=playtime, score=score)
        profile.save_data()

def fresh_setup():
    # clean the whole user_data — remove all JSON files
    for filename in os.listdir(temp_user_data_path):
        if filename.endswith(".json"):
            os.remove(os.path.join(temp_user_data_path, filename))
    # reinitialize with a fresh name_id.json
    with open(f"{temp_user_data_path}/name_id.json", "w") as f:
        json.dump({}, f)
    manager = AccountManager()
    manager.create_account("tuf08092", "nullptr")
    manager.create_account("tut69764", "nullptr")
    manager.create_account("tuq10172", "nullptr")

def cleanup():
    """
    Clean up temporary user data files after testing.
    """
    shutil.rmtree(temp_user_data_path)
    print(" ✓ Cleaned up temporary user data files.")

if __name__ == "__main__":
    reset = "--reset" in sys.argv
    local = "--local" in sys.argv
    print(root_path)
    if not local:
        temp_user_data_path = tempfile.mkdtemp()
        accounts.user_data_path = temp_user_data_path
        # make a fresh name_id.json file for testing
        with open(f"{temp_user_data_path}/name_id.json", "w") as f:
            json.dump({}, f) # should now be able to run the tests many times consecutively without issues
    elif local:
        temp_user_data_path = root_path + '/user_data'
    keep = "--keep" in sys.argv
    if "--seed" in sys.argv:
        seed = "--seed" in sys.argv and int(sys.argv[sys.argv.index("--seed") + 1])
        seed0 = seed
    else:
        seed = random.randint(1, 999999)
        seed0 = seed
    if "--num" in sys.argv:
        num_accounts = "--num" in sys.argv and int(sys.argv[sys.argv.index("--num") + 1])
    else:
        num_accounts = 10   
    if not local:
        test_create_account()
        test_create_duplicate_account()
        test_authenticate_valid()
        test_authenticate_invalid_password()
        test_authenticate_nonexistent_user()
        test_user_data_structure()
        test_password_not_stored_in_plaintext()
        try:
          test_random_account_creation(seed=seed, num_accounts=num_accounts)
        except Exception as e:
         print(f"Error occurred while testing random account creation: {e}")
         print(f"It's possible that the seed {seed} led to a collision in usernames. You can try running the test again with a different seed using the --seed flag.")
        seed += 1
        try:
           test_duplicate_random_account_creation(seed=seed, num_accounts=num_accounts)
        except Exception as e:
           print(f"Error occurred while testing duplicate random account creation: {e}")
           print(f"It's possible that the seed {seed} led to a collision in usernames. You can try running the test again with a different seed using the --seed flag.")
        seed += 1
    elif local:
        if reset:
            fresh_setup()          
    if not reset:
        try:
            test_random_sessions_addition(seed=seed, num_accounts=num_accounts)
        except Exception as e:
            print(f"Error occurred while testing random sessions addition: {e}")
            print(f"It's possible that the seed {seed} led to a collision in usernames. You can try running the test again with a different seed using the --seed flag.")
        seed += 1
    if "--manny" in sys.argv:
        local_test_manny(seed=seed)
        seed += 1
    print(" ✓ All tests passed!")
    if not local:
        if not keep:
            cleanup()
        else:
            print("   Temporary user data files have been kept for inspection.")
    print(f"   Random seed used for random tests: {seed0}")
    print(f"   Number of accounts created during random tests: {num_accounts}")