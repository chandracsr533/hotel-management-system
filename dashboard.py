from database import get_cursor


def dashboard_counts():
    cur = get_cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM rooms")
    rooms = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM rooms WHERE room_status='Available'"
    )
    available = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM rooms WHERE room_status='Booked'"
    )
    booked = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM bookings")
    bookings = cur.fetchone()[0]

    cur.execute(
        "SELECT IFNULL(SUM(total_amount),0) FROM bookings WHERE booking_status != 'Cancelled'"
    )
    revenue = float(cur.fetchone()[0])

    return {
        "customers": customers,
        "rooms": rooms,
        "available": available,
        "booked": booked,
        "bookings": bookings,
        "revenue": revenue
    }


def recent_bookings():
    cur = get_cursor()
    sql = """
    SELECT
        b.booking_id,
        c.customer_name,
        r.room_number,
        b.booking_status
    FROM bookings b
    JOIN customers c
        ON b.customer_id = c.customer_id
    JOIN rooms r
        ON b.room_id = r.room_id
    ORDER BY b.booking_id DESC
    LIMIT 5
    """
    cur.execute(sql)
    return cur.fetchall()


def recent_customers():
    cur = get_cursor()
    sql = """
    SELECT
        customer_id,
        customer_name,
        city
    FROM customers
    ORDER BY customer_id DESC
    LIMIT 5
    """
    cur.execute(sql)
    return cur.fetchall()


# ================= REPORTS ================= #

def report_summary():
    cur = get_cursor()

    # Total customers
    cur.execute("SELECT COUNT(*) FROM customers")
    total_customers = cur.fetchone()[0]

    # Total rooms
    cur.execute("SELECT COUNT(*) FROM rooms")
    total_rooms = cur.fetchone()[0]

    # Total bookings
    cur.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cur.fetchone()[0]

    # Total revenue (exclude cancelled)
    cur.execute(
        "SELECT IFNULL(SUM(total_amount), 0) FROM bookings WHERE booking_status != 'Cancelled'"
    )
    total_revenue = float(cur.fetchone()[0])

    # Available rooms
    cur.execute(
        "SELECT COUNT(*) FROM rooms WHERE room_status='Available'"
    )
    available_rooms = cur.fetchone()[0]

    # Booked rooms
    cur.execute(
        "SELECT COUNT(*) FROM rooms WHERE room_status='Booked'"
    )
    booked_rooms = cur.fetchone()[0]

    return {
        "customers": total_customers,
        "rooms": total_rooms,
        "bookings": total_bookings,
        "revenue": total_revenue,
        "available": available_rooms,
        "booked": booked_rooms
    }


def monthly_revenue():
    cur = get_cursor()
    sql = """
        SELECT
            DATE_FORMAT(check_in_date, '%Y-%m') AS month,
            SUM(total_amount) AS revenue
        FROM bookings
        WHERE booking_status != 'Cancelled'
        GROUP BY DATE_FORMAT(check_in_date, '%Y-%m')
        ORDER BY month
    """
    cur.execute(sql)
    rows = cur.fetchall()
    return [(r[0], float(r[1])) for r in rows] if rows else []


def booking_status_report():
    cur = get_cursor()
    sql = """
        SELECT
            booking_status,
            COUNT(*) AS total
        FROM bookings
        GROUP BY booking_status
    """
    cur.execute(sql)
    return cur.fetchall()


def room_type_report():
    cur = get_cursor()
    sql = """
        SELECT
            room_type,
            COUNT(*) AS total
        FROM rooms
        GROUP BY room_type
        ORDER BY total DESC
    """
    cur.execute(sql)
    return cur.fetchall()