import numpy as np
import pandas as pd


class VolatilityBreakoutStrategy:
    """
    A volatility breakout strategy that generates buy/sell signals based on
    rolling volatility.

    Logic:
    - Computes rolling x-day standard deviation of daily returns
    - Generates a signal: +1 (buy) when return > volatility, -1 (sell) when return < -volatility, 0 (hold)
    - Returns a pd.Series of signals with the same index as input prices

    Args:
        lookback (int): Number of days for rolling volatility window (default 20)

    Returns:
        pd.Series: Signal series with values in {-1, 0, 1}

    Example:
        prices = pd.Series([100, 101, 102, 103, ...])
        strategy = VolatilityBreakoutStrategy(lookback=10)
        signals = strategy.signals(prices)
        # First 10 rows may be NaN, then {-1, 0, 1}
    """

    def __init__(self, lookback: int = 20):
        self.lookback = lookback

    def signals(self, prices: pd.Series) -> pd.Series:
        """
        Generate trading signals based on volatility breakout.

        High-level steps:
        1. Compute daily returns from prices
        2. Calculate rolling standard deviation (volatility) over lookback window
        3. For each day, compare return to +/- volatility threshold
        4. Return signal series (-1, 0, +1)

        Args:
            prices: pd.Series of daily prices

        Returns:
            pd.Series of signals aligned with prices index
        """
        # YOUR CODE STARTS HERE
        # Hint: use .pct_change() for returns, .rolling().std() for volatility
        # Compare current return to +/- volatility threshold
        if len(prices) == 0:
            raise ValueError("Prices cannot be empty")
        pct_chg = prices.pct_change().fillna(0)
        vol = pct_chg.rolling(self.lookback).std().fillna(0)
        signals = np.where(pct_chg > vol, 1, 0)
        signals = np.where(pct_chg < -vol, -1, signals)
        return pd.Series(signals, index=prices.index)

        # YOUR CODE ENDS HERE

if __name__ == "__main__":
    prices = pd.Series([100, 101, 102, 103, 104, 105, 106, 107, 108, 109])
    strategy = VolatilityBreakoutStrategy(lookback=3)
    signals = strategy.signals(prices)
    print(signals)