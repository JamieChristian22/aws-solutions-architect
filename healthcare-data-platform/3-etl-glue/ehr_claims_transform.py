import sys
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

# Goal: standardize EHR + claims data into a curated model

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

ehr_dynf = glueContext.create_dynamic_frame.from_catalog(
    database="raw_db",
    table_name="ehr"
)

claims_dynf = glueContext.create_dynamic_frame.from_catalog(
    database="raw_db",
    table_name="claims"
)

ehr_df = ehr_dynf.toDF()
claims_df = claims_dynf.toDF()

# Example cleanup / normalization steps
ehr_df = ehr_df.withColumnRenamed("patient_mrn", "patient_id")
claims_df = claims_df.withColumnRenamed("subscriber_id", "patient_id")

joined_df = ehr_df.join(claims_df, "patient_id", "left")

curated_dynf = glueContext.create_dynamic_frame.from_df(
    joined_df,
    glueContext,
    "curated_dynf"
)

glueContext.write_dynamic_frame.from_options(
    frame=curated_dynf,
    connection_type="s3",
    connection_options={"path": "s3://hcp-curated-zone/standardized_encounters/"},
    format="parquet"
)