"""
Unit tests for Backtester (engine).

Tests should verify:
- Uses t-1 signal for t trade
- Correctly tracks equity, cash, position
- Handles no-trade scenarios
- Integration with strategy and broker
- Mocked failure paths
"""
import pandas as pd
import numpy as np
import pytest
from unittest.mock import MagicMock, Mock
from finm_python.hw5 import Backtester
from finm_python.hw5 import Broker
from finm_python.hw5 import VolatilityBreakoutStrategy


class TestBasicExecution:
    """Test basic backtester functionality."""
    
    def test_run_returns_dataframe(self, strategy, broker, simple_prices):
        """
        Verify that run() returns a DataFrame with correct structure.
        
        Expected: DataFrame with columns ['equity', 'cash', 'position']
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create Backtester
        bt = Backtester(strategy, broker)
        # Step 2: Call run()
        result = bt.run(simple_prices)
        # Step 3: Assert result is a DataFrame
        assert isinstance(result, pd.DataFrame)
        # Step 4: Assert columns are correct
        assert list(result.columns) == ['equity', 'cash', 'position']
        # YOUR CODE ENDS HERE
    
    def test_output_length_matches_input(self, strategy, broker, simple_prices):
        """
        Verify that result has same length as input prices.
        
        Expected: len(result) == len(prices)
        """
        # YOUR CODE STARTS HERE
        # Step 1: Run backtest
        bt = Backtester(strategy, broker)
        result = bt.run(simple_prices)
        # Step 2: Assert length
        assert len(simple_prices) == len(result)
        # YOUR CODE ENDS HERE
    
    def test_output_index_matches_input(self, strategy, broker, simple_prices):
        """
        Verify that result index matches price index.
        
        Expected: result.index.equals(prices.index)
        """
        # YOUR CODE STARTS HERE
        # Step 1: Run backtest
        bt = Backtester(strategy, broker)
        result = bt.run(simple_prices)
        # Step 2: Assert index equality
        assert result.index.eq(simple_prices.index)
        # YOUR CODE ENDS HERE
    
    def test_initial_state_reflects_broker_starting_values(self, broker, simple_prices):
        """
        Verify that first row reflects initial broker state.
        
        Given: broker with cash=1000, position=0
        Expected: result.iloc[0] matches initial state
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create strategy and backtester
        strategy = MagicMock()
        bt = Backtester(strategy, broker)
        # Step 2: Run backtest
        result = bt.run(simple_prices)
        # Step 3: Assert result.iloc[0]['cash'] == 1000
        assert result.iloc[0]['cash'] == 1000, f"Expected cash to be 1000, got {result.iloc[0]['cash']}"
        # Step 4: Assert result.iloc[0]['position'] == 0
        assert result.iloc[0]['position'] == 0, f"Expected position to be 0, got {result.iloc[0]['position']}"
        # Step 5: Assert result.iloc[0]['equity'] == 1000
        assert result.iloc[0]['equity'] == 1000, f"Expected equity to be 1000, got {result.iloc[0]['equity']}"
        # YOUR CODE ENDS HERE


class TestTradingLogic:
    """Test that trades execute correctly."""
    
    def test_buy_signal_executes_trade(self, broker, simple_prices):
        """
        Verify that a +1 signal results in a buy.
        
        Use a mock strategy that returns all +1 signals.
        Expected: position increases, cash decreases
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create a mock strategy
        mock_strategy = MagicMock()
        mock_strategy.signals.return_value = pd.Series([1]*len(simple_prices), index=simple_prices.index)
        # Step 2: Create Backtester with mock
        bt = Backtester(mock_strategy, broker)
        # Step 3: Run backtest
        result = bt.run(simple_prices)
        # Step 4: Assert broker.position > 0
        assert result.iloc[-1]['position'] > 0, f"Expected position to be > 0, got {result.iloc[-1]['position']}"
        # Step 5: Assert broker.cash < 1000
        assert result.iloc[-1]['cash'] < 1000, f"Expected cash to be < 1000, got {result.iloc[-1]['cash']}"
        # YOUR CODE ENDS HERE
    
    def test_sell_signal_executes_trade(self, broker, simple_prices):
        """
        Verify that a -1 signal results in a sell (short).
        
        Use a mock strategy that returns all -1 signals.
        Expected: position becomes negative, cash increases
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create a mock strategy with all -1 signals
        strategy = MagicMock()
        strategy.signals.return_value = pd.Series([-1] * len(simple_prices), index=simple_prices.index)
        # Step 2: Run backtest
        bt = Backtester(strategy, broker)
        result = bt.run(simple_prices)
        # Step 3: Assert broker.position < 0 (short)
        assert broker.position < 0, f"Expected position to be < 0, got {broker.position}"
        # Step 4: Assert broker.cash > 1000
        assert broker.cash > 1000, f"Expected cash to be > 1000, got {broker.cash}"
        # YOUR CODE ENDS HERE
    
    def test_hold_signal_executes_no_trade(self, broker, simple_prices):
        """
        Verify that 0 signals result in no trades.
        
        Use a mock strategy that returns all 0 signals.
        Expected: position = 0, cash unchanged
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create a mock strategy with all 0 signals
        strategy = MagicMock()
        strategy.signals.return_value = pd.Series([0] * len(simple_prices), index=simple_prices.index)
        # Step 2: Run backtest
        bt = Backtester(strategy, broker)
        result = bt.run(simple_prices)
        # Step 3: Assert broker.position == 0
        assert broker.position == 0, f"Expected position to be 0, got {broker.position}"
        # Step 4: Assert broker.cash == 1000 (unchanged)
        assert broker.cash == 1000, f"Expected cash to be 1000, got {broker.cash}"
        # YOUR CODE ENDS HERE


class TestSignalTiming:
    """Test that t-1 signal is used for t trade."""
    
    def test_uses_previous_signal_for_current_trade(self, broker):
        """
        Verify that the signal from t-1 is used to trade at t.
        
        Strategy: Create mock with specific signal pattern:
        - signals[0] = 0 (no trade at t=1)
        - signals[1] = 1 (buy at t=2)
        
        Expected:
        - At t=1: no trade (position = 0)
        - At t=2: buy executed (position > 0)
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create prices (e.g., [100, 105, 110])
        prices = pd.Series([100, 105, 110], index=pd.date_range('2025-01-01', periods=3))
        # Step 2: Create a mock strategy:
        strategy = MagicMock()
        strategy.signals.return_value = pd.Series([0, 1, 1], index=prices.index)
        # Step 3: Run backtest
        bt = Backtester(strategy, broker)
        result = bt.run(prices)
        # Step 4: Check that at index 1, the position is still 0
        assert result.iloc[0]['position'] == 0, f"Expected position to be 0, got {result.iloc[0]['position']}"
        # Step 5: Check that at index 2, position > 0
        assert result.iloc[1]['position'] > 0, f"Expected position to be > 0, got {result.iloc[1]['position']}"
        # YOUR CODE ENDS HERE
    
    def test_first_bar_has_no_trade(self, strategy, broker, simple_prices):
        """
        Verify that no trade occurs at first bar (no signal from t-1).
        
        Expected: result.iloc[0] equals initial state
        """
        # YOUR CODE STARTS HERE
        # Step 1: Run backtest
        bt = Backtester(strategy, broker)
        result = bt.run(simple_prices)
        # Step 2: Assert first row position == 0
        assert result.iloc[0]['position'] == 0, f"Expected position to be 0, got {result.iloc[0]['position']}"
        # Step 3: Assert first row cash == initial cash
        assert result.iloc[0]['cash'] == 1000, f"Expected cash to be 1000, got {result.iloc[0]['cash']}"
        # YOUR CODE ENDS HERE
    
    def test_signal_changes_trigger_trades(self, broker):
        """
        Verify that position changes when signal changes.
        
        Mock strategy with signals: [0, 0, 1, 1, 0, -1]
        Expected:
        - Trade occurs when signal changes from 0->1, 1->0, 0->-1
        - No trade when signal stays same
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create prices and mock signals
        prices = pd.Series(np.arange(100, 106), index=pd.date_range('2025-01-01', periods=6))
        strategy = MagicMock()
        strategy.signals.return_value = pd.Series([0, 0, 1, 0, -1, 0], index=prices.index)
        # Step 2: Track position after each bar
        bt = Backtester(strategy, broker)
        result = bt.run(prices)
        positions = result['position'].tolist()
        # Step 3: Assert position changes at signal transitions
        assert positions[3] == 1, f"Expected position to be 1, got {positions[3]}"
        assert positions[5] == -1, f"Expected position to be -1, got {positions[5]}"
        # YOUR CODE ENDS HERE


class TestEquityCalculation:
    """Test equity tracking (cash + position * price)."""
    
    def test_equity_equals_cash_plus_position_value(self, strategy, broker, simple_prices):
        """
        Verify equity calculation: equity = cash + position * current_price.
        
        Expected: For each row, equity == cash + position * price[i]
        """
        # YOUR CODE STARTS HERE
        # Step 1: Run backtest
        # Step 2: Loop through result rows
        # Step 3: For each row i, assert:
        #   result.loc[i, 'equity'] ≈ result.loc[i, 'cash'] + result.loc[i, 'position'] * simple_prices.iloc[i]
        pass
        # YOUR CODE ENDS HERE
    
    def test_equity_reflects_price_changes(self, broker):
        """
        Verify that equity changes with price movements while holding position.
        
        Scenario:
        - Buy at price = 100
        - Price rises to 110
        - Equity should increase by position * (110 - 100)
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create prices [100, 110, 120]
        # Step 2: Create mock strategy with buy signal
        # Step 3: Run backtest
        # Step 4: Assert equity increases as prices rise
        pass
        # YOUR CODE ENDS HERE
    
    def test_final_equity_matches_liquidation_value(self, strategy, rich_broker, long_prices):
        """
        Verify that final equity equals what you'd get if you liquidated.
        
        Expected: final_equity = final_cash + final_position * final_price
        """
        # YOUR CODE STARTS HERE
        # Step 1: Run backtest
        # Step 2: Get last row
        # Step 3: Calculate expected liquidation value
        # Step 4: Assert equality
        pass
        # YOUR CODE ENDS HERE


class TestIntegrationWithRealStrategy:
    """Test with actual VolatilityBreakoutStrategy (not mocked)."""
    
    def test_end_to_end_with_real_strategy(self, rich_broker, volatile_prices):
        """
        Run full backtest with real strategy and verify basic properties.
        
        Expected:
        - No crashes
        - Final equity is positive
        - Broker state is consistent
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create real strategy
        # Step 2: Create backtester
        # Step 3: Run backtest
        # Step 4: Assert no NaN in result
        # Step 5: Assert final equity > 0
        pass
        # YOUR CODE ENDS HERE
    
    def test_backtest_is_deterministic(self, strategy, broker, volatile_prices):
        """
        Verify that running same backtest twice gives same results.
        
        Expected: result1.equals(result2)
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create two identical brokers and strategies
        # Step 2: Run backtest twice
        # Step 3: Assert results are equal
        pass
        # YOUR CODE ENDS HERE


class TestErrorHandling:
    """Test failure scenarios and error propagation."""
    
    def test_broker_error_propagates(self, broker, simple_prices):
        """
        Test that broker errors are propagated to caller.
        
        Mock broker to raise ValueError on market_order.
        Expected: Backtester.run() raises ValueError
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create mock broker that raises on market_order
        #   mock_broker = Mock()
        #   mock_broker.cash = 1000
        #   mock_broker.position = 0
        #   mock_broker.market_order.side_effect = ValueError("Mock error")
        # Step 2: Create strategy that generates trade signal
        # Step 3: Use pytest.raises to assert ValueError
        # Step 4: Run backtest
        pass
        # YOUR CODE ENDS HERE
    
    def test_strategy_error_propagates(self, broker, simple_prices):
        """
        Test that strategy errors propagate.
        
        Mock strategy to raise exception in signals().
        Expected: Backtester.run() raises exception
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create mock strategy that raises on signals()
        #   mock_strategy = Mock()
        #   mock_strategy.signals.side_effect = RuntimeError("Strategy failed")
        # Step 2: Use pytest.raises
        # Step 3: Run backtest
        pass
        # YOUR CODE ENDS HERE
    
    def test_insufficient_cash_stops_backtest(self, simple_prices):
        """
        Test that insufficient cash error is raised appropriately.
        
        Given: small cash, buy signals
        Expected: ValueError about insufficient cash
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create broker with tiny cash (e.g., $10)
        # Step 2: Create strategy that generates buy signals
        # Step 3: Use pytest.raises(ValueError, match="Insufficient")
        # Step 4: Run backtest
        pass
        # YOUR CODE ENDS HERE


class TestEdgeCases:
    """Test unusual scenarios."""
    
    def test_empty_prices_series(self, strategy, broker):
        """
        Test behavior with empty price series.
        
        Expected: Should handle gracefully or raise clear error
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create empty Series
        # Step 2: Attempt to run backtest
        # Step 3: Document behavior (error or empty result)
        pass
        # YOUR CODE ENDS HERE
    
    def test_single_price_point(self, strategy, broker):
        """
        Test with only one price.
        
        Expected: Returns result with 1 row, no trades
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create Series with 1 price
        # Step 2: Run backtest
        # Step 3: Assert result has 1 row
        # Step 4: Assert no trades occurred
        pass
        # YOUR CODE ENDS HERE
    
    def test_very_long_price_series(self, strategy, rich_broker):
        """
        Test with large price series to verify performance.
        
        Create 1000 prices and verify backtest completes quickly.
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create 1000 prices
        # Step 2: Run backtest
        # Step 3: Assert result has correct length
        # Step 4: (Optional) Time the execution
        pass
        # YOUR CODE ENDS HERE


class TestMockedScenarios:
    """Test specific scenarios using mocks for precise control."""
    
    def test_alternating_signals(self, broker):
        """
        Test with signals that alternate: [0, 1, 0, 1, 0, -1, 0].
        
        Verify position changes correctly at each transition.
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create prices
        # Step 2: Create mock with alternating signals
        # Step 3: Run backtest
        # Step 4: Verify position at each step
        pass
        # YOUR CODE ENDS HERE
    
    def test_buy_and_hold_scenario(self, broker):
        """
        Test simple buy-and-hold: signal = 1 at start, then 1 forever.
        
        Expected: Buy once, then hold position
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create signals: [0, 1, 1, 1, 1, ...]
        # Step 2: Run backtest
        # Step 3: Assert position stays constant after first buy
        pass
        # YOUR CODE ENDS HERE
    
    def test_round_trip_trade(self, broker):
        """
        Test round trip: buy then sell back to flat.
        
        Signals: [0, 1, 1, 0, 0]
        Expected: position goes 0 -> positive -> 0
        """
        # YOUR CODE STARTS HERE
        # Step 1: Create mock signals for round trip
        # Step 2: Run backtest
        # Step 3: Assert position returns to 0
        # Step 4: Assert cash changes reflect round trip
        pass
        # YOUR CODE ENDS HERE
