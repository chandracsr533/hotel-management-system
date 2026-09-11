"""
CLI utility to create or update admin users for Aurum Hotel Management System.
Usage:
    python create_admin.py [username] [password]
"""
import sys
from werkzeug.security import generate_password_hash
from database import get_connection, get_cursor


def create_or_update_admin(username, password):
    conn = get_connection()
    cur = get_cursor()

    if not conn or not cur:
        print("[ERROR] Could not connect to the database.")
        return False

    hashed = generate_password_hash(password)

    sql = """
    INSERT INTO admins (username, password)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE password=%s
    """
    try:
        cur.execute(sql, (username, hashed, hashed))
        conn.commit()
        print(f"[OK] Admin user '{username}' created/updated successfully.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save admin user: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        u = sys.argv[1]
        p = sys.argv[2]
    else:
        u = input("Enter admin username [default: admin]: ").strip() or "admin"
        p = input("Enter admin password [default: admin123]: ").strip() or "admin123"

    create_or_update_admin(u, p)

