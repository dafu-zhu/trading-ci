"""
Unit tests for Broker.

Tests should verify:
- Buy/sell orders update cash and position correctly
- Input validation (side, qty)
- Insufficient cash/shares handling
- Edge cases (zero qty, negative values)
"""
import pytest
from backtester.broker import Broker


class TestBuyOrders:
    """Test buy order functionality."""
    
    def test_buy_order_deducts_cash(self, broker):
        """
        Verify that a BUY order deducts the correct amount from cash.
        
        Given: broker with $1,000 cash
        When: BUY 5 shares @ $10
        Expected: cash = $950
        """
        # YOUR CODE STARTS HERE
        # Step 1: Execute market_order("BUY", 5, 10.0)
        # Step 2: Assert broker.cash == 950
        pass
        # YOUR CODE ENDS HERE
    
    def test_buy_order_increases_position(self, broker):
        """
        Verify that a BUY order increases position by qty.
        
        Given: broker with position = 0
        When: BUY 10 shares
        Expected: position = 10
        """
        # YOUR CODE STARTS HERE
        # Step 1: Execute buy order
        # Step 2: Assert broker.position == 10
        pass
        # YOUR CODE ENDS HERE
    
    def test_multiple_buy_orders_accumulate_position(self, broker):
        """
        Verify that multiple BUY orders accumulate correctly.
        
        When: BUY 5 @ $10, then BUY 3 @ $10
        Expected: position = 8, cash = 1000 - 80
        """
        # YOUR CODE STARTS HERE
        # Step 1: Execute first buy
        # Step 2: Execute second buy
        # Step 3: Assert position and cash
        pass
        # YOUR CODE ENDS HERE
    
    def test_buy_order_with_exact_cash_succeeds(self, broker):
        """
        Verify that buying with exactly available cash succeeds.
        
        Given: $1,000 cash
        When: BUY 100 @ $10 (costs exactly $1,000)
        Expected: cash = 0, position = 100, no error
        """
        # YOUR CODE STARTS HERE
        # Step 1: Calculate qty that uses all cash
        # Step 2: Execute buy
        # Step 3: Assert cash == 0 and position is correct
        pass
        # YOUR CODE ENDS HERE
    
    def test_buy_order_exceeding_cash_raises_error(self, broker):
        """
        Verify that insufficient cash raises ValueError.
        
        Given: $1,000 cash
        When: BUY 200 @ $10 (costs $2,000)
        Expected: ValueError with "Insufficient cash"
        """
        # YOUR CODE STARTS HERE
        # Step 1: Use pytest.raises(ValueError, match="Insufficient cash")
        # Step 2: Execute order that exceeds cash
        # Step 3: Assert cash and position unchanged
        pass
        # YOUR CODE ENDS HERE


class TestSellOrders:
    """Test sell order functionality."""
    
    def test_sell_order_increases_cash(self, broker):
        """
        Verify that a SELL order adds proceeds to cash.
        
        Given: position = 10, cash = $1,000
        When: SELL 5 @ $10
        Expected: cash = $1,050
        """
        # YOUR CODE STARTS HERE
        # Step 1: Set up initial position (buy first)
        # Step 2: Execute sell
        # Step 3: Assert cash increased
        pass
        # YOUR CODE ENDS HERE
    
    def test_sell_order_decreases_position(self, broker):
        """
        Verify that a SELL order decreases position by qty.
        
        Given: position = 10
        When: SELL 3 shares
        Expected: position = 7
        """
        # YOUR CODE STARTS HERE
        # Step 1: Set up initial position
        # Step 2: Execute sell
        # Step 3: Assert position decreased
        pass
        # YOUR CODE ENDS HERE
    
    def test_sell_entire_position(self, broker):
        """
        Verify selling entire position works correctly.
        
        When: Hold 10 shares, SELL 10
        Expected: position = 0, cash increases by 10 * price
        """
        # YOUR CODE STARTS HERE
        # Step 1: Buy some shares
        # Step 2: Sell all shares
        # Step 3: Assert position == 0
        pass
        # YOUR CODE ENDS HERE
    
    def test_sell_exceeding_position_raises_error(self, broker):
        """
        Verify that selling more than held raises ValueError.
        
        Given: position = 5
        When: SELL 10
        Expected: ValueError with "Insufficient shares"
        """
        # YOUR CODE STARTS HERE
        # Step 1: Buy some shares (e.g., 5)
        # Step 2: Use pytest.raises(ValueError, match="Insufficient shares")
        # Step 3: Attempt to sell more than held
        pass
        # YOUR CODE ENDS HERE
    
    def test_sell_with_zero_position_raises_error(self, broker):
        """
        Verify that selling with no position raises error.
        
        Given: position = 0
        When: SELL 1
        Expected: ValueError
        """
        # YOUR CODE STARTS HERE
        # Step 1: Don't buy anything (position = 0)
        # Step 2: Attempt to sell
        # Step 3: Assert ValueError raised
        pass
        # YOUR CODE ENDS HERE


class TestInputValidation:
    """Test order validation logic."""
    
    def test_invalid_side_raises_error(self, broker):
        """
        Verify that invalid side parameter raises ValueError.
        
        When: side not in ["BUY", "SELL"]
        Expected: ValueError with message about invalid side
        """
        # YOUR CODE STARTS HERE
        # Test invalid sides: "buy", "LONG", "SHORT", "INVALID", etc.
        # Use pytest.raises(ValueError, match="Invalid side")
        pass
        # YOUR CODE ENDS HERE
    
    def test_zero_quantity_raises_error(self, broker):
        """
        Verify that qty=0 raises ValueError.
        
        Expected: ValueError with "qty must be > 0"
        """
        # YOUR CODE STARTS HERE
        # Step 1: Try BUY with qty=0
        # Step 2: Assert ValueError raised
        pass
        # YOUR CODE ENDS HERE
    
    def test_negative_quantity_raises_error(self, broker):
        """
        Verify that negative qty raises ValueError.
        
        Expected: ValueError
        """
        # YOUR CODE STARTS HERE
        # Try qty=-5
        pass
        # YOUR CODE ENDS HERE
    
    def test_negative_price_allowed(self, broker):
        """
        Verify behavior with negative price (edge case).
        
        Note: Current implementation may allow this.
        Decide if you want to add validation or allow it.
        """
        # YOUR CODE STARTS HERE
        # Try executing order with negative price
        # Assert behavior (either raises error or processes)
        # This test documents the current behavior
        pass
        # YOUR CODE ENDS HERE


class TestBuyAndSellRoundTrip:
    """Test buy-then-sell scenarios."""
    
    def test_buy_then_sell_returns_to_original_state(self):
        """
        Verify that buying then selling at same price returns to original state.
        
        Given: cash = $1,000, position = 0
        When: BUY 10 @ $10, then SELL 10 @ $10
        Expected: cash = $1,000, position = 0
        """
        # YOUR CODE STARTS HERE
        # Step 1: Record initial state
        # Step 2: Buy shares
        # Step 3: Sell same shares at same price
        # Step 4: Assert state matches initial
        pass
        # YOUR CODE ENDS HERE
    
    def test_profit_from_price_increase(self, rich_broker):
        """
        Verify that buying low and selling high increases cash.
        
        When: BUY @ $10, SELL @ $15
        Expected: net cash increase of $5 per share
        """
        # YOUR CODE STARTS HERE
        # Step 1: Record initial cash
        # Step 2: Buy at low price
        # Step 3: Sell at high price
        # Step 4: Assert profit = (sell_price - buy_price) * qty
        pass
        # YOUR CODE ENDS HERE
    
    def test_loss_from_price_decrease(self, rich_broker):
        """
        Verify that buying high and selling low decreases cash.
        
        When: BUY @ $15, SELL @ $10
        Expected: net cash decrease of $5 per share
        """
        # YOUR CODE STARTS HERE
        # Step 1: Record initial cash
        # Step 2: Buy at high price
        # Step 3: Sell at low price
        # Step 4: Assert loss = (buy_price - sell_price) * qty
        pass
        # YOUR CODE ENDS HERE


class TestEdgeCases:
    """Test unusual but valid scenarios."""
    
    def test_fractional_price(self, broker):
        """
        Verify that fractional prices work correctly.
        
        When: BUY 10 @ $10.57
        Expected: cash deducted = 105.70
        """
        # YOUR CODE STARTS HERE
        # Step 1: Execute order with fractional price
        # Step 2: Assert cash calculation is precise
        # Hint: Use pytest.approx() for float comparison
        pass
        # YOUR CODE ENDS HERE
    
    def test_large_order(self, rich_broker):
        """
        Verify that large orders work correctly.
        
        When: BUY 100,000 shares @ $5
        Expected: Correct cash deduction and position update
        """
        # YOUR CODE STARTS HERE
        # Step 1: Execute large order
        # Step 2: Assert calculations are correct
        pass
        # YOUR CODE ENDS HERE
    
    def test_many_small_orders(self, rich_broker):
        """
        Verify that many small orders accumulate correctly.
        
        When: Execute 100 orders of 1 share each
        Expected: position = 100, cash accurate
        """
        # YOUR CODE STARTS HERE
        # Step 1: Loop 100 times buying 1 share
        # Step 2: Assert final position and cash
        pass
        # YOUR CODE ENDS HERE
