import mysql.connector
from database import get_connection, get_cursor


# ===============================
# Get All Customers
# ===============================

def get_customers():
    cur = get_cursor()
    sql = "SELECT * FROM customers ORDER BY customer_id DESC"
    cur.execute(sql)
    return cur.fetchall()


# Alias for CLI / backwards compatibility
view_customers = get_customers


# ===============================
# Search Customer
# ===============================

def search_customer(keyword):
    cur = get_cursor()
    sql = """
    SELECT *
    FROM customers
    WHERE
        customer_name LIKE %s
        OR mobile LIKE %s
        OR email LIKE %s
        OR city LIKE %s
    ORDER BY customer_id DESC
    """
    value = "%" + keyword + "%"
    cur.execute(sql, (value, value, value, value))
    return cur.fetchall()


# ===============================
# Insert Customer
# ===============================

def insert_customer(data):
    conn = get_connection()
    cur = get_cursor()
    sql = """
    INSERT INTO customers
    (
        customer_name,
        gender,
        mobile,
        email,
        address,
        city,
        check_in_date
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s)
    """
    try:
        cur.execute(sql, data)
        conn.commit()
        return True, "Customer added successfully."
    except mysql.connector.Error as err:
        conn.rollback()
        return False, f"Database error: {err}"


# Alias for backwards compatibility
add_customer = insert_customer


# ===============================
# Get Customer By ID
# ===============================

def get_customer_by_id(customer_id):
    cur = get_cursor()
    sql = """
    SELECT *
    FROM customers
    WHERE customer_id=%s
    """
    cur.execute(sql, (customer_id,))
    return cur.fetchone()


# ===============================
# Update Customer
# ===============================

def update_customer(data):
    conn = get_connection()
    cur = get_cursor()
    sql = """
    UPDATE customers
    SET
        customer_name=%s,
        gender=%s,
        mobile=%s,
        email=%s,
        address=%s,
        city=%s,
        check_in_date=%s
    WHERE customer_id=%s
    """
    try:
        cur.execute(sql, data)
        conn.commit()
        return True, "Customer updated successfully."
    except mysql.connector.Error as err:
        conn.rollback()
        return False, f"Database error: {err}"


# ===============================
# Delete Customer
# ===============================

def delete_customer(customer_id):
    conn = get_connection()
    cur = get_cursor()
    sql = "DELETE FROM customers WHERE customer_id=%s"
    try:
        cur.execute(sql, (customer_id,))
        conn.commit()
        return True, "Customer deleted successfully."
    except mysql.connector.IntegrityError:
        return False, "Cannot delete customer because they have existing bookings."
    except mysql.connector.Error as err:
        conn.rollback()
        return False, f"Database error: {err}"