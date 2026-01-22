# Student Housing Management System

A robust Django-based web application for managing student housing, including registration, room booking, payment tracking, and complaints.

## 🚀 Features

- **Role-Based Access Control (RBAC)**: Distinct panels for Students, Supervisors, and Admins.
- **Housing Management**: Manage Buildings, Rooms, and Occupancy.
- **Application Workflow**: Student registration approval flow.
- **Security**:
    - OWASP Top 10 protection (SQLi, XSS, CSRF).
    - Login Rate Limiting (Axes).
    - Session Security.
- **UX/UI**: Modern, responsive interface using Bootstrap 5 (RTL support).

## 🛠 Prerequisites

- Python 3.10+
- Django 5.0+

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/StudentHousingManager.git
    cd StudentHousingManager
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Migrations**:
    ```bash
    python manage.py migrate
    ```
    *Note: This will also set up the Axes and Auth tables.*

5.  **Create Superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run Development Server**:
    ```bash
    python manage.py runserver
    ```

## 🔐 Security Configuration

This project is configured for **Production Readiness**:
- Set `DEBUG = False` in environment variables for production.
- **Rate Limiting**: Accounts will be locked after 5 failed login attempts.
- **Headers**: Strict security headers are enabled when `DEBUG = False`.

## 📂 Project Structure

- `accounts/`: User authentication and profiles.
- `housing/`: Building and Room management.
- `applications/`: Student application processing.
- `core/`: Dashboard and home views.

---
*Developed for Academic Final Evaluation*
