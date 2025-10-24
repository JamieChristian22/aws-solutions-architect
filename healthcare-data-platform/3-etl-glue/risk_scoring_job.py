import sys
from pyspark.sql.functions import col, when
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

# Goal: compute a patient readmission risk score and outreach status

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

curated_dynf = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://hcp-curated-zone/standardized_encounters/"]},
    format="parquet"
)

outreach_dynf = glueContext.create_dynamic_frame.from_catalog(
    database="raw_db",
    table_name="care_mgmt_notes"
)

curated_df = curated_dynf.toDF()
outreach_df = outreach_dynf.toDF()

combined = curated_df.join(
    outreach_df.select("patient_id", "last_outreach_status", "last_outreach_ts"),
    on="patient_id",
    how="left"
)

scored = combined.withColumn(
    "risk_score",
    (
        col("er_visits_30d") * 10 +
        col("chronic_condition_count") * 5 -
        when(col("last_outreach_status") == "successful", 15).otherwise(0)
    )
).withColumn(
    "high_risk_flag",
    when(col("risk_score") >= 80, True).otherwise(False)
)

final_dynf = glueContext.create_dynamic_frame.from_df(scored, glueContext, "final_dynf")

glueContext.write_dynamic_frame.from_options(
    frame=final_dynf,
    connection_type="s3",
    connection_options={"path": "s3://hcp-curated-zone/patient_risk/"},
    format="parquet"
)