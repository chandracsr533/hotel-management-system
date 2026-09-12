from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from config import SECRET_KEY

from login import admin_login

from dashboard import (
    dashboard_counts,
    recent_bookings,
    recent_customers,
    report_summary,
    monthly_revenue,
    booking_status_report,
    room_type_report
)

from customer import (
    get_customers,
    insert_customer,
    get_customer_by_id,
    update_customer,
    delete_customer,
    search_customer
)

from room import (
    get_rooms,
    insert_room,
    get_room_by_id,
    update_room,
    delete_room,
    search_room
)

from booking import (
    get_bookings,
    get_customer_list,
    get_available_rooms,
    insert_booking,
    delete_booking,
    search_booking
)

from billing import (
    get_bill_data,
    get_invoice
)


# ================= APPLICATION ================= #

app = Flask(__name__)

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not configured. Please check your .env file."
    )

app.secret_key = SECRET_KEY


# ================= AUTHENTICATION ================= #

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "admin" not in session:
            flash(
                "Please log in to access this page.",
                "warning"
            )
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function


# ================= HOME ================= #

@app.route("/")
def home():
    return render_template("index.html")


# ================= LOGIN ================= #

@app.route("/login", methods=["GET", "POST"])
def login():

    if "admin" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if admin_login(username, password):

            session["admin"] = username

            flash(
                f"Welcome, {username}!",
                "success"
            )

            return redirect(url_for("dashboard"))

        flash(
            "Invalid Username or Password",
            "danger"
        )

    return render_template("login.html")


# ================= LOGOUT ================= #

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out successfully.",
        "info"
    )

    return redirect(url_for("login"))


# ================= DASHBOARD ================= #

@app.route("/dashboard")
@login_required
def dashboard():

    data = dashboard_counts()
    recent = recent_bookings()
    customers = recent_customers()

    return render_template(
        "dashboard.html",
        data=data,
        recent=recent,
        customers=customers
    )


# ================= CUSTOMERS ================= #

@app.route("/customers")
@login_required
def customers():

    keyword = request.args.get(
        "search",
        ""
    ).strip()

    if keyword:
        data = search_customer(keyword)
    else:
        data = get_customers()

    return render_template(
        "customers.html",
        customers=data
    )


@app.route("/add_customer", methods=["GET", "POST"])
@login_required
def add_customer():

    if request.method == "POST":

        data = (
            request.form.get(
                "customer_name",
                ""
            ).strip(),

            request.form.get(
                "gender",
                "Male"
            ),

            request.form.get(
                "mobile",
                ""
            ).strip(),

            request.form.get(
                "email",
                ""
            ).strip(),

            request.form.get(
                "address",
                ""
            ).strip(),

            request.form.get(
                "city",
                ""
            ).strip(),

            request.form.get(
                "check_in_date"
            ) or None
        )

        success, msg = insert_customer(data)

        if success:

            flash(msg, "success")

            return redirect(
                url_for("customers")
            )

        flash(msg, "danger")

    return render_template(
        "add_customer.html"
    )


@app.route(
    "/edit_customer/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_customer(id):

    if request.method == "POST":

        data = (
            request.form.get(
                "customer_name",
                ""
            ).strip(),

            request.form.get(
                "gender",
                "Male"
            ),

            request.form.get(
                "mobile",
                ""
            ).strip(),

            request.form.get(
                "email",
                ""
            ).strip(),

            request.form.get(
                "address",
                ""
            ).strip(),

            request.form.get(
                "city",
                ""
            ).strip(),

            request.form.get(
                "check_in_date"
            ) or None,

            id
        )

        success, msg = update_customer(data)

        if success:

            flash(msg, "success")

            return redirect(
                url_for("customers")
            )

        flash(msg, "danger")

    customer = get_customer_by_id(id)

    if not customer:

        flash(
            "Customer not found.",
            "warning"
        )

        return redirect(
            url_for("customers")
        )

    return render_template(
        "edit_customer.html",
        customer=customer
    )


@app.route("/delete_customer/<int:id>")
@login_required
def delete_customer_route(id):

    success, msg = delete_customer(id)

    flash(
        msg,
        "success" if success else "danger"
    )

    return redirect(
        url_for("customers")
    )


# ================= ROOMS ================= #

@app.route("/rooms")
@login_required
def rooms():

    keyword = request.args.get(
        "search",
        ""
    ).strip()

    if keyword:
        data = search_room(keyword)
    else:
        data = get_rooms()

    return render_template(
        "rooms.html",
        rooms=data
    )


@app.route("/add_room", methods=["GET", "POST"])
@login_required
def add_room():

    if request.method == "POST":

        data = (
            request.form.get(
                "room_number",
                ""
            ).strip(),

            request.form.get(
                "room_type",
                "Single"
            ),

            request.form.get(
                "room_price",
                0
            ),

            request.form.get(
                "room_status",
                "Available"
            ),

            request.form.get(
                "floor_number",
                1
            ),

            request.form.get(
                "room_description",
                ""
            ).strip()
        )

        success, msg = insert_room(data)

        if success:

            flash(msg, "success")

            return redirect(
                url_for("rooms")
            )

        flash(msg, "danger")

    return render_template(
        "add_room.html"
    )


@app.route(
    "/edit_room/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_room(id):

    if request.method == "POST":

        data = (
            request.form.get(
                "room_number",
                ""
            ).strip(),

            request.form.get(
                "room_type",
                "Single"
            ),

            request.form.get(
                "room_price",
                0
            ),

            request.form.get(
                "room_status",
                "Available"
            ),

            request.form.get(
                "floor_number",
                1
            ),

            request.form.get(
                "room_description",
                ""
            ).strip(),

            id
        )

        success, msg = update_room(data)

        if success:

            flash(msg, "success")

            return redirect(
                url_for("rooms")
            )

        flash(msg, "danger")

    room = get_room_by_id(id)

    if not room:

        flash(
            "Room not found.",
            "warning"
        )

        return redirect(
            url_for("rooms")
        )

    return render_template(
        "edit_room.html",
        room=room
    )


@app.route("/delete_room/<int:room_id>")
@login_required
def remove_room(room_id):

    success, msg = delete_room(room_id)

    flash(
        msg,
        "success" if success else "danger"
    )

    return redirect(
        url_for("rooms")
    )


# ================= BOOKINGS ================= #

@app.route("/bookings")
@login_required
def bookings():

    keyword = request.args.get(
        "search",
        ""
    ).strip()

    if keyword:
        data = search_booking(keyword)
    else:
        data = get_bookings()

    return render_template(
        "bookings.html",
        bookings=data
    )


@app.route("/add_booking", methods=["GET", "POST"])
@login_required
def add_booking():

    if request.method == "POST":

        data = (
            request.form.get("customer_id"),
            request.form.get("room_id"),
            request.form.get("check_in_date"),
            request.form.get("check_out_date")
        )

        success, message = insert_booking(data)

        if success:

            flash(
                message,
                "success"
            )

            return redirect(
                url_for("bookings")
            )

        flash(
            message,
            "danger"
        )

    customers = get_customer_list()

    check_in = request.args.get(
        "check_in_date"
    )

    check_out = request.args.get(
        "check_out_date"
    )

    rooms = get_available_rooms(
        check_in,
        check_out
    )

    return render_template(
        "add_booking.html",
        customers=customers,
        rooms=rooms
    )


@app.route("/delete_booking/<int:id>")
@login_required
def delete_booking_route(id):

    success, msg = delete_booking(id)

    flash(
        msg,
        "success" if success else "danger"
    )

    return redirect(
        url_for("bookings")
    )


# ================= BILLING ================= #

@app.route("/billing")
@login_required
def billing():

    data = get_bill_data()

    return render_template(
        "billing.html",
        bills=data
    )


@app.route("/invoice/<int:booking_id>")
@login_required
def invoice(booking_id):

    bill = get_invoice(
        booking_id
    )

    if bill is None:

        flash(
            "Invoice not found for this booking ID.",
            "warning"
        )

        return redirect(
            url_for("billing")
        )

    return render_template(
        "invoice.html",
        bill=bill
    )


# ================= REPORTS ================= #

@app.route("/reports")
@login_required
def reports():

    summary = report_summary()
    revenue = monthly_revenue()
    booking_status = booking_status_report()
    room_types = room_type_report()

    return render_template(
        "reports.html",
        summary=summary,
        revenue=revenue,
        booking_status=booking_status,
        room_types=room_types
    )


# ================= RUN APPLICATION ================= #

if __name__ == "__main__":
    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )