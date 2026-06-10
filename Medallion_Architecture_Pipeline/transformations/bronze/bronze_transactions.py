from pyspark import pipelines as dp


@dp.materialized_view(
    comment="Bronze layer: raw ingestion of bakehouse sales transactions. No transformations applied."
)
def bronze_transactions():
    return spark.read.table("samples.bakehouse.sales_transactions")
