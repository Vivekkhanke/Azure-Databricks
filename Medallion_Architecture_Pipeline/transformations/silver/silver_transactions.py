from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.expect_or_drop("valid_transaction_id", "transaction_id IS NOT NULL")
@dp.expect_or_drop("valid_customer_id", "customer_id IS NOT NULL")
@dp.expect("positive_total_price", "total_price > 0")
@dp.materialized_view(
    comment="Silver layer: cleansed transactions with standardized column names, masked card numbers, and data quality constraints."
)
def silver_transactions():
    return (
        spark.read.table("bronze_transactions")
        .select(
            F.col("transactionID").alias("transaction_id"),
            F.col("customerID").alias("customer_id"),
            F.col("franchiseID").alias("franchise_id"),
            F.col("dateTime").alias("transaction_timestamp"),
            F.to_date(F.col("dateTime")).alias("transaction_date"),
            F.col("product"),
            F.col("quantity"),
            F.col("unitPrice").alias("unit_price"),
            F.col("totalPrice").alias("total_price"),
            F.col("paymentMethod").alias("payment_method"),
            # Mask card number — retain only last 4 digits
            F.concat(
                F.lit("****-****-****-"),
                F.substring(F.col("cardNumber").cast("string"), -4, 4)
            ).alias("card_number_masked"),
        )
    )
