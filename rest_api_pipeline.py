import dlt
from alpaca import alpaca_source


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="alpaca",
        destination=dlt.destinations.postgres,
        dataset_name="alpaca",
        progress="log",
        export_schema_path="schemas/export",
    )
    source = alpaca_source(list_of_stocks=["NVDA", "TSLA"])
    info = pipeline.run(source)
