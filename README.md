# Django E-commerce Web App Hosting

**Live Demo:** [https://farhanareekode.github.io/E-com-Host/](https://farhanareekode.github.io/E-com-Host/)  
---

## Overview

This project is a Django-based e-commerce web application hosted on AWS. The application offers a robust platform for managing products, orders, and user authentication.

---

## Features

- User registration and login
- Product listing and detailed views
- Shopping cart and checkout functionality
- Admin panel for product and order management
- Responsive design for desktop and mobile users

---

## Technologies Used

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (default) / PostgreSQL (optional for production)
- **Hosting Platform:** GitHub Pages / AWS / Custom Server

---

## How to Run Locally

### Prerequisites
- Python 3.x installed
- `pip` for package management
- `virtualenv` for creating a virtual environment
- Git installed

### Steps to Run Locally

1. **Clone the repository:**
   ```
   git clone https://github.com/farhanareekode/E-commerce.git
   cd E-commerce
   
2. **Create a virtual environment:**
Run the following command to create a virtual environment:
```
python3 -m venv env`

   *Activate the virtual environment:*
   On Linux/macOS:
   `source env/bin/activate`
   
   On Windows:
   `.\env\Scripts\activate`

4. **Install project dependencies:**
Run the following command to install all required dependencies:
   `pip install -r requirements.txt`
   
5. **Apply database migrations:**
Run the following command to apply migrations and set up the database:
   `python manage.py migrate`
   
6. **Create a superuser account:**
Run the following command to create a superuser account for accessing the admin panel:
   `python manage.py createsuperuser`
   Follow the prompts to enter a username, email, and password.
   
   Log in to the admin panel at:
   `http://127.0.0.1:8000/admin/`

7. **Run the development server:**
Start the server using the following command:
   `python manage.py runserver`

8. **Access the application in your browser:**
Open your web browser and go to:
   `http://127.0.0.1:8000/`
