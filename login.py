from database import get_cursor
from werkzeug.security import check_password_hash


def admin_login(username, password):
    cur = get_cursor()
    if not cur:
        return None

    sql = """
    SELECT password
    FROM admins
    WHERE username=%s
    """

    cur.execute(sql, (username,))

    result = cur.fetchone()

    if not result:
        return None

    stored_password = result[0]

    if check_password_hash(stored_password, password):
        return True

    return None