import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Backtester:
    """
    End-of-day backtester loop.

    On each bar t:
    1. Compute signal from t-1 prices (look-back)
    2. If signal changed, execute trade at close of t
    3. Track cash, position, and equity

    Args:
        strategy: object with .signals(prices) -> pd.Series method
        broker: Broker object with .market_order() method

    Returns:
        pd.DataFrame with columns [equity, cash, position] indexed by date
    """

    def __init__(self, strategy, broker):
        self.strategy = strategy
        self.broker = broker

    def run(self, prices: pd.Series) -> pd.DataFrame:
        """
        Run the backtest over a price series.

        High-level algorithm:
        1. Compute signals for entire price history
        2. Loop through each day t (starting t=1):
           a. Get signal from t-1
           b. Determine trade action (current position vs. signal)
           c. If action needed, execute market_order at prices[t]
           d. Record cash, position, equity
        3. Return historical record

        Args:
            prices: pd.Series of daily prices

        Returns:
            pd.DataFrame with index=dates, columns=[equity, cash, position]

        Example:
            prices = pd.Series([100, 101, 102, 103], index=pd.date_range('2023-01-01', periods=4))
            result = backtester.run(prices)
            print(result)
            #                  equity    cash  position
            # 2023-01-01       1000000  1000000         0
            # 2023-01-02       1000100  999900          1
            # ...
        """
        # YOUR CODE STARTS HERE
        # Step 1: Get signals for all days
        # Step 2: Initialize tracking lists for results
        # Step 3: Loop from index 1 to len(prices)
        #   - Check signal at t-1
        #   - Determine if we need to change position
        #   - Execute trade if needed
        #   - Calculate equity = cash + position * current_price
        #   - Store results
        # Step 4: Return as DataFrame
        signals = self.strategy.signals(prices)
        equity = [self.broker.cash + self.broker.position * prices.iloc[0], ]
        cash = [self.broker.cash,]
        position = [self.broker.position,]
        for i in range(1, len(prices)):
            target_position = signals.iloc[i-1]
            curr_position = self.broker.position
            qty = target_position - curr_position
            abs_qty = abs(qty)

            if qty != 0:
                side = "BUY" if qty > 0 else "SELL"
                # execute trade
                self.broker.market_order(side, abs_qty, prices.iloc[i])

            cash.append(self.broker.cash)
            position.append(self.broker.position)
            equity.append(cash[-1] + position[-1] * prices.iloc[i])

        result = pd.DataFrame({
            'equity': equity,
            'cash': cash,
            'position': position
        }, index=prices.index)

        return result
        # YOUR CODE ENDS HERE