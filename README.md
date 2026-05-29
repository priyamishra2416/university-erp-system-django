# 🎓 University ERP System

A web-based University ERP (Enterprise Resource Planning) System developed using Django to simplify and digitize day-to-day academic and administrative operations within educational institutions.

This project was built as part of my Django learning journey and focuses on managing students, faculty, attendance, examination results, and fee records through a centralized dashboard.

---

## 📌 Project Overview

Managing university data manually can be time-consuming and error-prone. This ERP system provides a single platform where administrators can efficiently manage student records, track attendance, maintain faculty information, publish results, and monitor fee payments.

The project follows a modular approach, making it easy to maintain and extend with additional features in the future.

---

## ✨ Features

### 🔐 Authentication System

* User Registration
* User Login
* Secure Logout
* Session Management

### 👨‍🎓 Student Management

* Add Student
* Edit Student Information
* Delete Student
* Search Students
* Student Profile Page

### 📅 Attendance Management

* Mark Present
* Mark Absent
* Attendance History
* Student-wise Attendance Tracking

### 📊 Results Management

* Add Results
* Subject-wise Marks
* CGPA Management
* Result Records

### 📄 PDF Marksheet Generation

* Download Student Marksheet
* Printable Result Format
* Automated PDF Creation using ReportLab

### 💰 Fees Management

* Add Fee Records
* Payment Status Tracking
* Paid/Pending Status Management

### 👨‍🏫 Faculty Management

* Add Faculty
* Department Management
* Subject Assignment
* Faculty Listing

### 📈 Dashboard

* Total Students
* Total Faculty
* Total Results
* Fee Statistics
* Quick Navigation

### ⚙️ Settings Page

* User Profile Information
* Account Settings
* System Navigation

---

## 🛠️ Technology Stack

### Backend

* Python
* Django

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* SQLite

### Additional Libraries

* ReportLab (PDF Generation)

---

## 📂 Project Structure

```text
University ERP System
│
├── app/
├── static/
├── templates/
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---

## 🚀 Installation & Setup

### Clone Repository

```bash
git clone https://github.com/priyamishra2416/university-erp-system-django.git
```

### Navigate to Project

```bash
cd university-erp-system-django
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py migrate
```

### Run Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 💡 Challenges Faced During Development

While building this project, I encountered several real-world development challenges:

* URL routing issues
* Template rendering errors
* Database migration conflicts
* Authentication flow bugs
* Dynamic dashboard integration
* PDF generation implementation
* Responsive UI design challenges
* CRUD operation debugging

Solving these problems helped me gain a deeper understanding of Django's architecture and workflow.

---

## 📚 Key Learnings

Through this project, I improved my understanding of:

* Django Models
* CRUD Operations
* Authentication & Authorization
* Template Rendering
* Database Relationships
* Form Handling
* PDF Generation
* Responsive Web Design
* Project Structure & Organization

---

## 🌍 Real-World Use Case

This system can be used by schools, colleges, coaching institutes, and universities to manage academic and administrative operations digitally.

Instead of maintaining records manually, institutions can use a centralized platform to manage students, faculty, attendance, examination results, and fee information more efficiently.

---

## 👨‍💻 Author

**Priya Mishra**

Django Developer | Python Enthusiast | Building Real-World Projects

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub.
