
import getpass
import os
from auth import initialize_auth_db, create_user, DB_PATH

initialize_auth_db()

username = input("Enter new username: ").strip()

if not username:
    print("Username cannot be empty.")
    raise SystemExit(1)

password = getpass.getpass("Enter new password: ")
confirm_password = getpass.getpass("Confirm password: ")

if len(password) < 8:
    print("Password must be at least 8 characters.")
    raise SystemExit(1)

if password != confirm_password:
    print("Passwords do not match.")
    raise SystemExit(1)

if create_user(username, password):
    try:
        os.chmod(DB_PATH, 0o600)
    except OSError:
        print("Warning: Could not restrict database permissions.")

    print("User created successfully.")
else:
    print("That username already exists.")
