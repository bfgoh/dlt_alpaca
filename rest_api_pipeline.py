import dlt
from alpaca import alpaca_source
import polars as pl

df = pl.read_csv("MarketCap_Processed_20241210.csv")
ticker = df.select(pl.col("Ticker"))
list_of_tickers = ticker.to_series().to_list()
STEP = 20
END = 200
# print(list(range(5, 105, 5)))
if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="alpaca",
        destination=dlt.destinations.postgres,
        dataset_name="historical_stock",
        progress="log",
        export_schema_path="schemas/export",
    )
    for j in range(STEP, END + STEP, STEP):
        i = j - STEP
        list_of_tickers = ticker.to_series().to_list()
        list_of_tickers = list_of_tickers[i:j]
        source = alpaca_source(list_of_stocks=list_of_tickers, split_adjusted="split")
        info = pipeline.run(source, loader_file_format="csv")
        print(info)
