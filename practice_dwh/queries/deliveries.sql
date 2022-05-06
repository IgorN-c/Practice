SELECT
  count(*) as delivered_orders
FROM dim.ft_order AS fto
  INNER JOIN dim.dm_date_delivery AS dmdd
             ON (fto.key_delivery_date = dmdd.key_delivery_date)
WHERE dmdd.delivery_date = CURRENT_DATE - 1
;
