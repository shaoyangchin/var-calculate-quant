from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .config import DefaultConfig
from .data_fetcher import fetch_price_history
from .portfolio import calculate_portfolio_var
from .returns import calculate_returns
from .var_methods import historical_var, monte_carlo_var, parametric_var


@dataclass
class VaRResults:
    """Container for VaR calculation results."""

    ticker: str
    portfolio_value: float
    confidence_level: float
    returns: np.ndarray
    historical_var: float
    parametric_var: float
    monte_carlo_var: float
    mc_simulated_returns: np.ndarray
    historical_var_dollar: float
    parametric_var_dollar: float
    monte_carlo_var_dollar: float


def calculate_var_for_ticker(
    ticker: str | None = None,
    confidence_level: float | None = None,
    portfolio_value: float | None = None,
    time_horizon: int | None = None,
    mc_simulations: int | None = None,
) -> VaRResults:
    """
    End-to-end pipeline to calculate VaR for a single ticker.

    Parameters
    ----------
    ticker : str, optional
        Stock ticker symbol.
    confidence_level : float, optional
        Confidence level (e.g., 0.95 for 95%).
    portfolio_value : float, optional
        Portfolio value in dollars.
    time_horizon : int, optional
        Time horizon in days.
    mc_simulations : int, optional
        Number of Monte Carlo simulations.

    Returns
    -------
    VaRResults
        Results object containing all VaR calculations.
    """
    cfg = DefaultConfig()
    if ticker is None:
        ticker = cfg.ticker
    if confidence_level is None:
        confidence_level = cfg.confidence_levels[1]  # Default to 95%
    if portfolio_value is None:
        portfolio_value = cfg.portfolio_value
    if time_horizon is None:
        time_horizon = cfg.time_horizon
    if mc_simulations is None:
        mc_simulations = cfg.mc_simulations

    # 1. Fetch historical data
    df = fetch_price_history(ticker=ticker, start=cfg.start_date, end=cfg.end_date)

    # 2. Calculate returns
    prices = df["Close"]
    returns_series = calculate_returns(prices, method="log")
    returns_clean = returns_series.dropna()

    if len(returns_clean) < 30:
        raise ValueError(
            f"Insufficient data: only {len(returns_clean)} return observations. Need at least 30."
        )

    # 3. Calculate VaR using different methods
    hist_var = historical_var(returns_clean, confidence_level)
    param_var = parametric_var(returns_clean, confidence_level)
    mc_var, mc_sim_returns = monte_carlo_var(
        returns_clean,
        confidence_level,
        num_simulations=mc_simulations,
        time_horizon=time_horizon,
        random_seed=42,
    )

    # 4. Convert to dollar amounts
    hist_var_dollar = portfolio_value * hist_var
    param_var_dollar = portfolio_value * param_var
    mc_var_dollar = portfolio_value * mc_var

    return VaRResults(
        ticker=ticker,
        portfolio_value=portfolio_value,
        confidence_level=confidence_level,
        returns=returns_clean.to_numpy(),
        historical_var=hist_var,
        parametric_var=param_var,
        monte_carlo_var=mc_var,
        mc_simulated_returns=mc_sim_returns,
        historical_var_dollar=hist_var_dollar,
        parametric_var_dollar=param_var_dollar,
        monte_carlo_var_dollar=mc_var_dollar,
    )


def summarize_var_results(results: VaRResults) -> str:
    """
    Create a human-readable summary of VaR results.

    Parameters
    ----------
    results : VaRResults
        VaR calculation results.

    Returns
    -------
    str
        Formatted summary string.
    """
    conf_pct = results.confidence_level * 100

    lines = [
        f"Ticker: {results.ticker}",
        f"Portfolio Value: ${results.portfolio_value:,.2f}",
        f"Confidence Level: {conf_pct:.0f}%",
        "",
        "Value at Risk (VaR) Results:",
        f"  Historical Method:",
        f"    VaR: {results.historical_var * 100:.4f}%",
        f"    VaR (Dollar): ${results.historical_var_dollar:,.2f}",
        "",
        f"  Parametric Method (Normal Distribution):",
        f"    VaR: {results.parametric_var * 100:.4f}%",
        f"    VaR (Dollar): ${results.parametric_var_dollar:,.2f}",
        "",
        f"  Monte Carlo Method:",
        f"    VaR: {results.monte_carlo_var * 100:.4f}%",
        f"    VaR (Dollar): ${results.monte_carlo_var_dollar:,.2f}",
        "",
        "Interpretation:",
        f"  With {conf_pct:.0f}% confidence, the maximum expected loss over 1 day is:",
        f"    Historical: ${results.historical_var_dollar:,.2f}",
        f"    Parametric: ${results.parametric_var_dollar:,.2f}",
        f"    Monte Carlo: ${results.monte_carlo_var_dollar:,.2f}",
    ]
    return "\n".join(lines)
