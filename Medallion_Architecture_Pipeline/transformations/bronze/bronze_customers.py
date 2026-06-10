from pyspark import pipelines as dp


@dp.materialized_view(
    comment="Bronze layer: raw ingestion of bakehouse sales customers. No transformations applied."
)
def bronze_customers():
    return spark.read.table("samples.bakehouse.sales_customers")
