from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.materialized_view(
    comment="Gold layer: aggregated sales metrics per product — revenue, volume, and customer reach.",
    cluster_by=["product"],
)
def gold_sales_by_product():
    return (
        spark.read.table("silver_transactions")
        .groupBy("product")
        .agg(
            F.sum("total_price").alias("total_revenue"),
            F.sum("quantity").alias("total_quantity_sold"),
            F.avg("unit_price").alias("avg_unit_price"),
            F.countDistinct("transaction_id").alias("transaction_count"),
            F.countDistinct("customer_id").alias("unique_customer_count"),
        )
        .orderBy(F.col("total_revenue").desc())
    )
