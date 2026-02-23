-- select * from orders;

select order_id,
julianday(order_delivered_customer_date)-julianday(order_purchase_timestamp) as delivery_days
from orders;

select 
order_id,
cast(julianday(order_delivered_customer_date)-julianday(order_purchase_timestamp) as int) as delivery_days_int,
cast(julianday(order_delivered_customer_date)-julianday(order_estimated_delivery_date) as int) as delivery_delay_int
from orders;

select count(*) as total_orders,

sum(
case 
when julianday(order_delivered_customer_date) > julianday(order_estimated_delivery_date)
then 1 
else 0 
end 
) as late_orders,

round(
100.0 * sum(
case 
when julianday(order_delivered_customer_date) > julianday(order_estimated_delivery_date)
then 1 
else 0 
end 
)
/count(*)
,2
) as delay_rate_percent

from orders

where order_status ='delivered';
