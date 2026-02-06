from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class DefaultConfig:
    """
    Default configuration for VaR calculations.
    """

    ticker: str = "AAPL"
    # Look back this many calendar days for historical data
    lookback_days: int = 365 * 2
    # Confidence levels for VaR
    confidence_levels: tuple[float, ...] = (0.90, 0.95, 0.99)
    # Investment amount in dollars
    portfolio_value: float = 100000.0
    # Time horizon in days (typically 1 for 1-day VaR)
    time_horizon: int = 1
    # Number of Monte Carlo simulations
    mc_simulations: int = 10000

    @property
    def start_date(self) -> date:
        return date.today() - timedelta(days=self.lookback_days)

    @property
    def end_date(self) -> date:
        # Use yesterday to avoid partial current-day data
        return date.today() - timedelta(days=1)
