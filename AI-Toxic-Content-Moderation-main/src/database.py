import sqlite3

DB_NAME = "moderation.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # --------------------------
    # Users Table
    # --------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT
    )
    """)

    # --------------------------
    # Comment History
    # --------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id TEXT,

        comment TEXT,

        toxicity REAL,

        severity TEXT,

        risk REAL,

        decision TEXT
    )
    """)

    conn.commit()
    conn.close()


# ============================================================
# USER FUNCTIONS
# ============================================================

def register_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users(username,password)
            VALUES(?,?)
            """,
            (username, password)
        )

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:

        conn.close()

        return False


def login_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=? AND password=?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# ============================================================
# COMMENT HISTORY
# ============================================================

def add_comment(
    user_id,
    comment,
    toxicity,
    severity,
    risk,
    decision
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO user_history
        (
            user_id,
            comment,
            toxicity,
            severity,
            risk,
            decision
        )
        VALUES
        (?,?,?,?,?,?)
        """,
        (
            user_id,
            comment,
            toxicity,
            severity,
            risk,
            decision
        )
    )

    conn.commit()
    conn.close()


def get_history(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM user_history
        WHERE user_id=?
        ORDER BY id
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_all_history():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM user_history
    ORDER BY id
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows