# Alpaca Short Straddle Trading Bot

A Python trading bot that implements short straddle strategies using the Alpaca Trading API. Short straddles profit from low volatility by selling both call and put options at the same strike price and expiration date.

## Features

- **Short Straddle Strategy**: Automatically places sell-to-open orders for both call and put options
- **Paper Trading**: Safe testing environment using Alpaca's paper trading
- **CLI Interface**: Easy-to-use command line interface
- **Risk Management**: Configurable position sizing and limit orders
- **OCC Symbol Generation**: Automatic options contract symbol formatting

## Quick Start

### 1. Installation

```bash
cd straddle_bot
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file with your Alpaca API credentials:

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

Required environment variables:
- `ALPACA_API_KEY_ID`: Your Alpaca API key
- `ALPACA_API_SECRET_KEY`: Your Alpaca secret key

### 3. Check Configuration

```bash
python main.py check-config
```

### 4. Run the Bot

Open a short straddle on SPY expiring in 7 days:

```bash
python main.py open-straddle SPY
```

With custom parameters:

```bash
python main.py open-straddle AAPL --expiry-days 14 --qty 2 --limit-credit 5.50
```

## Commands

### `open-straddle`
Opens a short straddle position.

**Arguments:**
- `symbol`: Stock symbol (e.g., AAPL, SPY)

**Options:**
- `--expiry-days`: Days until expiration (default: 7)
- `--qty`: Number of contracts (default: 1)
- `--limit-credit`: Limit price for credit received (optional)

### `check-config`
Validates your API configuration.

## How It Works

1. **Price Discovery**: Fetches the current stock price using Alpaca's market data API
2. **Strike Selection**: Finds the nearest at-the-money strike price
3. **Symbol Generation**: Creates OCC-formatted option symbols for both call and put
4. **Order Placement**: Submits a multi-leg order to sell both options simultaneously
5. **Monitoring**: Logs order status and provides order ID for tracking

## Strategy Details

**Short Straddle:**
- Sell 1 call option at strike K
- Sell 1 put option at strike K (same expiration)
- Profit when stock price stays near strike K
- Maximum profit = premium collected
- Risk = unlimited if stock moves significantly

**Best Market Conditions:**
- Low implied volatility
- Stocks expected to trade sideways
- High time decay (theta positive)

## Risk Warning

⚠️ **Options trading involves significant risk and is not suitable for all investors.**

Short straddles have **unlimited risk** if the underlying stock moves significantly in either direction. Always:
- Start with paper trading
- Use appropriate position sizing
- Monitor positions closely
- Have an exit strategy
- Understand margin requirements

## Paper vs Live Trading

By default, the bot uses Alpaca's paper trading environment. To switch to live trading:

1. Set `ALPACA_BASE_URL=https://api.alpaca.markets` in your `.env` file
2. Ensure your account has sufficient funds and options trading approval
3. Verify you have Level 3 options trading permissions for multi-leg strategies

## Requirements

- Python 3.8+
- Alpaca brokerage account with options trading enabled
- Level 3 options trading approval for multi-leg strategies

## Dependencies

See `requirements.txt` for full list. Key dependencies:
- `alpaca-py`: Official Alpaca Python SDK
- `typer`: CLI framework
- `rich`: Terminal formatting
- `pydantic`: Data validation
- `pendulum`: Date/time handling