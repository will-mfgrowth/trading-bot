import logging
from typing import Optional
import pendulum as pl
from alpaca.data.requests import StockLatestTradeRequest
from .alpaca_client import get_clients, place_short_straddle
from .options_utils import nearest_atm_strike

logger = logging.getLogger(__name__)

class ShortStraddleStrategy:
    def __init__(self, symbol: str, expiry_days: int = 7, qty: int = 1, limit_credit: Optional[float] = None):
        self.symbol = symbol
        self.expiry_days = expiry_days
        self.qty = qty
        self.limit_credit = limit_credit

    def run_once(self) -> Optional[str]:
        """Execute short straddle strategy once"""
        clients = get_clients()
        
        # Calculate expiry date
        now = pl.now('America/New_York')
        expiry = now.add(days=self.expiry_days).format('YYYY-MM-DD')
        
        # Get current stock price
        latest = clients.data.get_stock_latest_trade(StockLatestTradeRequest(symbol_or_symbols=self.symbol))
        last_price = float(latest[self.symbol].price)
        
        # Find nearest ATM strike
        strike = nearest_atm_strike(last_price, increment=1.0)
        
        # Place the short straddle order
        order_id = place_short_straddle(self.symbol, expiry, strike, self.qty, self.limit_credit)
        
        logger.info('Opened short straddle on %s exp=%s strike=%.2f id=%s', 
                   self.symbol, expiry, strike, order_id)
        return order_id