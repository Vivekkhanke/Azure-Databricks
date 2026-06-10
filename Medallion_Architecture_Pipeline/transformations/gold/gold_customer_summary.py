from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.materialized_view(
    comment="Gold layer: customer 360 view — lifetime spend, transaction history, and profile data joined.",
    cluster_by=["customer_id"],
)
def gold_customer_summary():
    transactions = spark.read.table("silver_transactions")
    customers = spark.read.table("silver_customers")

    customer_metrics = (
        transactions.groupBy("customer_id")
        .agg(
            F.sum("total_price").alias("total_spend"),
            F.count("transaction_id").alias("transaction_count"),
            F.avg("total_price").alias("avg_order_value"),
            F.min("transaction_date").alias("first_purchase_date"),
            F.max("transaction_date").alias("last_purchase_date"),
            F.countDistinct("product").alias("unique_products_purchased"),
        )
    )

    return (
        customer_metrics
        .join(customers, on="customer_id", how="inner")
        .select(
            "customer_id",
            "full_name",
            "email_address",
            "city",
            "country",
            "continent",
            "gender",
            "total_spend",
            "transaction_count",
            "avg_order_value",
            "first_purchase_date",
            "last_purchase_date",
            "unique_products_purchased",
        )
    )
