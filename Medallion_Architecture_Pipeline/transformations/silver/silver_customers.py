from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.expect_or_drop("valid_customer_id", "customer_id IS NOT NULL")
@dp.expect_or_drop("valid_email", "email_address IS NOT NULL")
@dp.materialized_view(
    comment="Silver layer: cleansed customer records with full_name derived field. Phone number excluded as PII."
)
def silver_customers():
    return (
        spark.read.table("bronze_customers")
        .select(
            F.col("customerID").alias("customer_id"),
            F.concat_ws(" ", F.col("first_name"), F.col("last_name")).alias("full_name"),
            F.col("first_name"),
            F.col("last_name"),
            F.col("email_address"),
            F.col("city"),
            F.col("state"),
            F.col("country"),
            F.col("continent"),
            F.col("postal_zip_code"),
            F.col("gender"),
        )
    )
