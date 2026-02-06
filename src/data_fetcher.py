from __future__ import annotations

from datetime import date

import pandas as pd
import yfinance as yf


def fetch_price_history(
    ticker: str,
    start: date,
    end: date,
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a given ticker using yfinance.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol (e.g., "AAPL").
    start : date
        Start date for historical data (inclusive).
    end : date
        End date for historical data (inclusive).
    interval : str, optional
        Data interval, default "1d".

    Returns
    -------
    pd.DataFrame
        DataFrame indexed by datetime with OHLCV columns.
    """
    df = yf.download(
        ticker,
        start=start.isoformat(),
        end=end.isoformat(),
        interval=interval,
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"No data returned for ticker {ticker} in given date range.")

    # Ensure we have a DateTimeIndex and sort
    df = df.sort_index()
    return df
