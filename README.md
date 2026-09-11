# 🏨 Aurum Hotel Management System

A complete Hotel Management System developed using **Python, Flask, MySQL, Bootstrap 5, HTML, CSS, and JavaScript**.

---

## 📌 Features

### 🔐 Authentication
- Admin Login
- Session-based Authentication
- Secure Logout

### 👥 Customer Management
- Add Customer
- View Customers
- Edit Customer
- Delete Customer
- Search Customer

### 🛏 Room Management
- Add Room
- View Rooms
- Edit Room
- Delete Room
- Search Rooms
- Room Availability Status

### 📅 Booking Management
- Add Booking
- Cancel Booking
- Search Booking
- Automatic Room Allocation
- Automatic Room Status Update

### 💰 Billing
- Automatic Bill Generation
- GST Calculation
- Invoice Generation
- Print Invoice

### 📊 Dashboard
- Live Customer Count
- Live Room Count
- Live Booking Count
- Revenue Summary
- Available vs Booked Rooms
- Charts
- Recent Bookings
- Recent Customers

---

## 🛠 Technologies Used

- Python
- Flask
- MySQL
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Chart.js

---

## 📂 Project Structure

```
HotelManagement/
│── app.py             # Flask Web Application & Routes
│── schema.sql         # MySQL Database Schema & Seed Data
│── create_admin.py    # Admin User Creation CLI Tool
│── main.py            # Interactive Customer Management CLI
│── database.py        # Database Connection & Query Helpers
│── config.py          # Environment Configurations
│── login.py           # Admin Authentication Logic
│── customer.py        # Customer CRUD Operations
│── room.py            # Room Management Logic
│── booking.py         # Booking Lifecycle & Date Availability
│── billing.py         # Billing & Invoice Generation
│── dashboard.py       # Metrics & Analytics Queries
│── requirements.txt   # Python Dependencies
│
├── templates/         # HTML Jinja2 Templates
├── static/            # CSS, JavaScript & Static Images
│   ├── css/
│   ├── images/
│
└── README.md
```

---

## 🚀 How to Run

1. Clone the repository:

```bash
git clone <repository-url>
cd hotel-management-system-flask-main
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your MySQL credentials in `.env`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=hotel_management
SECRET_KEY=your_secret_key
```

4. Import the MySQL database schema:

```bash
mysql -u root -p < schema.sql
```

5. (Optional) Create or reset an Admin User:

```bash
python create_admin.py admin admin123
```
*Default login:* Username: `admin` | Password: `admin123`

6. Run the Web Application:

```bash
python app.py
```

7. Open in your browser:

```
http://127.0.0.1:5000
```

*(Optional)* You can also run the terminal CLI utility:

```bash
python main.py
```

---

## 👨‍💻 Developed By

**Suhail Shaik**

MCA Student

Python | Flask | MySQL Developer