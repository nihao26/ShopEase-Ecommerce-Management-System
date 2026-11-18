# ShopEase – E-Commerce Management System

ShopEase is an E-Commerce Management System developed using **React, Flask, Python and MySQL**. The project provides an online shopping platform with customer, seller and administrator functionalities.

## Live Demo

**Frontend:** [ShopEase – Live Website](https://shop-ease-ecommerce-management-syst.vercel.app/)

**Backend:** Deployment URL to be added.

## Project Overview

The E-Commerce Management System is designed to manage the major operations of an online shopping platform. It includes customer management, seller management, product management, shopping cart operations, order processing, product reviews and administrative functions.

The project uses React for the frontend, Flask and Python for backend operations, and MySQL for database management.

## Features

### Customer
- Customer registration and login.
- View and update customer profile.
- Browse and search products.
- Filter products based on category and price.
- Add products to the shopping cart.
- Update product quantities and remove items from the cart.
- Place orders.
- View order history and order details.
- Submit product reviews and ratings.

### Seller
- Seller login.
- View seller profile.
- View products associated with the seller.
- Manage product listings.
- View customer orders.
- Update order status.

### Administrator
- Administrator login.
- View customer and seller details.
- View products and orders.
- Add, view and delete product categories.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js |
| Backend | Python, Flask |
| Database | MySQL |
| Database Connectivity | MySQL Connector |
| API Integration | Flask API |
| Frontend Deployment | Vercel |
| Version Control | Git and GitHub |

## Project Structure

```text
ShopEase-Ecommerce-Management-System/
│
├── Backend/
│   ├── setup_database.py
│   ├── insert_data.py
│   ├── database.py
│   ├── security.py
│   ├── customer.py
│   ├── seller.py
│   ├── product.py
│   ├── cart.py
│   ├── order.py
│   ├── review.py
│   ├── admin.py
│   └── ...
│
├── Frontend/
│   └── React application files
│
├── .gitignore
└── README.md
```

## Database Setup

The project uses MySQL as its relational database.

1. Install MySQL Server.
2. Configure the database connection details in the backend configuration.
3. Install the required Python dependencies.
4. Run `setup_database.py` to create the database tables.
5. Run `insert_data.py` to insert the initial sample data.

**Note:** The setup and data insertion scripts should be executed during initial database setup, not every time the application starts.

## Running the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/nihao26/ShopEase-Ecommerce-Management-System.git
```

```bash
cd ShopEase-Ecommerce-Management-System
```

### 2. Set Up the Backend

Open a terminal and navigate to the Backend folder:

```bash
cd Backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Configure the MySQL database connection and run the database setup scripts:

```bash
python setup_database.py
```

```bash
python insert_data.py
```

Start the Flask application using the appropriate Flask application entry point.

### 3. Set Up the Frontend

Open another terminal and navigate to the Frontend folder:

```bash
cd Frontend
```

Install the dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

The frontend and backend should be configured to communicate through the Flask API.

## Deployment

- **Frontend:** Deployed using Vercel.
- **Backend:** Flask backend can be deployed separately using a Python-compatible hosting platform.
- **Database:** MySQL database must be accessible to the deployed backend.

Database credentials and other sensitive configuration details should be stored securely using environment variables and should not be committed to GitHub.

## Security

- Passwords are stored using PBKDF2-based password hashing.
- Password verification is performed during login.
- Database operations use parameterized queries.
- Customer and seller password fields are excluded from their administrative listing results.

## Contributors

This project was developed collaboratively as part of a B.Tech Computer Science and Engineering DBMS project.

- **Backend Development:** Python, MySQL and database operations.
- **Frontend Development:** React.js and user interface.
- **Integration:** Flask API and frontend-backend connectivity.

---

**ShopEase – E-Commerce Management System**

A college project demonstrating database management, backend development, frontend integration and the core operations of an online shopping platform.
