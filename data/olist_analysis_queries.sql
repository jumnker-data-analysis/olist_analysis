CREATE TABLE orders (
order_id TEXT,
customer_id TEXT,
order_status TEXT,
order_purchase_timestamp TIMESTAMP,
order_approved_at TIMESTAMP,
order_delivered_carrier_date TIMESTAMP,
order_delivered_customer_date TIMESTAMP,
order_estimated_delivery_date TIMESTAMP
);

select *
from orders
limit 10;

CREATE TABLE customers (
customer_id TEXT,
customer_unique_id TEXT,
customer_zip_code_prefix TEXT,
customer_city TEXT,
customer_state TEXT
);


CREATE TABLE order_items (
order_id TEXT,
order_item_id INTEGER,
product_id TEXT,
seller_id TEXT,
shipping_limit_date TIMESTAMP,
price NUMERIC,
freight_value NUMERIC
);



CREATE TABLE order_payments (
order_id TEXT,
payment_sequential INTEGER,
payment_type TEXT,
payment_installments INTEGER,
payment_value NUMERIC
);


SELECT * FROM customers LIMIT 5;
SELECT * FROM order_items LIMIT 5;
SELECT * FROM order_payments LIMIT 5;
SELECT * FROM orders LIMIT 5;


SELECT
o.order_id,
c.customer_city,
c.customer_state,
oi.price,
oi.freight_value,
p.payment_type,
p.payment_value
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
JOIN order_items oi
ON o.order_id = oi.order_id
JOIN order_payments p
ON o.order_id = p.order_id
LIMIT 20;


-- Monthly Revenue KPI
SELECT
date_trunc('month', o.order_purchase_timestamp)::date AS order_month,
ROUND(SUM(p.payment_value), 2) AS monthly_revenue,
COUNT(DISTINCT o.order_id) AS total_orders,
ROUND(SUM(p.payment_value) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM orders o
JOIN order_payments p
ON o.order_id = p.order_id
GROUP BY date_trunc('month', o.order_purchase_timestamp)::date
ORDER BY order_month;

-- Customer segment KPI
WITH customer_spending AS (
SELECT
c.customer_unique_id,
ROUND(SUM(p.payment_value), 2) AS total_spending
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN order_payments p
ON o.order_id = p.order_id
GROUP BY c.customer_unique_id
),

customer_segment AS (
SELECT
customer_unique_id,
total_spending,
CASE
WHEN total_spending >= 1000 THEN 'High Value'
WHEN total_spending >= 300 THEN 'Medium Value'
ELSE 'Low Value'
END AS segment
FROM customer_spending
)

SELECT
segment,
COUNT(*) AS total_customers,
ROUND(SUM(total_spending), 2) AS segment_revenue,
ROUND(AVG(total_spending), 2) AS avg_segment_revenue
FROM customer_segment
GROUP BY segment
ORDER BY segment_revenue DESC;

-- Delivery per
SELECT
date_trunc('month', order_purchase_timestamp)::date AS order_month,
COUNT(*) AS delivered_orders,
ROUND(
AVG(EXTRACT(EPOCH FROM (order_delivered_customer_date - order_purchase_timestamp)) / 86400),
2
) AS avg_delivery_days,
ROUND(
COUNT(*) FILTER (
WHERE order_delivered_customer_date > order_estimated_delivery_date
) * 100.0 / COUNT(*),
2
) AS late_delivery_rate
FROM orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL
AND order_estimated_delivery_date IS NOT NULL
GROUP BY date_trunc('month', order_purchase_timestamp)::date
ORDER BY order_month;


SELECT
c.customer_state,
COUNT(DISTINCT o.order_id) AS total_orders,
ROUND(SUM(p.payment_value), 2) AS total_revenue,
ROUND(SUM(p.payment_value) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN order_payments p
ON o.order_id = p.order_id
GROUP BY c.customer_state
ORDER BY total_revenue DESC;


SELECT
ROUND(SUM(p.payment_value), 2) AS total_revenue,
COUNT(DISTINCT o.order_id) AS total_orders,
COUNT(DISTINCT c.customer_unique_id) AS total_customers,
ROUND(SUM(p.payment_value) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
JOIN order_payments p
ON o.order_id = p.order_id;
