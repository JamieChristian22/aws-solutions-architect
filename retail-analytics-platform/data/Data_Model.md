# Retail Data Model

FactSales: date_key, store_key, product_key, channel_key, order_id, units, gross_sales, discounts, net_sales, cogs, returns.
FactInventory: date_key, store_key, product_key, on_hand_units, in_transit_units, stockout_flag.
DimDate, DimStore, DimProduct, DimChannel, DimPromotion.
