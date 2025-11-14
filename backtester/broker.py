class Broker:
    """
    A deterministic broker for backtesting. No slippage, no fees.

    Tracks:
    - cash: available capital
    - position: number of shares held (can be positive or negative)

    Args:
        cash (float): starting capital (default 1M)

    Example:
        broker = Broker(cash=10_000)
        broker.market_order("BUY", 10, 50.0)  # buy 10 @ $50 = -$500 cash
        # broker.cash == 9_500, broker.position == 10
    """

    def __init__(self, cash: float = 1_000_000):
        self.cash = cash
        self.position = 0

    def market_order(self, side: str, qty: int, price: float) -> None:
        """
        Execute a market order. Updates cash and position.

        Validation:
        - side must be "BUY" or "SELL"
        - qty must be > 0
        - For "SELL", check position >= qty
        - For "BUY", check cash >= qty * price

        Args:
            side (str): "BUY" or "SELL"
            qty (int): number of shares (must be > 0)
            price (float): price per share

        Raises:
            ValueError: if side not recognized or qty <= 0
            ValueError: if insufficient cash (BUY) or shares (SELL)

        Example:
            broker.market_order("BUY", 5, 100.0)
            # Deduct 500 from cash, add 5 to position
        """

        # YOUR CODE STARTS HERE
        # Step 1: Validate side and qty
        # Step 2: Calculate trade cost (qty * price)
        # Step 3: Check constraints (cash for BUY, position for SELL)
        # Step 4: Update cash and position
        if qty <= 0:
            raise ValueError("qty must be > 0")

        if side == "BUY":
            cost = qty * price
            if cost > self.cash:
                raise ValueError("Insufficient cash")
            self.cash -= cost
            self.position += qty
        elif side == "SELL":
            # allow short selling
            self.cash += qty * price
            self.position -= qty
        else:
            raise ValueError(f"Invalid side: {side}")

        # YOUR CODE ENDS HERE