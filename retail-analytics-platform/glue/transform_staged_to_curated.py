# transform_staged_to_curated.py
#
# Joins staged sales data with product master + inventory snapshot
# Outputs fact tables to curated zone in S3, ready for Athena / Redshift load.

import sys
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.utils import getResolvedOptions
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ['STAGED_PATH','INVENTORY_PATH','PRODUCT_PATH','CURATED_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

staged_df = spark.read.parquet(args['STAGED_PATH'])
inv_df = spark.read.parquet(args['INVENTORY_PATH'])
prod_df = spark.read.parquet(args['PRODUCT_PATH'])

fact_sales = (
    staged_df
    .join(prod_df, ["item_id"], "left")
    .join(inv_df, ["store_id","item_id"], "left")
    .select(
        "timestamp_utc",
        "store_id",
        F.col("item_id").alias("sku"),
        "qty_sold",
        "unit_price",
        "gross_margin_est",
        "on_hand_qty",
        "reorder_point"
    )
)

fact_sales.write.mode("append").parquet(f"{args['CURATED_PATH']}/fact_sales/")
