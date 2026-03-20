# LAB11

A Flask-based e-commerce web application with user authentication, product browsing, shopping basket, and order management.

## Features

- **User Authentication** – Register, log in, log out, and "remember me" cookie support
- **Product Catalog** – Browse products with pagination
- **Shopping Basket** – Add, remove, increment, and decrement items
- **Checkout & Orders** – Place orders and view order history

## Tech Stack

- **Backend**: Python 3, Flask
- **Database**: MariaDB / MySQL (via PyMySQL)
- **Forms**: Flask-WTF / WTForms
- **Email**: Flask-Mail
- **Deployment**: WSGI (`app.wsgi`)

## Requirements

- Python 3.8+
- MariaDB or MySQL server

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/JoaoSouza129/LAB11.git
   cd LAB11
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**

   Create a database and import the schema:

   ```bash
   mysql -u <user> -p <database_name> < schema.sql
   ```

5. **Configure the application**

   Set the required environment variables (or update `__init__.py`):

   | Variable | Description |
   |---|---|
   | `SECRET_KEY` | Flask secret key for session signing |
   | Database credentials | Connection details used in `db_auth.py` and `db_store.py` |

6. **Run the development server**

   ```bash
   flask --app LAB11 run
   ```

   The application will be available at `http://127.0.0.1:5000`.

## Project Structure

```
LAB11/
├── __init__.py        # Application factory
├── auth.py            # Authentication routes (register, login, logout)
├── store.py           # Store routes (index, basket, checkout, orders)
├── db_auth.py         # Database helpers for authentication
├── db_store.py        # Database helpers for the store
├── schema.sql         # Database schema
├── app.wsgi           # WSGI entry point for deployment
├── requirements.txt   # Python dependencies
├── static/            # Static assets (CSS, images, JS)
└── templates/         # Jinja2 HTML templates
    ├── base.html
    ├── auth/
    └── shop/
```

## Routes

| Method | Path | Description |
|---|---|---|
| GET/POST | `/auth/register` | Create a new account |
| GET/POST | `/auth/login` | Log in |
| GET | `/auth/logout` | Log out |
| GET | `/` | Product listing (paginated) |
| GET | `/checkout` | View shopping basket |
| POST | `/order` | Place an order |
| GET | `/orders` | View past orders |
| GET | `/add/<id>` | Add a product to the basket |
| GET | `/remove/<id>` | Remove a product from the basket |
| GET | `/increment/<id>` | Increase quantity of a basket item |
| GET | `/decrement/<id>` | Decrease quantity of a basket item |
| GET | `/empty` | Empty the basket |
