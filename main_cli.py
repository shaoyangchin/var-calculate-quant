import argparse

from src.pipeline import calculate_var_for_ticker, summarize_var_results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Value at Risk (VaR) Calculator - Historical, Parametric, and Monte Carlo methods."
    )
    parser.add_argument(
        "--ticker",
        type=str,
        default="AAPL",
        help="Ticker symbol to analyze (default: AAPL).",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.95,
        help="Confidence level for VaR (default: 0.95 for 95%%).",
    )
    parser.add_argument(
        "--portfolio-value",
        type=float,
        default=100000.0,
        help="Portfolio value in dollars (default: 100000).",
    )
    parser.add_argument(
        "--time-horizon",
        type=int,
        default=1,
        help="Time horizon in days (default: 1).",
    )
    parser.add_argument(
        "--mc-simulations",
        type=int,
        default=10000,
        help="Number of Monte Carlo simulations (default: 10000).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("Fetching data and calculating VaR...")
    print()

    results = calculate_var_for_ticker(
        ticker=args.ticker,
        confidence_level=args.confidence,
        portfolio_value=args.portfolio_value,
        time_horizon=args.time_horizon,
        mc_simulations=args.mc_simulations,
    )

    summary = summarize_var_results(results)
    print(summary)


if __name__ == "__main__":
    main()
