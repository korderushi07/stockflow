<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

# ============================================
# PAGE ROUTES
# ============================================

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/sales")
def sales():
    return render_template("sales.html")

@app.route("/alerts")
def alerts():
    return render_template("alerts.html")


# ============================================
# API ROUTES — PRODUCTS
# ============================================

@app.route("/api/products", methods=["GET"])
def get_products():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vw_product_details")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products)

@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.json
    name          = data.get("name", "").strip()
    category_id   = int(data.get("category_id") or 0)
    supplier_id   = int(data.get("supplier_id") or 0)
    price         = float(data.get("price") or 0)
    stock_qty     = int(data.get("stock_qty") or 0)
    reorder_level = int(data.get("reorder_level") or 10)
    unit          = data.get("unit", "pcs").strip()

    if not name or category_id == 0 or supplier_id == 0 or price == 0:
        return jsonify({"error": "Please fill in all required fields!"}), 400

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, category_id, supplier_id, price, stock_qty, reorder_level, unit)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (name, category_id, supplier_id, price, stock_qty, reorder_level, unit))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Product '{name}' added successfully!"})


# ============================================
# API ROUTES — SALES
# ============================================

@app.route("/api/sales", methods=["GET"])
def get_sales():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.sale_id, p.name AS product, c.full_name AS customer,
               s.quantity_sold, s.total_amount, s.sale_date
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        JOIN customers c ON s.customer_id = c.customer_id
        ORDER BY s.sale_date DESC
    """)
    sales = cursor.fetchall()
    for sale in sales:
        if sale["sale_date"]:
            sale["sale_date"] = str(sale["sale_date"])
    cursor.close()
    conn.close()
    return jsonify(sales)

@app.route("/api/sales", methods=["POST"])
def add_sale():
    data = request.json
    product_id    = int(data.get("product_id") or 0)
    customer_id   = int(data.get("customer_id") or 0)
    quantity_sold = int(data.get("quantity_sold") or 1)

    if product_id == 0 or customer_id == 0:
        return jsonify({"error": "Please select a product and customer!"}), 400

    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT price, stock_qty, name FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()

    if not product:
        return jsonify({"error": "Product not found!"}), 404

    if quantity_sold > product["stock_qty"]:
        return jsonify({"error": f"Not enough stock! Only {product['stock_qty']} units available."}), 400

    total = float(product["price"]) * quantity_sold

    cursor.execute("""
        INSERT INTO sales (product_id, customer_id, quantity_sold, total_amount)
        VALUES (%s, %s, %s, %s)
    """, (product_id, customer_id, quantity_sold, total))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Sale recorded! Stock auto-updated by SQL trigger."})


# ============================================
# API ROUTES — ALERTS
# ============================================

@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT sa.alert_id, p.name AS product,
               sa.alert_message, sa.alert_time, sa.is_resolved
        FROM stock_alerts sa
        JOIN products p ON sa.product_id = p.product_id
        ORDER BY sa.alert_time DESC
    """)
    alerts = cursor.fetchall()
    for alert in alerts:
        if alert["alert_time"]:
            alert["alert_time"] = str(alert["alert_time"])
    cursor.close()
    conn.close()
    return jsonify(alerts)

@app.route("/api/alerts/<int:alert_id>/resolve", methods=["POST"])
def resolve_alert(alert_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE stock_alerts SET is_resolved = TRUE WHERE alert_id = %s", (alert_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Alert resolved!"})


# ============================================
# API ROUTES — DASHBOARD STATS
# ============================================

@app.route("/api/stats", methods=["GET"])
def get_stats():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM products")
    total_products = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM sales")
    total_sales = cursor.fetchone()["total"]

    cursor.execute("SELECT COALESCE(SUM(total_amount), 0) AS total FROM sales")
    total_revenue = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM stock_alerts WHERE is_resolved = FALSE")
    active_alerts = cursor.fetchone()["total"]

    cursor.close()
    conn.close()
    return jsonify({
        "total_products": total_products,
        "total_sales": total_sales,
        "total_revenue": float(total_revenue),
        "active_alerts": active_alerts
    })


# ============================================
# API ROUTES — DROPDOWNS
# ============================================

@app.route("/api/categories", methods=["GET"])
def get_categories():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route("/api/suppliers", methods=["GET"])
def get_suppliers():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM suppliers WHERE is_active = TRUE")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route("/api/customers", methods=["GET"])
def get_customers():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)


if __name__ == "__main__":
=======
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

# ============================================
# PAGE ROUTES
# ============================================

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/sales")
def sales():
    return render_template("sales.html")

@app.route("/alerts")
def alerts():
    return render_template("alerts.html")


# ============================================
# API ROUTES — PRODUCTS
# ============================================

@app.route("/api/products", methods=["GET"])
def get_products():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vw_product_details")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products)

@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.json
    name          = data.get("name", "").strip()
    category_id   = int(data.get("category_id") or 0)
    supplier_id   = int(data.get("supplier_id") or 0)
    price         = float(data.get("price") or 0)
    stock_qty     = int(data.get("stock_qty") or 0)
    reorder_level = int(data.get("reorder_level") or 10)
    unit          = data.get("unit", "pcs").strip()

    if not name or category_id == 0 or supplier_id == 0 or price == 0:
        return jsonify({"error": "Please fill in all required fields!"}), 400

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, category_id, supplier_id, price, stock_qty, reorder_level, unit)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (name, category_id, supplier_id, price, stock_qty, reorder_level, unit))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Product '{name}' added successfully!"})


# ============================================
# API ROUTES — SALES
# ============================================

@app.route("/api/sales", methods=["GET"])
def get_sales():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.sale_id, p.name AS product, c.full_name AS customer,
               s.quantity_sold, s.total_amount, s.sale_date
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        JOIN customers c ON s.customer_id = c.customer_id
        ORDER BY s.sale_date DESC
    """)
    sales = cursor.fetchall()
    for sale in sales:
        if sale["sale_date"]:
            sale["sale_date"] = str(sale["sale_date"])
    cursor.close()
    conn.close()
    return jsonify(sales)

@app.route("/api/sales", methods=["POST"])
def add_sale():
    data = request.json
    product_id    = int(data.get("product_id") or 0)
    customer_id   = int(data.get("customer_id") or 0)
    quantity_sold = int(data.get("quantity_sold") or 1)

    if product_id == 0 or customer_id == 0:
        return jsonify({"error": "Please select a product and customer!"}), 400

    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT price, stock_qty, name FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()

    if not product:
        return jsonify({"error": "Product not found!"}), 404

    if quantity_sold > product["stock_qty"]:
        return jsonify({"error": f"Not enough stock! Only {product['stock_qty']} units available."}), 400

    total = float(product["price"]) * quantity_sold

    cursor.execute("""
        INSERT INTO sales (product_id, customer_id, quantity_sold, total_amount)
        VALUES (%s, %s, %s, %s)
    """, (product_id, customer_id, quantity_sold, total))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Sale recorded! Stock auto-updated by SQL trigger."})


# ============================================
# API ROUTES — ALERTS
# ============================================

@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT sa.alert_id, p.name AS product,
               sa.alert_message, sa.alert_time, sa.is_resolved
        FROM stock_alerts sa
        JOIN products p ON sa.product_id = p.product_id
        ORDER BY sa.alert_time DESC
    """)
    alerts = cursor.fetchall()
    for alert in alerts:
        if alert["alert_time"]:
            alert["alert_time"] = str(alert["alert_time"])
    cursor.close()
    conn.close()
    return jsonify(alerts)

@app.route("/api/alerts/<int:alert_id>/resolve", methods=["POST"])
def resolve_alert(alert_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE stock_alerts SET is_resolved = TRUE WHERE alert_id = %s", (alert_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Alert resolved!"})


# ============================================
# API ROUTES — DASHBOARD STATS
# ============================================

@app.route("/api/stats", methods=["GET"])
def get_stats():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM products")
    total_products = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM sales")
    total_sales = cursor.fetchone()["total"]

    cursor.execute("SELECT COALESCE(SUM(total_amount), 0) AS total FROM sales")
    total_revenue = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM stock_alerts WHERE is_resolved = FALSE")
    active_alerts = cursor.fetchone()["total"]

    cursor.close()
    conn.close()
    return jsonify({
        "total_products": total_products,
        "total_sales": total_sales,
        "total_revenue": float(total_revenue),
        "active_alerts": active_alerts
    })


# ============================================
# API ROUTES — DROPDOWNS
# ============================================

@app.route("/api/categories", methods=["GET"])
def get_categories():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route("/api/suppliers", methods=["GET"])
def get_suppliers():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM suppliers WHERE is_active = TRUE")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route("/api/customers", methods=["GET"])
def get_customers():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)


if __name__ == "__main__":
>>>>>>> e9850321be0d01f9bf24ae43ecd6dadbc2d1cb06
    app.run(debug=True)