# 📚 Library Management API

A modern **Library Management REST API** built with **FastAPI**, **SQLAlchemy**, and **JWT Authentication**. This project demonstrates backend development tasks including authentication, authorization, CRUD operations, pagination, searching, filtering, and role-based access control.

---

## 🚀 Features

### 🔐 Authentication & Authorization

* User registration
* Username-based login
* JWT authentication
* Password hashing with bcrypt
* Role-based authorization (Admin / User)
* Protected API endpoints

### 📖 Books

* Create, update, delete books (Admin)
* View all books
* View book details
* Search books by title, author, or ISBN
* Filter books by category
* Pagination
* Sorting
* Track available copies

### 🏷 Categories

* Create, update, delete categories
* List all categories

### 📚 Borrowing System

* Borrow books
* Return books
* Prevent borrowing unavailable books
* Track borrow history
* Manage available copies automatically

### ⭐ Reviews

* Add book reviews
* View reviews
* Update reviews
* Delete reviews

### 👥 Users

* Register new users
* User profiles
* Role management

### ⚡ API Features

* RESTful API design
* Input validation with Pydantic
* SQLite database
* Seed script with sample data
* Interactive Swagger documentation
* Automatic OpenAPI documentation

---

# 🛠 Tech Stack

* Python 3.13
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn
* Passlib (bcrypt)
* Python-JOSE (JWT)

---

# 📁 Project Structure

```text
library-management-api/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── books.py
│   │   ├── loans.py
│   │   ├── reviews.py
│   │   └── categories.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── seed.py
│   │   └── init_db.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── category.py
│   │   ├── loan.py
│   │   └── review.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── category.py
│   │   ├── loan.py
│   │   └── review.py
│   │
│   └── main.py
│
├── run.py
├── .env.example
├── requirements.txt
└── README.md
```

---

# ⚙ Installation

## Clone the repository

```bash
git clone https://github.com/matinmah-git/library-management-api.git
cd library-management-api
```

## Create a virtual environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Start the server

```bash
python run.py
```

or

```bash
uvicorn app.main:app --reload
```

---

# 🌱 Seed Sample Data

Populate the database with sample books and categories.

```bash
python -m app.database.seed
```

---

# 📖 API Documentation

After starting the server:

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# 🔑 Authentication

Login using:

```
POST /api/auth/login
```

Copy the returned JWT token.

Click **Authorize** in Swagger UI and enter:

```
Bearer YOUR_TOKEN
```

---

# 📌 Main Endpoints

## Authentication

```
POST /api/auth/register

POST /api/auth/login

POST /api/auth/me
```

---

## Books

```
GET /api/books

GET /api/books/{id}

POST /api/books

PUT /api/books/{id}

DELETE /api/books/{id}
```

---

## Categories

```
GET /api/categories

GET /api/categories/{id}

POST /api/categories

PUT /api/categories/{id}

DELETE /api/categories/{id}
```

---

## Loans

```
GET /api/loans

GET /api/loans/me 

POST /api/loans

PUT /api/loans/return/{id}

DELETE /api/loans/{id}
```

---

## Reviews

```
GET /api/reviews

GET /api/reviews/{id}

POST /api/reviews

PUT /api/reviews/{id}

DELETE /api/reviews/{id}
```

---

# 🔎 Searching

Search by title, author, or ISBN.

Example:

```
GET /api/books?search=python
```

---

# 📄 Pagination

Example:

```
GET /api/books?page=2&size=10
```

---

# 🏷 Filtering

```
GET /api/books?category_id=3

GET /api/books?available=true
```

---

# 🔃 Sorting

```
GET /api/books?sort=title

GET /api/books?sort=-created_at
```

---

# 🔒 Authorization

| Role  | Permissions                                    |
| ----- | ---------------------------------------------- |
| Admin | Full access to all resources                   |
| User  | Borrow books, review books, manage own account |

---

# 📈 Future Improvements

* Email verification
* Password reset via email
* Book reservation
* Book recommendations
* PostgreSQL support
* Rate limiting
* Dashboard statistics
* Docker support

---

# 👨‍💻 Author

**Matin Mahpour**

GitHub: https://github.com/matinmah-git
