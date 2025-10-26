CREATE TABLE dim_product (
    sku             VARCHAR(50) PRIMARY KEY,
    category        VARCHAR(100),
    brand           VARCHAR(100),
    cost            DECIMAL(10,2)
);
