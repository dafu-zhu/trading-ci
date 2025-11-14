"""
Shared test fixtures for backtester tests.

This file provides reusable fixtures that can be used across all test files.
"""
import numpy as np
import pandas as pd
import pytest
from finm_python.hw5 import VolatilityBreakoutStrategy, Broker


@pytest.fixture
def simple_prices():
    """
    A simple deterministic rising price series.
    Useful for basic functionality tests.
    
    Returns:
        pd.Series: 10 prices from 100 to 109
    """
    return pd.Series(
        [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0],
        index=pd.date_range('2023-01-01', periods=10)
    )


@pytest.fixture
def long_prices():
    """
    A longer price series for testing rolling windows.
    
    Returns:
        pd.Series: 200 prices linearly increasing from 100 to 120
    """
    return pd.Series(
        np.linspace(100, 120, 200),
        index=pd.date_range('2023-01-01', periods=200)
    )


@pytest.fixture
def volatile_prices():
    """
    A volatile price series with significant ups and downs.
    Good for testing signal generation under volatility.
    
    Returns:
        pd.Series: 50 prices with random volatility around 100
    """
    np.random.seed(42)  # Deterministic randomness
    returns = np.random.normal(0, 0.02, 50)  # 2% daily volatility
    prices = 100 * np.exp(np.cumsum(returns))
    return pd.Series(prices, index=pd.date_range('2023-01-01', periods=50))


@pytest.fixture
def constant_prices():
    """
    A constant price series (no movement).
    Useful for edge case testing.
    
    Returns:
        pd.Series: 20 prices all equal to 100
    """
    return pd.Series(
        [100.0] * 20,
        index=pd.date_range('2023-01-01', periods=20)
    )


@pytest.fixture
def strategy():
    """
    Default VolatilityBreakoutStrategy with lookback=20.
    
    Returns:
        VolatilityBreakoutStrategy: Strategy instance
    """
    return VolatilityBreakoutStrategy(lookback=20)


@pytest.fixture
def short_lookback_strategy():
    """
    Strategy with shorter lookback window for testing.
    
    Returns:
        VolatilityBreakoutStrategy: Strategy with lookback=5
    """
    return VolatilityBreakoutStrategy(lookback=5)


@pytest.fixture
def broker():
    """
    Default broker with $1,000 starting cash.
    
    Returns:
        Broker: Broker instance with cash=1000
    """
    return Broker(cash=1_000)


@pytest.fixture
def rich_broker():
    """
    Broker with larger starting capital.
    
    Returns:
        Broker: Broker instance with cash=1,000,000
    """
    return Broker(cash=1_000_000)
