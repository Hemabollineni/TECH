
import sqlite3
import hashlib
import secrets
import hmac
import getpass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "auth.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_auth_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                salt BLOB NOT NULL,
                password_hash BLOB NOT NULL
            )
        """)


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600000
    )

    return salt, password_hash


def create_user(username, password):
    salt, password_hash = hash_password(password)

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, salt, password_hash) "
                "VALUES (?, ?, ?)",
                (username, salt, password_hash)
            )
        return True

    except sqlite3.IntegrityError:
        return False


def authenticate(username, password):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT salt, password_hash FROM users WHERE username = ?",
            (username,)
        ).fetchone()

    if row is None:
        return False

    salt, stored_hash = row
    _, entered_hash = hash_password(password, salt)

    return hmac.compare_digest(stored_hash, entered_hash)


def login_required():
    initialize_auth_db()

    for attempt in range(3):
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")

        if authenticate(username, password):
            print("Login successful!")
            return username

        remaining = 2 - attempt

        if remaining > 0:
            print(f"Invalid credentials. Attempts remaining: {remaining}")

    print("Access denied. Maximum login attempts reached.")
    return None
