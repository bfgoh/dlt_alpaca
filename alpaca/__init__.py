from dlt.sources.rest_api import (
    RESTAPIConfig,
    rest_api_source,
)
from custom_config import APIKeyAuth
from dlt.sources.helpers.rest_client.paginators import JSONResponseCursorPaginator
import dlt


@dlt.source(name="alpaca", parallelized=True)
def alpaca_source(
    list_of_stocks: list,
    api_key: str = dlt.secrets.value,
    api_secret: str = dlt.secrets.value,
    base_url: str = dlt.config.value,
):
    source_config: RESTAPIConfig = {
        "client": {
            "base_url": base_url,
            "auth": APIKeyAuth(
                "APCA-API-KEY-ID", api_key, "APCA-API-SECRET-KEY", api_secret, "header"
            ),
            "paginator": JSONResponseCursorPaginator(
                cursor_path="$.next_page_token", cursor_param="page_token"
            ),
        },
        "resources": [
            {
                "name": f"historical_bar_{ticker}",
                "table_name": f"{ticker}",  # This is the name of table in  Postgres
                "endpoint": {
                    "data_selector": "bars",
                    "path": "/v2/stocks/{symbol}/bars",
                    "params": {
                        "symbol": ticker,
                        "timeframe": "1T",
                        "start": "{incremental.start_value}",
                        "adjustment": "raw",
                        "feed": "sip",
                        "limit": 10_000,
                        "sort": "asc",
                    },
                    "incremental": {
                        "cursor_path": "t",
                        "initial_value": "2025-01-01T00:00:00Z",
                    },
                },
            }
            for ticker in list_of_stocks
        ],
    }

    return rest_api_source(source_config)
