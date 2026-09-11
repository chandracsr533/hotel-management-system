# 🏨 Aurum Hotel Management System

A web-based **Hotel Management System** built with **Python, Flask, MySQL, Bootstrap 5, HTML, CSS, and JavaScript**.

The system provides an admin interface for managing hotel customers, rooms, bookings, billing, invoices, and reports from a centralized dashboard.

---

## 📌 Project Overview

The **Aurum Hotel Management System** is designed to simplify common hotel administration tasks through a web-based application.

Administrators can manage customer information, maintain room details, create and cancel bookings, calculate bills with GST, generate invoices, and view hotel statistics and reports.

The application uses **Flask** for the backend, **MySQL** for data storage, **Jinja2** templates for dynamic web pages, and **Bootstrap 5** for the user interface.

---

## ✨ Features

### 🔐 Admin Authentication

- Admin login
- Session-based authentication
- Protected application routes
- Secure logout
- Password hashing using Werkzeug
- Environment-based secret key configuration

### 👥 Customer Management

- Add customers
- View customer records
- Edit customer information
- Delete customers
- Search customers
- Store customer contact and address details

### 🛏️ Room Management

- Add rooms
- View room details
- Edit room information
- Delete rooms
- Search rooms
- Store room type and pricing
- Track room floor and description
- Maintain room availability status
- Prevent duplicate room numbers

### 📅 Booking Management

- Create hotel bookings
- Select customers and rooms
- Check-in and check-out date validation
- Calculate total stay duration automatically
- Calculate booking amount automatically
- Date-based room availability
- Prevent overlapping bookings for the same room
- Cancel bookings
- Search bookings
- Automatically update room status when applicable

### 💰 Billing & Invoices

- Automatic bill generation
- Room charge calculation
- 18% GST calculation
- Grand total calculation
- Invoice generation
- Invoice details based on booking information
- Print invoice functionality

### 📊 Dashboard & Reports

- Total customer count
- Total room count
- Total booking count
- Revenue summary
- Available room count
- Booked room count
- Recent bookings
- Recent customers
- Monthly revenue report
- Booking status report
- Room type report
- Interactive charts using Chart.js
- Printable reports

---

## 🛠️ Technologies Used

### Backend

- Python 3
- Flask
- MySQL
- mysql-connector-python
- Werkzeug
- python-dotenv

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Jinja2
- Font Awesome

### Data Visualization

- Chart.js

---

## 🏗️ Project Architecture

The project follows a modular structure where different Python files handle different parts of the application.

```text
hotel-management-system-flask-main/
│
├── app.py                 # Flask application and routes
├── config.py              # Environment configuration
├── database.py            # MySQL connection and cursor handling
├── login.py               # Admin authentication
├── customer.py            # Customer CRUD and search operations
├── room.py                # Room management operations
├── booking.py             # Booking and availability logic
├── billing.py             # Billing and invoice calculations
├── dashboard.py           # Dashboard metrics and reports
├── create_admin.py        # Admin account creation utility
│
├── schema.sql             # MySQL database schema
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignored files
├── README.md              # Project documentation
│
├── templates/             # Jinja2 HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── customers.html
│   ├── add_customer.html
│   ├── edit_customer.html
│   ├── rooms.html
│   ├── add_room.html
│   ├── edit_room.html
│   ├── bookings.html
│   ├── add_booking.html
│   ├── billing.html
│   ├── invoice.html
│   └── reports.html
│
└── static/
    ├── css/               # Stylesheets
    └── images/            # Static images