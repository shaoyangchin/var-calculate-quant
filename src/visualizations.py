from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_returns_distribution(
    returns: pd.Series | np.ndarray,
    var_values: dict[str, float] | None = None,
    title: str = "Returns Distribution with VaR",
    figsize: tuple[int, int] = (10, 6),
) -> plt.Figure:
    """
    Plot histogram of returns with VaR thresholds.

    Parameters
    ----------
    returns : pd.Series or np.ndarray
        Historical returns.
    var_values : dict, optional
        Dictionary mapping method names to VaR values (e.g., {"Historical 95%": 0.02}).
    title : str
        Plot title.
    figsize : tuple
        Figure size.

    Returns
    -------
    plt.Figure
        Matplotlib figure object.
    """
    if isinstance(returns, pd.Series):
        returns = returns.dropna().to_numpy()
    else:
        returns = np.asarray(returns)
        returns = returns[~np.isnan(returns)]

    fig, ax = plt.subplots(figsize=figsize)

    # Histogram
    ax.hist(returns, bins=50, alpha=0.7, color="steelblue", edgecolor="black", density=True)

    # KDE overlay
    sns.kdeplot(returns, ax=ax, color="darkblue", linewidth=2, label="KDE")

    # Plot VaR thresholds
    if var_values:
        colors = ["red", "orange", "darkred", "purple", "brown"]
        for idx, (label, var_val) in enumerate(var_values.items()):
            color = colors[idx % len(colors)]
            ax.axvline(-var_val, color=color, linestyle="--", linewidth=2, label=f"{label}")

    ax.set_xlabel("Returns", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return fig


def plot_var_comparison(
    var_results: dict[str, float],
    title: str = "VaR Comparison Across Methods",
    figsize: tuple[int, int] = (10, 5),
) -> plt.Figure:
    """
    Bar chart comparing VaR values across different methods.

    Parameters
    ----------
    var_results : dict
        Dictionary mapping method names to VaR values.
    title : str
        Plot title.
    figsize : tuple
        Figure size.

    Returns
    -------
    plt.Figure
        Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=figsize)

    methods = list(var_results.keys())
    values = [var_results[m] * 100 for m in methods]  # Convert to percentage

    bars = ax.bar(methods, values, color="coral", edgecolor="black", alpha=0.8)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{val:.2f}%",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax.set_ylabel("VaR (%)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    return fig
