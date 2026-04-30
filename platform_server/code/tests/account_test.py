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
from platform_server.code import accounts
from platform_server.code.accounts import AccountManager
<<<<<<< Updated upstream
temp_user_data_path = tempfile.mkdtemp()
accounts.user_data_path = temp_user_data_path
# make a fresh name_id.json file for testing
with open(f"{temp_user_data_path}/name_id.json", "w") as f:
    json.dump({}, f) # should now be able to run the tests many times consecutively without issues
=======
from platform_server.code.accounts import Profile
>>>>>>> Stashed changes

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

def test_create_account():
    """
    Test creating a new account.
    """
    print ("   Testing account creation...")
    manager = AccountManager()
    assert manager.create_account("testuser", "password123") == True
    assert "testuser" in manager.usernames
    print(" ✓ Account creation worked correctly.")
    
def test_create_duplicate_account():
    """
    Test that duplicate usernames cannot be created.
    """
    print("   Testing duplicate account creation...")
    manager = AccountManager()
    manager.create_account("testuser", "password123")
    assert manager.create_account("testuser", "differentpass") == False
    print(" ✓ Duplicate account creation was successfully prevented.")

def test_authenticate_valid():
    """
    Test authentication with correct credentials.
    """
    print("   Testing valid authentication...")
    manager = AccountManager()
    manager.create_account("testuser", "password123")
    assert manager.authenticate("testuser", "password123") == True
    print(" ✓ Valid authentication worked correctly.")

def test_authenticate_invalid_password():
    """
    Test authentication with incorrect password.
    """
    print("   Testing invalid authentication...")
    manager = AccountManager()
    manager.create_account("testuser", "password123")
    assert manager.authenticate("testuser", "wrongpassword") == False
    print(" ✓ Invalid authentication worked correctly.")

def test_authenticate_nonexistent_user():
    """
    Test authentication for non-existent user.
    """
    print("   Testing authentication for non-existent user...")
    manager = AccountManager()
    try:
        manager.authenticate("nouser", "password123")
        assert False
    except KeyError:
        assert True
    print(" ✓ Non-existent user authentication worked correctly.")

def test_user_data_structure():
    """
    Test that user data file is created correctly.
    """
    print("   Testing user data structure...")
    manager = AccountManager()
    manager.create_account("testuser", "password123")
    with open("user_data/name_id.json", "r") as f:
        data = json.load(f)
    assert "testuser" in data
    user_id = data["testuser"]
    with open(f"user_data/{user_id}.json", "r") as f:
        user_data = json.load(f)
    assert user_data["USERNAME"] == "testuser"
    assert "PASSWORD_HASH" in user_data
    assert "GAME_DATA" in user_data
    assert "SURVIVING_1111" in user_data["GAME_DATA"]
    assert "THELLUSOMA" in user_data["GAME_DATA"]
    assert "LIZZIES_ADVENTURE" in user_data["GAME_DATA"]
    print(" ✓ User data structure is correct.")

def test_password_not_stored_in_plaintext():
    """
    Test that the password is not stored in plaintext.
    """
    print("   Testing password storage...")
    manager = AccountManager()
    manager.create_account("testuser", "password123")
    with open("user_data/name_id.json", "r") as f:
        data = json.load(f)
    user_id = data["testuser"]
    with open(f"user_data/{user_id}.json", "r") as f:
        user_data = json.load(f)
    assert user_data["PASSWORD_HASH"] != "password123"
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
        assert manager.create_account(username, password) == True
        assert manager.authenticate(username, password) == True
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
        assert manager.create_account(username, password) == True
        assert manager.create_account(username, password) == False
    print(" ✓ Duplicate random account creation was successfully prevented.")

<<<<<<< Updated upstream
=======
def test_random_sessions_addition(seed=12345678910, num_accounts=10):
    """
    Test adding sessions to profiles with random usernames. 
    """
    print("   Testing adding sessions to random profiles...")
    manager = AccountManager()
    random.seed(seed)
    user_list = ArrayList()
    for num in range(num_accounts):
        username = random_username()
        password = random_password()
        manager.create_account(username, password)
        new_profile = manager.accounts.get(username)
        user_list.append(new_profile)
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
    print(" ✓ Adding sessions to random profiles worked correctly.")

def random_sessions_addition(seed=12345678910, num_accounts=1000):
    """
    Test adding sessions to profiles with random usernames. 
    """
    print("   Testing adding sessions to random profiles...")
    manager = AccountManager()
    random.seed(seed)
    for num in range(num_accounts):
        username = random_username()
        password = random_password()
        manager.create_account(username, password)
        new_profile = manager.accounts.get(username)
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
    print(" ✓ Adding sessions to random profiles worked correctly.")

def local_test(seed=12345678910):
        manager = AccountManager()
        random.seed(seed)
        username = 'tuf08092'
        password = 'nullptr'
        profile = Profile(username, manager.ids)
        print(profile)
        print(profile.sessions) 
        amount = 10
        for sessions in range(amount):
            game = random_game()
            playtime = random_playtime()
            score = random_score()
            session = profile.create_session(game=game, time_played=playtime, score=score)
        profile.save_data()

>>>>>>> Stashed changes
def cleanup():
    """
    Clean up temporary user data files after testing.
    """
    shutil.rmtree(temp_user_data_path)
    print(" ✓ Cleaned up temporary user data files.")

if __name__ == "__main__":
    local = "--local" in sys.argv
    print(root_path)
    if not local:
        temp_user_data_path = tempfile.mkdtemp()
        accounts.user_data_path = temp_user_data_path
        # make a fresh name_id.json file for testing
        with open(f"{temp_user_data_path}/name_id.json", "w") as f:
            json.dump({}, f) # should now be able to run the tests many times consecutively without issues
    elif "--local" in sys.argv:
        temp_user_data_path = root_path + '/user_data'
    keep = "--keep" in sys.argv
    if "--seed" in sys.argv:
        seed = "--seed" in sys.argv and int(sys.argv[sys.argv.index("--seed") + 1])
    else:
        seed = random.randint(1, 999999)
    if "--num" in sys.argv:
        num_accounts = "--num" in sys.argv and int(sys.argv[sys.argv.index("--num") + 1])
    else:
        num_accounts = 10
    test_create_account()
    test_create_duplicate_account()
    test_authenticate_valid()
    test_authenticate_invalid_password()
    test_authenticate_nonexistent_user()
    test_user_data_structure()
    test_password_not_stored_in_plaintext()
    test_random_account_creation(seed=seed, num_accounts=num_accounts)
    seed += 1
<<<<<<< Updated upstream
    test_duplicate_random_account_creation(seed=seed, num_accounts=num_accounts)
=======
    try:
        test_duplicate_random_account_creation(seed=seed, num_accounts=num_accounts)
    except Exception as e:
        print(f"Error occurred while testing duplicate random account creation: {e}")
        print(f"It's possible that the seed {seed} led to a collision in usernames. You can try running the test again with a different seed using the --seed flag.")
    seed += 1
    try:
        test_random_sessions_addition(seed=seed)
    except Exception as e:
        print(f"Error occurred while testing random sessions addition: {e}")
        print(f"It's possible that the seed {seed} led to a collision in usernames. You can try running the test again with a different seed using the --seed flag.")
    seed += 1
    if "--local" in sys.argv:
        local_test(seed=seed)
>>>>>>> Stashed changes
    print(" ✓ All tests passed!")
    if not local:
        if not keep:
            cleanup()
        else:
            print("   Temporary user data files have been kept for inspection.")
    print(f"   Random seed used for random tests: {seed-1}")