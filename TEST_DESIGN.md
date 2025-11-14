# Test Design Documentation

## Overview

Test suite for a minimal daily-bar backtesting system with 67 unit tests achieving >90% code coverage.

**Testing Philosophy**: Pure functions, deterministic data, fast execution (<60s), no external dependencies.

---

## Architecture

### Component Hierarchy

```
┌─────────────────────────────────────────┐
│           Backtester (Engine)           │  ← Integration layer
├─────────────────────────────────────────┤
│  Strategy        │      Broker          │  ← Business logic layer
└─────────────────────────────────────────┘
```

**Test Strategy**: Bottom-up (unit → integration)

---

## Test Modules

### 1. `test_strategy.py` - Strategy Logic Tests

**Purpose**: Verify signal generation algorithm  
**Class**: `VolatilityBreakoutStrategy`  
**Coverage**: 15 tests

#### Test Categories

**A. Core Functionality** (5 tests)
- `test_signals_returns_correct_length` - Output shape validation
- `test_signals_returns_series_with_same_index` - Index preservation
- `test_signals_only_contain_valid_values` - Signal domain: {-1, 0, 1}
- `test_buy_signal_when_return_exceeds_volatility` - Buy logic
- `test_sell_signal_when_return_below_negative_volatility` - Sell logic

**B. Edge Cases** (4 tests)
- `test_empty_prices_raises_error` - Input validation
- `test_constant_prices_returns_all_zeros` - Zero volatility scenario
- `test_very_short_series` - Series < lookback window
- `test_single_price` - Minimal input

**C. Configuration** (2 tests)
- `test_different_lookback_windows_produce_different_signals` - Parameter sensitivity
- `test_lookback_of_one` - Boundary parameter

**D. Quality Assurance** (1 test)
- `test_repeated_calls_produce_same_signals` - Determinism check

#### Test Data Strategy

| Scenario | Data Type | Purpose |
|----------|-----------|---------|
| Rising prices | `np.linspace(100, 120, 200)` | Trend detection |
| Volatile prices | Seeded random walk | Signal variability |
| Flat prices | `[100] * 20` | Zero-volatility edge case |
| Jump/drop | `[100]*10 + [110]` | Volatility breakout |

---

### 2. `test_broker.py` - Order Execution Tests

**Purpose**: Verify trade execution and state management  
**Class**: `Broker`  
**Coverage**: 27 tests

#### Test Categories

**A. Buy Orders** (5 tests)
- `test_buy_order_deducts_cash` - Cash accounting
- `test_buy_order_increases_position` - Position tracking
- `test_multiple_buy_orders_accumulate_position` - Cumulative trades
- `test_buy_order_with_exact_cash_succeeds` - Boundary condition
- `test_buy_order_exceeding_cash_raises_error` - Constraint validation

**B. Sell Orders** (5 tests)
- `test_sell_order_increases_cash` - Cash accounting
- `test_sell_order_decreases_position` - Position tracking
- `test_sell_entire_position` - Exit scenario
- `test_sell_exceeding_position_raises_error` - Constraint validation
- `test_sell_with_zero_position_raises_error` - Invalid state

**C. Input Validation** (4 tests)
- `test_invalid_side_raises_error` - Side ∈ {BUY, SELL}
- `test_zero_quantity_raises_error` - qty > 0
- `test_negative_quantity_raises_error` - qty validation
- `test_negative_price_allowed` - Price edge case

**D. Round-Trip Trades** (3 tests)
- `test_buy_then_sell_returns_to_original_state` - Idempotence
- `test_profit_from_price_increase` - PnL calculation
- `test_loss_from_price_decrease` - PnL calculation

**E. Edge Cases** (3 tests)
- `test_fractional_price` - Float precision
- `test_large_order` - Scale testing
- `test_many_small_orders` - Accumulation accuracy

#### Invariants Tested

```python
# State consistency
cash + position × price = equity

# Constraint enforcement
buy: cash ≥ qty × price
sell: position ≥ qty

# Transaction correctness
Δcash = -qty × price  (buy)
Δcash = +qty × price  (sell)
```

---

### 3. `test_engine.py` - Backtester Integration Tests

**Purpose**: Verify end-to-end backtest execution  
**Class**: `Backtester`  
**Coverage**: 25 tests

#### Test Categories

**A. Basic Execution** (4 tests)
- `test_run_returns_dataframe` - Return type validation
- `test_output_length_matches_input` - Output shape
- `test_output_index_matches_input` - Index alignment
- `test_initial_state_reflects_broker_starting_values` - Initial conditions

**B. Trading Logic** (3 tests)
- `test_buy_signal_executes_trade` - Long execution
- `test_sell_signal_executes_trade` - Short execution
- `test_hold_signal_executes_no_trade` - No-op handling

**C. Signal Timing** (3 tests)
- `test_uses_previous_signal_for_current_trade` - t-1 signal → t trade
- `test_first_bar_has_no_trade` - No look-ahead bias
- `test_signal_changes_trigger_trades` - Transition detection

**D. Equity Calculation** (3 tests)
- `test_equity_equals_cash_plus_position_value` - Accounting formula
- `test_equity_reflects_price_changes` - Mark-to-market
- `test_final_equity_matches_liquidation_value` - Terminal state

**E. Integration** (2 tests)
- `test_end_to_end_with_real_strategy` - Full pipeline
- `test_backtest_is_deterministic` - Reproducibility

**F. Error Handling** (3 tests)
- `test_broker_error_propagates` - Exception propagation
- `test_strategy_error_propagates` - Exception propagation
- `test_insufficient_cash_stops_backtest` - Constraint violation

**G. Edge Cases** (3 tests)
- `test_empty_prices_series` - Empty input
- `test_single_price_point` - Minimal input
- `test_very_long_price_series` - Scale testing

**H. Mocked Scenarios** (4 tests)
- `test_alternating_signals` - Complex signal pattern
- `test_buy_and_hold_scenario` - Static position
- `test_round_trip_trade` - Entry/exit cycle

#### Key Test Pattern: Mock Strategy

```python
# Control exact signal sequence for precise testing
mock_strategy = MagicMock()
mock_strategy.signals.return_value = pd.Series([0, 0, 1, 1, 0, -1])

# Verify expected position transitions
# Bar 0: pos=0, Bar 3: pos=1 (buy), Bar 5: pos=0 (sell), Bar 6: pos=-1 (short)
```

---

## Shared Fixtures (`conftest.py`)

### Price Fixtures

| Fixture | Description | Use Case |
|---------|-------------|----------|
| `simple_prices` | 10-day rising series | Quick smoke tests |
| `long_prices` | 200-day series | Rolling window tests |
| `volatile_prices` | Seeded random walk | Signal generation |
| `constant_prices` | Flat series | Zero-volatility edge case |

### Component Fixtures

| Fixture | Configuration | Purpose |
|---------|---------------|---------|
| `strategy` | lookback=20 | Default strategy |
| `short_lookback_strategy` | lookback=5 | Parameter testing |
| `broker` | cash=1,000 | Resource-constrained testing |
| `rich_broker` | cash=1,000,000 | Unconstrained testing |

---

## Testing Principles

### 1. Arrange-Act-Assert (AAA)

```python
def test_example():
    # ARRANGE: Set up test data
    broker = Broker(cash=1000)
    
    # ACT: Execute the operation
    broker.market_order("BUY", 5, 10.0)
    
    # ASSERT: Verify expectations
    assert broker.cash == 950
    assert broker.position == 5
```

### 2. Determinism

- ✅ Seeded randomness: `np.random.seed(42)`
- ✅ Synthetic data: `np.linspace()`, manual series
- ❌ No network calls
- ❌ No file I/O
- ❌ No system time dependencies

### 3. Isolation

- Each test runs independently
- Fixtures create fresh instances
- No shared mutable state
- Tests can run in any order

### 4. Fast Execution

- Target: <60 seconds total
- Actual: ~2-5 seconds
- No sleep() or delays
- Minimal test data (10-200 points)

---

## Coverage Strategy

### Target: ≥90% Line Coverage

**Covered**:
- ✅ All public methods
- ✅ Happy paths
- ✅ Error paths
- ✅ Edge cases
- ✅ Boundary conditions

**Intentionally Excluded**:
- Test files themselves
- `__init__.py` files
- `conftest.py` fixtures

### Coverage Gaps Acceptable

- Unreachable code branches
- Defensive assertions
- Debug logging

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
1. Install dependencies (requirements.txt)
2. Run tests: pytest -v
3. Generate coverage: coverage run -m pytest
4. Enforce threshold: coverage report --fail-under=90
5. Upload artifacts: coverage HTML report
```

### Success Criteria

- ✅ All tests pass
- ✅ Coverage ≥ 90%
- ✅ Execution time < 60s
- ✅ No deprecation warnings

---

## Test Metrics

| Metric | Value |
|--------|-------|
| Total tests | 67 |
| Strategy tests | 15 |
| Broker tests | 27 |
| Engine tests | 25 |
| Line coverage | 97% |
| Execution time | ~3s |
| Fixtures | 8 |

---

## Running Tests

### Local Development

```bash
# Run all tests
pytest -v

# Run specific module
pytest tests/test_broker.py -v

# Run specific test
pytest tests/test_broker.py::TestBuyOrders::test_buy_order_deducts_cash -v

# With coverage
coverage run -m pytest
coverage report -m
coverage html
```

### Configuration Files

- `pytest.ini` - pytest configuration, pythonpath
- `.coveragerc` - coverage measurement settings
- `requirements.txt` - test dependencies

---

## Design Rationale

### Why This Structure?

1. **Bottom-up testing**: Unit tests before integration
2. **Clear boundaries**: Each component tested independently
3. **Mock judiciously**: Only for signal control in engine tests
4. **Real integration**: Engine tests use actual Strategy + Broker when possible
5. **Comprehensive edge cases**: Empty, single, large, constant inputs

### Trade-offs

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| 67 tests | High confidence, good coverage | Maintenance overhead |
| Mocked signals | Precise control of test scenarios | Less realistic in some cases |
| Synthetic data | Deterministic, fast | Doesn't test real market behavior |
| No parametrize | Explicit, readable tests | Some duplication |

---

## Future Enhancements

- [ ] Parametrized tests to reduce duplication
- [ ] Property-based testing with Hypothesis
- [ ] Performance benchmarks
- [ ] Mutation testing for test quality
- [ ] Integration with real market data (separate suite)

---

**Version**: 1.0  
**Last Updated**: 2025  
**File**: Assignment 5 - Testing & CI in Financial Engineering
