import mysql.connector

from database import get_connection, get_cursor

# View All Rooms
def get_rooms():
    cur = get_cursor()
    sql = "SELECT * FROM rooms ORDER BY room_id DESC"
    cur.execute(sql)
    return cur.fetchall()


# Add Room
def insert_room(data):
    conn = get_connection()
    cur = get_cursor()
    sql = """
    INSERT INTO rooms
    (
        room_number,
        room_type,
        room_price,
        room_status,
        floor_number,
        room_description
    )
    VALUES
    (%s,%s,%s,%s,%s,%s)
    """
    try:
        cur.execute(sql, data)
        conn.commit()
        return True, "Room added successfully."
    except mysql.connector.IntegrityError:
        conn.rollback()
        return False, "A room with this room number already exists."
    except mysql.connector.Error as err:
        conn.rollback()
        return False, f"Database error: {err}"


# Get Room by ID
def get_room_by_id(room_id):
    cur = get_cursor()
    sql = "SELECT * FROM rooms WHERE room_id=%s"
    cur.execute(sql, (room_id,))
    return cur.fetchone()


# Update Room
def update_room(data):
    conn = get_connection()
    cur = get_cursor()
    sql = """
    UPDATE rooms
    SET
        room_number=%s,
        room_type=%s,
        room_price=%s,
        room_status=%s,
        floor_number=%s,
        room_description=%s
    WHERE room_id=%s
    """
    try:
        cur.execute(sql, data)
        conn.commit()
        return True, "Room updated successfully."
    except mysql.connector.IntegrityError:
        conn.rollback()
        return False, "A room with this room number already exists."
    except mysql.connector.Error as err:
        conn.rollback()
        return False, f"Database error: {err}"


# Delete Room
def delete_room(room_id):
    conn = get_connection()
    cur = get_cursor()
    sql = "DELETE FROM rooms WHERE room_id=%s"
    try:
        cur.execute(sql, (room_id,))
        conn.commit()
        return True, "Room deleted successfully."
    except mysql.connector.IntegrityError:
        conn.rollback()
        return False, "Cannot delete room because it is associated with existing bookings."
    except mysql.connector.Error as err:
        conn.rollback()
        return False, f"Database error: {err}"


# Search Room
def search_room(keyword):
    cur = get_cursor()
    sql = """
    SELECT *
    FROM rooms
    WHERE room_number LIKE %s
       OR room_type LIKE %s
       OR room_status LIKE %s
    ORDER BY room_id DESC
    """
    value = "%" + keyword + "%"
    cur.execute(sql, (value, value, value))
    return cur.fetchall()