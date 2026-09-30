import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user.db")


def init_db():
    """Ensure the users table exists in the database. Auto-recovers if file is corrupted."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError:
        # If user.db exists but is corrupted (e.g. 0 or 1 byte empty file), reset it
        if os.path.exists(DB_PATH):
            try:
                os.remove(DB_PATH)
            except Exception:
                pass
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()


def signup(username, password):
    """Register a new user account. Returns True if successful, False if username exists."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False
    except Exception:
        return False
    finally:
        conn.close()


def login(username, password):
    """Authenticate an existing user. Returns True if credentials match."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        return user is not None
    except Exception:
        return False
    finally:
        conn.close()


# Initialize database automatically on import
init_db()