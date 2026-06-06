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

