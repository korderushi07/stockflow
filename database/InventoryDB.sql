CREATE DATABASE InventoryDB;
USE InventoryDB;

CREATE TABLE suppliers (
    supplier_id   INT PRIMARY KEY AUTO_INCREMENT,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(100) UNIQUE NOT NULL,
    phone         VARCHAR(20),
    city          VARCHAR(50),
    country       VARCHAR(50) DEFAULT 'India',
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    category_id   INT PRIMARY KEY AUTO_INCREMENT,
    name          VARCHAR(100) NOT NULL,
    description   TEXT
);

CREATE TABLE products (
    product_id    INT PRIMARY KEY AUTO_INCREMENT,
    name          VARCHAR(150) NOT NULL,
    category_id   INT,
    supplier_id   INT,
    price         DECIMAL(10,2) NOT NULL,
    stock_qty     INT DEFAULT 0,
    reorder_level INT DEFAULT 10,
    unit          VARCHAR(30),
    discount      DECIMAL(5,2) DEFAULT 0.00,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE customers (
    customer_id   INT PRIMARY KEY AUTO_INCREMENT,
    full_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(100) UNIQUE,
    phone         VARCHAR(20),
    city          VARCHAR(50),
    address       TEXT
);

CREATE TABLE sales (
    sale_id       INT PRIMARY KEY AUTO_INCREMENT,
    product_id    INT,
    customer_id   INT,
    quantity_sold INT NOT NULL,
    sale_date     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount  DECIMAL(10,2),
    FOREIGN KEY (product_id)  REFERENCES products(product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

use inventorydb;

CREATE TABLE stock_transactions (
    txn_id        INT PRIMARY KEY AUTO_INCREMENT,
    product_id    INT,
    txn_type      ENUM('IN', 'OUT') NOT NULL,
    quantity      INT NOT NULL,
    txn_date      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    remarks       VARCHAR(255),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE stock_alerts (
    alert_id      INT PRIMARY KEY AUTO_INCREMENT,
    product_id    INT,
    alert_message VARCHAR(255),
    alert_time    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_resolved   BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

SHOW TABLES;

INSERT INTO suppliers (name, email, phone, city, country) VALUES
('RajTech Supplies',      'raj@rajtech.in',       '9876501234', 'Mumbai',    'India'),
('PrimeMart Goods',       'prime@primemart.in',    '9823400001', 'Delhi',     'India'),
('Sunrise Distributors',  'sunrise@sd.in',         '9012300002', 'Pune',      'India'),
('GlobalStock Co.',       'gs@globalstock.in',     '9345600003', 'Chennai',   'India'),
('BlueStar Traders',      'blue@bluestar.in',      '9456700004', 'Hyderabad', 'India'),
('NexGen Suppliers',      'nexgen@nexgen.in',      '9567800005', 'Kolkata',   'India'),
('EverGreen Wholesale',   'ever@evergreen.in',     '9678900006', 'Jaipur',    'India'),
('FastTrack Logistics',   'fast@fasttrack.in',     '9789000007', 'Surat',     'India'),
('PeakPoint Enterprises', 'peak@peakpoint.in',     '9890100008', 'Nagpur',    'India'),
('SkyHigh Distributors',  'sky@skyhigh.in',        '9901200009', 'Lucknow',   'India');

INSERT INTO categories (name, description) VALUES
('Electronics',   'Gadgets, devices and accessories'),
('Groceries',     'Daily use food and household items'),
('Stationery',    'Office and school supplies'),
('Clothing',      'Apparel and fashion items'),
('Furniture',     'Home and office furniture'),
('Sports',        'Sports and fitness equipment'),
('Toys',          'Kids toys and games'),
('Medicine',      'Healthcare and pharmacy products'),
('Automotive',    'Car and bike accessories'),
('Cosmetics',     'Skincare and beauty products');

INSERT INTO products (name, category_id, supplier_id, price, stock_qty, reorder_level, unit) VALUES
('Wireless Mouse',        1,  1,  599.00,  50,  10, 'pcs'),
('USB-C Hub',             1,  1,  999.00,  30,   8, 'pcs'),
('Basmati Rice 5kg',      2,  3,  350.00, 100,  20, 'bag'),
('Sunflower Oil 1L',      2,  3,  180.00,  60,  15, 'bottle'),
('A4 Paper Ream',         3,  2,  250.00,  40,  10, 'ream'),
('Ball Pen Pack 10',      3,  2,   80.00,  80,  20, 'pack'),
('Men T-Shirt',           4,  4,  499.00,  25,   5, 'pcs'),
('Women Kurti',           4,  4,  799.00,  15,   5, 'pcs'),
('Office Chair',          5,  5, 4999.00,  10,   3, 'pcs'),
('Cricket Bat',           6,  6, 1299.00,  20,   5, 'pcs');

INSERT INTO customers (full_name, email, phone, city, address) VALUES
('Aarav Singh',    'aarav@gmail.com',   '9001122334', 'Mumbai',    '12 MG Road, Andheri'),
('Diya Nair',      'diya@gmail.com',    '9112233445', 'Pune',      '45 FC Road, Shivajinagar'),
('Rohan Verma',    'rohan@gmail.com',   '9223344556', 'Delhi',     '78 Connaught Place'),
('Meera Joshi',    'meera@gmail.com',   '9334455667', 'Bangalore', '23 Brigade Road'),
('Karan Malhotra', 'karan@gmail.com',   '9445566778', 'Hyderabad', '56 Banjara Hills'),
('Priya Desai',    'priya@gmail.com',   '9556677889', 'Chennai',   '90 Anna Nagar'),
('Amit Sharma',    'amit@gmail.com',    '9667788990', 'Kolkata',   '34 Park Street'),
('Neha Patil',     'neha@gmail.com',    '9778899001', 'Jaipur',    '67 Pink City Road'),
('Vijay Kumar',    'vijay@gmail.com',   '9889900112', 'Surat',     '11 Diamond Nagar'),
('Sneha Reddy',    'sneha@gmail.com',   '9990011223', 'Nagpur',    '88 Sitabuldi Road');

INSERT INTO sales (product_id, customer_id, quantity_sold, total_amount) VALUES
(1,  1,  3,  1797.00),   -- Wireless Mouse  x3  by Aarav
(2,  2,  1,   999.00),   -- USB-C Hub       x1  by Diya
(3,  3,  5,  1750.00),   -- Basmati Rice    x5  by Rohan
(4,  4,  4,   720.00),   -- Sunflower Oil   x4  by Meera
(5,  5, 10,  2500.00),   -- A4 Paper        x10 by Karan
(6,  6,  2,   160.00),   -- Ball Pen Pack   x2  by Priya
(7,  7,  3,  1497.00),   -- Men T-Shirt     x3  by Amit
(8,  8,  2,  1598.00),   -- Women Kurti     x2  by Neha
(9,  9,  1,  4999.00),   -- Office Chair    x1  by Vijay
(10, 10, 2,  2598.00);   -- Cricket Bat     x2  by Sneha

INSERT INTO stock_transactions (product_id, txn_type, quantity, remarks) VALUES
(1,  'IN',  100, 'Initial stock received from RajTech'),
(2,  'IN',   50, 'Initial stock received from RajTech'),
(3,  'IN',  200, 'Bulk restock from Sunrise Distributors'),
(4,  'IN',  150, 'Restock after low stock alert'),
(5,  'IN',  100, 'Monthly restock from PrimeMart'),
(6,  'IN',  200, 'Bulk order from PrimeMart'),
(7,  'IN',   60, 'New season stock from GlobalStock'),
(8,  'IN',   40, 'New season stock from GlobalStock'),
(9,  'IN',   20, 'First batch from BlueStar Traders'),
(10, 'IN',   50, 'Sports season restock from NexGen');

INSERT INTO stock_alerts (product_id, alert_message, is_resolved) VALUES
(1,  '⚠️ Low stock for: Wireless Mouse    | Current: 7  | Reorder Level: 10', FALSE),
(2,  '⚠️ Low stock for: USB-C Hub         | Current: 6  | Reorder Level: 8',  FALSE),
(3,  '⚠️ Low stock for: Basmati Rice 5kg  | Current: 15 | Reorder Level: 20', TRUE),
(4,  '⚠️ Low stock for: Sunflower Oil 1L  | Current: 12 | Reorder Level: 15', TRUE),
(5,  '⚠️ Low stock for: A4 Paper Ream     | Current: 8  | Reorder Level: 10', FALSE),
(6,  '⚠️ Low stock for: Ball Pen Pack 10  | Current: 18 | Reorder Level: 20', FALSE),
(7,  '⚠️ Low stock for: Men T-Shirt       | Current: 4  | Reorder Level: 5',  TRUE),
(8,  '⚠️ Low stock for: Women Kurti       | Current: 3  | Reorder Level: 5',  FALSE),
(9,  '⚠️ Low stock for: Office Chair      | Current: 2  | Reorder Level: 3',  FALSE),
(10, '⚠️ Low stock for: Cricket Bat       | Current: 4  | Reorder Level: 5',  TRUE);

SELECT * FROM suppliers;
SELECT * FROM categories;
SELECT * FROM products;
SELECT * FROM customers;
SELECT * FROM sales;
SELECT * FROM stock_transactions;
SELECT * FROM stock_alerts;


SELECT 'suppliers'         AS table_name, COUNT(*) AS total FROM suppliers         UNION ALL
SELECT 'categories',                       COUNT(*)          FROM categories         UNION ALL
SELECT 'products',                         COUNT(*)          FROM products           UNION ALL
SELECT 'customers',                        COUNT(*)          FROM customers          UNION ALL
SELECT 'sales',                            COUNT(*)          FROM sales              UNION ALL
SELECT 'stock_transactions',               COUNT(*)          FROM stock_transactions UNION ALL
SELECT 'stock_alerts',                     COUNT(*)          FROM stock_alerts;

CREATE VIEW vw_product_details AS
SELECT
    p.product_id,
    p.name          AS product,
    p.price,
    p.stock_qty,
    p.unit,
    p.reorder_level,
    c.name          AS category,
    s.name          AS supplier,
    s.city          AS supplier_city
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN suppliers  s ON p.supplier_id  = s.supplier_id;

CREATE VIEW vw_low_stock AS
SELECT
    p.product_id,
    p.name          AS product_name,
    c.name          AS category,
    s.name          AS supplier,
    s.phone         AS supplier_contact,
    p.stock_qty,
    p.reorder_level
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN suppliers  s ON p.supplier_id  = s.supplier_id
WHERE p.stock_qty < p.reorder_level;

SHOW FULL TABLES WHERE Table_type = 'VIEW';

CREATE VIEW vw_sales_summary AS
SELECT
    p.name          AS product_name,
    COUNT(sl.sale_id)         AS total_orders,
    SUM(sl.quantity_sold)     AS total_units_sold,
    SUM(sl.total_amount)      AS total_revenue
FROM sales sl
JOIN products p ON sl.product_id = p.product_id
GROUP BY p.name;

select * from products;

