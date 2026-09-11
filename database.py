import mysql.connector

from config import HOST, PORT, USER, PASSWORD, DATABASE


connection = None
cursor = None


def init_connection():
    """Create the MySQL database connection."""

    global connection, cursor

    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        cursor = connection.cursor()

        print("[OK] Database Connected Successfully")

        return connection, cursor

    except mysql.connector.Error as err:
        print(f"[ERROR] Database Connection Error: {err}")

        connection = None
        cursor = None

        return None, None


def get_connection():
    """Return an active database connection."""

    global connection, cursor

    try:
        if connection is None or not connection.is_connected():

            connection, cursor = init_connection()

        else:
            connection.ping(
                reconnect=True,
                attempts=3,
                delay=1
            )

    except mysql.connector.Error:
        connection, cursor = init_connection()

    return connection


def get_cursor():
    """Return a cursor for the active database connection."""

    global connection, cursor

    conn = get_connection()

    if conn is None:
        return None

    try:
        if cursor is None:
            cursor = conn.cursor()

        return cursor

    except mysql.connector.Error as err:
        print(f"[ERROR] Cursor Error: {err}")
        cursor = None
        return None


# Initialize database connection when application starts
init_connection()