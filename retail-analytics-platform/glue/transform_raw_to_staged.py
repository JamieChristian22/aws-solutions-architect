# transform_raw_to_staged.py
#
# PySpark Glue Job:
# 1. Read raw POS / inventory events from S3 (JSON)
# 2. Cast types, normalize timestamps, drop bad records
# 3. Write partitioned Parquet to s3://.../staged/...

import sys
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.utils import getResolvedOptions
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ['RAW_PATH','STAGED_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

raw_df = spark.read.json(args['RAW_PATH'])

cleaned_df = (
    raw_df
    .withColumn("qty_sold", F.col("qty_sold").cast("int"))
    .withColumn("unit_price", F.col("unit_price").cast("double"))
    .withColumn("timestamp_utc", F.to_timestamp("ingested_utc"))
    .dropna(subset=["store_id","item_id","qty_sold","unit_price","timestamp_utc"])
)

# partition by date/store for cost-efficient Athena scans
cleaned_df = cleaned_df.withColumn("date_key", F.date_format("timestamp_utc","yyyyMMdd"))
cleaned_df.write.mode("append").partitionBy("date_key","store_id").parquet(args['STAGED_PATH'])
