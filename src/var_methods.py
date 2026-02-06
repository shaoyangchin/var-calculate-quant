from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def historical_var(
    returns: pd.Series | np.ndarray,
    confidence_level: float = 0.95,
) -> float:
    """
    Calculate Value at Risk using the Historical Method.

    Parameters
    ----------
    returns : pd.Series or np.ndarray
        Historical returns.
    confidence_level : float
        Confidence level (e.g., 0.95 for 95% confidence).

    Returns
    -------
    float
        VaR as a positive number representing the loss threshold.
    """
    if isinstance(returns, pd.Series):
        returns = returns.dropna().to_numpy()
    else:
        returns = np.asarray(returns)
        returns = returns[~np.isnan(returns)]

    if len(returns) == 0:
        raise ValueError("No valid returns data provided.")

    # VaR is the negative of the (1 - confidence_level) percentile
    var = -np.percentile(returns, (1 - confidence_level) * 100)
    return float(var)


def parametric_var(
    returns: pd.Series | np.ndarray,
    confidence_level: float = 0.95,
) -> float:
    """
    Calculate Value at Risk using the Parametric (Variance-Covariance) Method.

    Assumes returns are normally distributed.

    Parameters
    ----------
    returns : pd.Series or np.ndarray
        Historical returns.
    confidence_level : float
        Confidence level (e.g., 0.95 for 95% confidence).

    Returns
    -------
    float
        VaR as a positive number representing the loss threshold.
    """
    if isinstance(returns, pd.Series):
        returns = returns.dropna().to_numpy()
    else:
        returns = np.asarray(returns)
        returns = returns[~np.isnan(returns)]

    if len(returns) == 0:
        raise ValueError("No valid returns data provided.")

    mu = np.mean(returns)
    sigma = np.std(returns, ddof=1)

    # Z-score for the confidence level
    z = stats.norm.ppf(confidence_level)

    # VaR = -(mu - z * sigma)
    var = -(mu - z * sigma)
    return float(var)


def monte_carlo_var(
    returns: pd.Series | np.ndarray,
    confidence_level: float = 0.95,
    num_simulations: int = 10000,
    time_horizon: int = 1,
    random_seed: int | None = None,
) -> tuple[float, np.ndarray]:
    """
    Calculate Value at Risk using Monte Carlo Simulation.

    Parameters
    ----------
    returns : pd.Series or np.ndarray
        Historical returns for parameter estimation.
    confidence_level : float
        Confidence level (e.g., 0.95 for 95% confidence).
    num_simulations : int
        Number of Monte Carlo simulations.
    time_horizon : int
        Time horizon in days (typically 1 for 1-day VaR).
    random_seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    var : float
        VaR as a positive number representing the loss threshold.
    simulated_returns : np.ndarray
        Array of simulated returns for the time horizon.
    """
    if isinstance(returns, pd.Series):
        returns = returns.dropna().to_numpy()
    else:
        returns = np.asarray(returns)
        returns = returns[~np.isnan(returns)]

    if len(returns) == 0:
        raise ValueError("No valid returns data provided.")

    mu = np.mean(returns)
    sigma = np.std(returns, ddof=1)

    if random_seed is not None:
        np.random.seed(random_seed)

    # Simulate returns for the time horizon
    # For multi-day horizon, we sum daily returns (or scale volatility)
    # Simple approach: simulate time_horizon days and sum
    simulated_returns = np.random.normal(
        mu * time_horizon,
        sigma * np.sqrt(time_horizon),
        num_simulations,
    )

    var = -np.percentile(simulated_returns, (1 - confidence_level) * 100)
    return float(var), simulated_returns
