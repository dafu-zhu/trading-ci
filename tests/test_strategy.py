"""
Unit tests for VolatilityBreakoutStrategy.

Tests should verify:
- Signal generation logic (buy/sell/hold conditions)
- Output format and length
- Edge cases (empty, constant, short series)
- NaN handling in early periods
"""
import numpy as np
import pandas as pd
import pytest
from finm_python.hw5 import VolatilityBreakoutStrategy


class TestSignalGeneration:
    """Test the core signal generation logic."""
    
    def test_signals_length(self, strategy, long_prices):
        """
        Verify that signals() returns a Series with the same length as input.
        
        Expected: len(signals) == len(prices)
        """
        # YOUR CODE STARTS HERE
        # Step 1: Call strategy.signals() with long_prices
        signals = strategy.signals(long_prices)
        # Step 2: Assert that length matches
        assert len(signals) == len(long_prices)
        # YOUR CODE ENDS HERE
    
    def test_signals_returns_series_with_same_index(self, strategy, simple_prices):
        """
        Verify that output Series has the same index as input prices.
        
        Expected: signals.index equals prices.index
        """
        # YOUR CODE STARTS HERE
        # Step 1: Get signals
        signals = strategy.signals(simple_prices)
        # Step 2: Assert index equality (use .equals() or ==)
        assert signals.index.equals(simple_prices.index)
        # YOUR CODE ENDS HERE
    
    def test_signals_only_contain_valid_values(self, strategy, volatile_prices):
        """
        Verify that all signals are in {-1, 0, 1}.
        
        Expected: Every value in signals is -1, 0, or 1
        """
        # YOUR CODE STARTS HERE
        # Step 1: Get signals
        signals = strategy.signals(volatile_prices)
        # Step 2: Assert all values are in {-1, 0, 1}
        # Hint: Use .isin([-1, 0, 1]).all()
        assert signals.isin([-1, 0, 1]).all()
        # YOUR CODE ENDS HERE
    
    def test_buy_signal_when_return_exceeds_volatility(self, short_lookback_strategy):
        """
        Test that strategy generates +1 (buy) when return > volatility.
        
        Create a synthetic scenario:
        - Low volatility period
        - Then a big positive return
        
        Expected: Signal = +1 after the big move
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create prices: [100] * 10 + [110]  (flat then jump)
        prices = pd.Series([100] * 10 + [110])
        # Step 2: Create a strategy with lookback=5
        # Step 3: Get signals
        signals = short_lookback_strategy.signals(prices)
        # Step 4: Assert that the signal at the jump is +1
        assert signals.iloc[10] == 1, f"Expected BUY signal at jump, got {signals.iloc[10]}"
        # Hint: The jump from 100->110 should exceed the low volatility

        # YOUR CODE ENDS HERE
    
    def test_sell_signal_when_return_below_negative_volatility(self, short_lookback_strategy):
        """
        Test that strategy generates -1 (sell) when return < -volatility.
        
        Create a synthetic scenario:
        - Low volatility period
        - Then a big negative return
        
        Expected: Signal = -1 after the big drop
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create prices: [100] * 10 + [90]  (flat then drop)
        prices = pd.Series([100] * 10 + [90])
        # Step 2: Create a strategy with lookback=5
        # Step 3: Get signals
        signals = short_lookback_strategy.signals(prices)
        # Step 4: Assert that the signal at the drop is -1
        assert signals.iloc[10] == -1, f"Expected SELL signal at drop, got {signals.iloc[10]}"
        # YOUR CODE ENDS HERE
    
    def test_hold_signal_when_return_within_volatility(self, strategy, constant_prices):
        """
        Test that strategy generates 0 (hold) when return is within volatility bands.
        
        Expected: All signals are 0 for constant prices
        """
        # YOUR CODE STARTS HERE
        signals = strategy.signals(constant_prices)
        assert signals.eq(0).all(), f"Expected all signals to be 0, got {signals}"
        # YOUR CODE ENDS HERE


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_prices_raises_error(self, strategy):
        """
        Verify that passing an empty Series raises ValueError.
        
        Expected: ValueError with message about empty prices
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create empty Series
        prices = pd.Series([], dtype=float)
        # Step 2: Use pytest.raises(ValueError) to assert exception
        # Step 3: Call strategy.signals() within the context
        with pytest.raises(ValueError):
            strategy.signals(prices)
        # YOUR CODE ENDS HERE
    
    def test_constant_prices_returns_all_zeros(self, strategy, constant_prices):
        """
        Verify that constant prices (no volatility) produce all 0 signals.
        
        Expected: All signals should be 0 (no breakout possible)
        """
        # YOUR CODE STARTS HERE
        # Step 1: Get signals from constant_prices
        signals = strategy.signals(constant_prices)
        # Step 2: Assert all signals are 0
        # Hint: (signals == 0).all()
        assert signals.eq(0).all(), f"Expected all signals to be 0, got {signals}"
        # YOUR CODE ENDS HERE
    
    def test_very_short_series(self):
        """
        Test strategy with series shorter than lookback window.
        
        Expected: Should handle gracefully (may have some NaN/0 behavior)
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create prices with only 3 values
        prices = pd.Series([100, 110, 120])
        # Step 2: Create strategy with lookback=10 (longer than series)
        strategy = VolatilityBreakoutStrategy(lookback=10)
        # Step 3: Get signals (should not crash)
        signals = strategy.signals(prices)
        # Step 4: Assert signals are returned and have correct length
        assert len(signals) == len(prices)
        # YOUR CODE ENDS HERE
    
    def test_single_price(self, strategy):
        """
        Test with a single price point.
        
        Expected: Returns a Series of length 1
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create Series with single value
        prices = pd.Series([100])
        # Step 2: Get signals
        signals = strategy.signals(prices)
        # Step 3: Assert length is 1 and value is 0
        assert len(signals) == 1 and signals.iloc[0] == 0, f"Expected length 1 with value 0, got {signals}"
        # YOUR CODE ENDS HERE


class TestLookbackParameter:
    """Test different lookback window sizes."""
    
    def test_different_lookback_windows_produce_different_signals(self, volatile_prices):
        """
        Verify that changing lookback changes signal generation.
        
        Expected: Strategy(lookback=5) != Strategy(lookback=20) signals
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create two strategies with different lookbacks (e.g., 5 and 20)
        strat_1 = VolatilityBreakoutStrategy(lookback=5)
        strat_2 = VolatilityBreakoutStrategy(lookback=20)
        # Step 2: Get signals from both
        signals1 = strat_1.signals(volatile_prices)
        signals2 = strat_2.signals(volatile_prices)
        # Step 3: Assert that at least some signals differ
        # Hint: ~(signals1 == signals2).all()
        assert not signals1.eq(signals2).all(), "Expected different signals with different lookbacks"
        # YOUR CODE ENDS HERE
    
    def test_lookback_of_one(self, simple_prices):
        """
        Test edge case with lookback=1.
        
        Expected: Should work, but volatility will be mostly 0 or NaN
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create strategy with lookback=1
        strategy = VolatilityBreakoutStrategy(lookback=1)
        # Step 2: Get signals
        signals = strategy.signals(simple_prices)
        # Step 3: Assert length matches prices
        assert len(signals) == len(simple_prices)
        # YOUR CODE ENDS HERE


class TestDeterminism:
    """Ensure strategy is deterministic (same input = same output)."""
    
    def test_repeated_calls_produce_same_signals(self, strategy, volatile_prices):
        """
        Verify that calling signals() multiple times returns identical results.
        
        Expected: signals1.equals(signals2) for same inputs
        """
        # YOUR CODE STARTS HERE
        # Step 1: Call strategy.signals() twice with same prices
        signals1 = strategy.signals(volatile_prices)
        signals2 = strategy.signals(volatile_prices)
        # Step 2: Assert both results are equal
        # Hint: Use pd.Series.equals() or assert (s1 == s2).all()
        assert signals1.eq(signals2).all(), f"Expected signals to be equal, got {signals1} != {signals2}"
        # YOUR CODE ENDS HERE
