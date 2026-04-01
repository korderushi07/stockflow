<div align="center">

# 📦 Inventory Pro

### A full-stack Inventory Management System built with Python Flask, MySQL, and vanilla JavaScript.

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge&logo=mysql)
![HTML](https://img.shields.io/badge/HTML%2FCSS%2FJS-Frontend-red?style=for-the-badge&logo=html5)

</div>

---

## 🖥️ Project Overview

**Inventory Pro** is a real-world inventory management system that allows businesses to track products, manage stock, record sales, and receive automatic low-stock alerts — all powered by a MySQL relational database with Triggers and Views.

---

## ✨ Features

- 📦 **Product Management** — Add products with category, supplier, price, and stock info
- 🛒 **Sales Recording** — Record sales with automatic stock reduction via SQL Trigger
- 🚨 **Low Stock Alerts** — Auto-generated alerts when stock falls below reorder level
- 📊 **Live Dashboard** — Charts showing stock levels and revenue per product
- 🔁 **Stock Transaction Log** — Full audit trail of every stock IN/OUT movement
- 🌙 **Dark UI** — Clean dark-themed dashboard with sidebar navigation

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python, Flask, Flask-CORS |
| **Database** | MySQL |
| **DB Library** | mysql-connector-python |
| **UI Framework** | Custom dark CSS + Chart.js |

---

## 🗄️ Database Design

### Tables (7)

| Table | Description |
|---|---|
| `suppliers` | Supplier details and contact info |
| `categories` | Product categories |
| `products` | Main product inventory |
| `customers` | Customer information |
| `sales` | Sales transactions |
| `stock_transactions` | Full stock movement history |
| `stock_alerts` | Auto-generated low stock alerts |

### SQL Views (3)

| View | Purpose |
|---|---|
| `vw_product_details` | Products joined with category and supplier |
| `vw_low_stock` | Products below reorder level with supplier contact |
| `vw_sales_summary` | Revenue and units sold per product |

### SQL Triggers (3)

| Trigger | When it fires | What it does |
|---|---|---|
| `trg_reduce_stock` | After INSERT on sales | Auto-reduces product stock |
| `trg_low_stock_alert` | After UPDATE on products | Creates alert if stock < reorder level |
| `trg_stock_in_log` | After UPDATE on products | Logs restock in transaction history |

---

## 📁 Folder Structure
```
inventory-pro/
│
├── app.py                  ← Flask backend (all API routes)
│
├── templates/
│   ├── index.html          ← Dashboard with charts
│   ├── products.html       ← Product management
│   ├── sales.html          ← Sales recording
│   └── alerts.html         ← Low stock alerts
│
└── static/
    └── css/
        └── style.css       ← Dark theme styles
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.x
- MySQL Server
- Git

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/inventory-pro.git
cd inventory-pro
```

### 2. Install dependencies
```bash
pip install flask mysql-connector-python flask-cors
```

### 3. Setup the MySQL database

Open MySQL and run:
```sql
CREATE DATABASE InventoryDB;
USE InventoryDB;
```

Then create all tables, views, and triggers as per the schema.

### 4. Create your db.py file

Create a file called `db.py` in the root folder:
```python
import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="InventoryDB"
    )
    return connection
```

### 5. Run the application
```bash
python app.py
```

Open your browser and go to:
```
http://127.0.0.1:5000
```

---

## 📸 Pages

| Page | URL | Description |
|---|---|---|
| Dashboard | `/` | Stats, charts, product and sales overview |
| Products | `/products` | Add and view all products |
| Sales | `/sales` | Record sales, trigger auto-fires |
| Alerts | `/alerts` | Low stock warnings and alert log |

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/products` | Fetch all products |
| POST | `/api/products` | Add a new product |
| GET | `/api/sales` | Fetch all sales |
| POST | `/api/sales` | Record a new sale |
| GET | `/api/alerts` | Fetch all stock alerts |
| POST | `/api/alerts/<id>/resolve` | Resolve an alert |
| GET | `/api/stats` | Dashboard statistics |
| GET | `/api/categories` | All categories |
| GET | `/api/suppliers` | All active suppliers |
| GET | `/api/customers` | All customers |

---

Made with ❤️ as a database project submission.

> **Note:** `db.py` is excluded from this repository as it contains database credentials. Create your own as shown above.
