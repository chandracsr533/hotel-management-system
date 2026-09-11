from datetime import datetime, date
import mysql.connector
from database import get_connection, get_cursor


# View All Bookings
def get_bookings():
    cur = get_cursor()
    sql = """
    SELECT
        b.booking_id,
        c.customer_name,
        r.room_number,
        b.check_in_date,
        b.check_out_date,
        b.total_days,
        b.total_amount,
        b.booking_status
    FROM bookings b
    JOIN customers c
        ON b.customer_id = c.customer_id
    JOIN rooms r
        ON b.room_id = r.room_id
    ORDER BY b.booking_id DESC
    """
    cur.execute(sql)
    return cur.fetchall()


# Get Customers
def get_customer_list():
    cur = get_cursor()
    cur.execute("SELECT customer_id, customer_name FROM customers ORDER BY customer_name ASC")
    return cur.fetchall()


# Get Available Rooms
def get_available_rooms(check_in=None, check_out=None):
    cur = get_cursor()
    if check_in and check_out:
        cur.execute("""
            SELECT r.room_id, r.room_number, r.room_type, r.room_price
            FROM rooms r
            WHERE NOT EXISTS (
                SELECT 1
                FROM bookings b
                WHERE b.room_id = r.room_id
                AND b.booking_status != 'Cancelled'
                AND b.check_in_date < %s
                AND b.check_out_date > %s
            )
            ORDER BY r.room_number ASC
        """, (check_out, check_in))
    else:
        cur.execute("""
            SELECT room_id, room_number, room_type, room_price
            FROM rooms
            WHERE room_status='Available'
            ORDER BY room_number ASC
        """)
    return cur.fetchall()


def insert_booking(data):
    conn = get_connection()
    cur = get_cursor()

    customer_id = data[0]
    room_id = data[1]
    check_in = data[2]
    check_out = data[3]

    # Convert dates
    try:
        d1 = datetime.strptime(str(check_in), "%Y-%m-%d")
        d2 = datetime.strptime(str(check_out), "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date format. Expected YYYY-MM-DD."

    # Validate dates
    if d2 <= d1:
        return False, "Check-out date must be after check-in date."

    # Check whether room exists and get price
    cur.execute(
        """
        SELECT room_price, room_status
        FROM rooms
        WHERE room_id=%s
        """,
        (room_id,)
    )
    room = cur.fetchone()

    if not room:
        return False, "Selected room does not exist."

    price = room[0]

    # Check overlapping bookings
    cur.execute(
        """
        SELECT booking_id
        FROM bookings
        WHERE room_id=%s
        AND booking_status != 'Cancelled'
        AND check_in_date < %s
        AND check_out_date > %s
        """,
        (room_id, check_out, check_in)
    )
    existing_booking = cur.fetchone()

    if existing_booking:
        return False, "This room is already booked for the selected dates."

    # Calculate number of days
    days = (d2 - d1).days
    total = days * float(price)

    # Insert booking
    sql = """
    INSERT INTO bookings
    (
        customer_id,
        room_id,
        check_in_date,
        check_out_date,
        total_days,
        total_amount,
        booking_status
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s)
    """

    try:
        cur.execute(
            sql,
            (
                customer_id,
                room_id,
                check_in,
                check_out,
                days,
                total,
                "Confirmed"
            )
        )

        # Update room status if booking includes today
        today = date.today()
        if d1.date() <= today <= d2.date():
            cur.execute(
                """
                UPDATE rooms
                SET room_status='Booked'
                WHERE room_id=%s
                """,
                (room_id,)
            )

        conn.commit()
        return True, "Booking created successfully."
    except mysql.connector.Error as err:
        conn.rollback()
        return False, f"Database error: {err}"


def get_room_id(booking_id):
    cur = get_cursor()
    sql = """
    SELECT room_id
    FROM bookings
    WHERE booking_id=%s
    """
    cur.execute(sql, (booking_id,))
    row = cur.fetchone()
    return row[0] if row else None


# Cancel Booking (soft cancel that preserves invoice/history)
def cancel_booking(booking_id):
    conn = get_connection()
    cur = get_cursor()

    room_id = get_room_id(booking_id)
    if not room_id:
        return False, "Booking not found."

    try:
        # Mark booking status as Cancelled
        cur.execute(
            """
            UPDATE bookings
            SET booking_status='Cancelled'
            WHERE booking_id=%s
            """,
            (booking_id,)
        )

        # Check if any active confirmed bookings remain for this room today
        today = date.today().strftime("%Y-%m-%d")
        cur.execute(
            """
            SELECT COUNT(*) FROM bookings
            WHERE room_id=%s AND booking_status='Confirmed'
            AND check_in_date <= %s AND check_out_date > %s
            """,
            (room_id, today, today)
        )
        active_count = cur.fetchone()[0]

        if active_count == 0:
            cur.execute(
                """
                UPDATE rooms
                SET room_status='Available'
                WHERE room_id=%s
                """,
                (room_id,)
            )

        conn.commit()
        return True, "Booking cancelled successfully."
    except mysql.connector.Error as err:
        conn.rollback()
        return False, f"Database error: {err}"


# Keep delete_booking mapping to cancel_booking to prevent accidental data loss
def delete_booking(booking_id):
    return cancel_booking(booking_id)


def search_booking(keyword):
    cur = get_cursor()
    sql = """
    SELECT
        b.booking_id,
        c.customer_name,
        r.room_number,
        b.check_in_date,
        b.check_out_date,
        b.total_days,
        b.total_amount,
        b.booking_status
    FROM bookings b
    JOIN customers c
        ON b.customer_id = c.customer_id
    JOIN rooms r
        ON b.room_id = r.room_id
    WHERE
        c.customer_name LIKE %s
        OR r.room_number LIKE %s
        OR b.booking_status LIKE %s
    ORDER BY b.booking_id DESC
    """
    value = "%" + keyword + "%"
    cur.execute(sql, (value, value, value))
    return cur.fetchall()