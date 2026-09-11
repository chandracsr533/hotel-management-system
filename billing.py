from decimal import Decimal

from database import get_cursor


GST_RATE = Decimal("0.18")

def get_bill_data():
    cur = get_cursor()
    sql = """
    SELECT
        b.booking_id,
        c.customer_name,
        r.room_number,
        b.total_amount
    FROM bookings b
    JOIN customers c
        ON b.customer_id = c.customer_id
    JOIN rooms r
        ON b.room_id = r.room_id
    ORDER BY b.booking_id DESC
    """
    cur.execute(sql)
    rows = cur.fetchall()

    bills = []
    for row in rows:
        booking_id = row[0]
        customer = row[1]
        room = row[2]
        total = Decimal(str(row[3])) if row[3] is not None else Decimal("0.00")
        gst = total * GST_RATE
        grand = total + gst

        bills.append((
            booking_id,
            customer,
            room,
            total,
            gst,
            grand
        ))

    return bills


def get_invoice(booking_id):
    cur = get_cursor()
    sql = """
    SELECT
        b.booking_id,
        c.customer_name,
        r.room_number,
        b.check_in_date,
        b.check_out_date,
        b.total_days,
        b.total_amount
    FROM bookings b
    JOIN customers c
        ON b.customer_id = c.customer_id
    JOIN rooms r
        ON b.room_id = r.room_id
    WHERE b.booking_id=%s
    """
    cur.execute(sql, (booking_id,))
    row = cur.fetchone()

    if row is None:
        return None

    amount = Decimal(str(row[6])) if row[6] is not None else Decimal("0.00")
    gst = amount * GST_RATE
    grand = amount + gst

    return {
        "booking_id": row[0],
        "customer": row[1],
        "room": row[2],
        "checkin": row[3],
        "checkout": row[4],
        "days": row[5],
        "amount": amount,
        "gst": gst,
        "grand": grand
    }


   