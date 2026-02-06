"""
Simple Streamlit UI for Value at Risk (VaR) calculation.

Run with:
    streamlit run app_streamlit.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import streamlit as st

from src.pipeline import calculate_var_for_ticker
from src.visualizations import plot_returns_distribution, plot_var_comparison


def main() -> None:
    st.title("Value at Risk (VaR) Calculator")
    st.markdown(
        """
This tool calculates **Value at Risk (VaR)** using three methods:
- **Historical Method**: Uses historical return distribution
- **Parametric Method**: Assumes normal distribution of returns
- **Monte Carlo Method**: Simulates future returns based on historical parameters

**VaR** measures the maximum expected loss over a given time period at a specified confidence level.
        """
    )

    with st.sidebar:
        st.header("Configuration")
        ticker = st.text_input("Ticker", value="AAPL")
        portfolio_value = st.number_input(
            "Portfolio Value ($)",
            min_value=1000.0,
            max_value=10000000.0,
            value=100000.0,
            step=10000.0,
        )
        confidence_level = st.selectbox(
            "Confidence Level",
            options=[0.90, 0.95, 0.99],
            index=1,
            format_func=lambda x: f"{x * 100:.0f}%",
        )
        time_horizon = st.number_input(
            "Time Horizon (days)",
            min_value=1,
            max_value=30,
            value=1,
            step=1,
        )
        mc_simulations = st.number_input(
            "Monte Carlo Simulations",
            min_value=1000,
            max_value=100000,
            value=10000,
            step=1000,
        )

        go = st.button("Calculate VaR")

    if not go:
        st.info("Set your options in the sidebar and click **Calculate VaR**.")
        return

    with st.spinner("Fetching data and calculating VaR..."):
        try:
            results = calculate_var_for_ticker(
                ticker=ticker,
                confidence_level=confidence_level,
                portfolio_value=portfolio_value,
                time_horizon=time_horizon,
                mc_simulations=mc_simulations,
            )
        except Exception as exc:
            st.error(f"Error: {exc}")
            return

    # Display results
    st.success(f"VaR calculated for **{ticker}** at **{confidence_level * 100:.0f}%** confidence")

    # Metrics
    st.subheader("VaR Results (Dollar Amount)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Historical", f"${results.historical_var_dollar:,.2f}")
    col2.metric("Parametric", f"${results.parametric_var_dollar:,.2f}")
    col3.metric("Monte Carlo", f"${results.monte_carlo_var_dollar:,.2f}")

    st.subheader("VaR Results (Percentage)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Historical", f"{results.historical_var * 100:.4f}%")
    col2.metric("Parametric", f"{results.parametric_var * 100:.4f}%")
    col3.metric("Monte Carlo", f"{results.monte_carlo_var * 100:.4f}%")

    # Interpretation
    st.subheader("Interpretation")
    st.write(
        f"With **{confidence_level * 100:.0f}% confidence**, the maximum expected loss "
        f"over **{time_horizon} day(s)** is approximately:"
    )
    st.write(f"- **Historical Method**: ${results.historical_var_dollar:,.2f}")
    st.write(f"- **Parametric Method**: ${results.parametric_var_dollar:,.2f}")
    st.write(f"- **Monte Carlo Method**: ${results.monte_carlo_var_dollar:,.2f}")

    # Visualizations
    st.subheader("Returns Distribution with VaR Thresholds")
    var_dict = {
        f"Historical {confidence_level * 100:.0f}%": results.historical_var,
        f"Parametric {confidence_level * 100:.0f}%": results.parametric_var,
        f"Monte Carlo {confidence_level * 100:.0f}%": results.monte_carlo_var,
    }
    fig1 = plot_returns_distribution(results.returns, var_values=var_dict)
    st.pyplot(fig1)

    st.subheader("VaR Comparison Across Methods")
    fig2 = plot_var_comparison(var_dict)
    st.pyplot(fig2)

    # Statistics
    st.subheader("Historical Returns Statistics")
    col1, col2 = st.columns(2)
    col1.metric("Mean Daily Return", f"{results.returns.mean() * 100:.4f}%")
    col1.metric("Std Dev (Daily)", f"{results.returns.std() * 100:.4f}%")
    col2.metric("Min Daily Return", f"{results.returns.min() * 100:.4f}%")
    col2.metric("Max Daily Return", f"{results.returns.max() * 100:.4f}%")


if __name__ == "__main__":
    main()
