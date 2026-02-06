from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_portfolio_var(
    returns: pd.Series | np.ndarray,
    portfolio_value: float,
    var_percentage: float,
) -> dict[str, float]:
    """
    Convert percentage VaR to dollar VaR for a portfolio.

    Parameters
    ----------
    returns : pd.Series or np.ndarray
        Historical returns (unused but kept for consistency).
    portfolio_value : float
        Total portfolio value in dollars.
    var_percentage : float
        VaR as a decimal (e.g., 0.02 for 2%).

    Returns
    -------
    dict
        Dictionary with 'var_percentage' and 'var_dollar' keys.
    """
    var_dollar = portfolio_value * var_percentage
    return {
        "var_percentage": var_percentage,
        "var_dollar": var_dollar,
    }
