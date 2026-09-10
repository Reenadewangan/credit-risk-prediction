import sqlite3
import bcrypt
import pandas as pd

DB_NAME = "users.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Predictions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            credit_amount INTEGER NOT NULL,
            duration INTEGER NOT NULL,
            prediction INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()
    conn.close()

    if result is None:
        return False

    stored_password = result[0].encode("utf-8")

    return bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password
    )

def save_prediction(username, credit_amount, duration, prediction):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            credit_amount INTEGER NOT NULL,
            duration INTEGER NOT NULL,
            prediction INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO predictions
        (username, credit_amount, duration, prediction)
        VALUES (?, ?, ?, ?)
    """, (
        username,
        credit_amount,
        duration,
        prediction
    ))

    conn.commit()
    conn.close()

def get_prediction_history(username):
    conn = sqlite3.connect(DB_NAME)

    query = """
        SELECT
            created_at,
            credit_amount,
            duration,
            prediction
        FROM predictions
        WHERE username = ?
        ORDER BY created_at DESC
    """

    history = pd.read_sql_query(
        query,
        conn,
        params=(username,)
    )

    conn.close()    

    return history