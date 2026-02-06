from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_returns(
    prices: pd.Series,
    method: str = "log",
) -> pd.Series:
    """
    Calculate returns from price series.

    Parameters
    ----------
    prices : pd.Series
        Price series (e.g., adjusted close prices).
    method : str, optional
        Return calculation method:
        - "log": logarithmic returns (default)
        - "simple": simple returns

    Returns
    -------
    pd.Series
        Returns series (first value will be NaN and typically dropped).
    """
    if method == "log":
        returns = np.log(prices / prices.shift(1))
    elif method == "simple":
        returns = prices.pct_change()
    else:
        raise ValueError(f"Unknown method: {method}. Use 'log' or 'simple'.")

    return returns
