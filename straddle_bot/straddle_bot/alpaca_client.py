import logging
from typing import Optional, List
from dataclasses import dataclass
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import LimitOrderRequest, OptionLegRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType, OrderClass, PositionIntent
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestTradeRequest
from .config import get_settings

logger = logging.getLogger(__name__)

@dataclass
class AlpacaClients:
    trading: TradingClient
    data: StockHistoricalDataClient

def get_clients() -> AlpacaClients:
    s = get_settings()
    trading = TradingClient(api_key=s.alpaca_key, secret_key=s.alpaca_secret, paper='paper' in s.base_url)
    data = StockHistoricalDataClient(api_key=s.alpaca_key, secret_key=s.alpaca_secret)
    return AlpacaClients(trading=trading, data=data)

def place_short_straddle(symbol: str, expiration: str, strike: float, quantity: int, limit_price: Optional[float]) -> str:
    """Place a short straddle (sell call + sell put at same strike/expiry)"""
    clients = get_clients()
    
    # Construct OCC symbols (e.g., AAPL240920C00190000)
    def occ(sym: str, exp: str, typ: str, strike_price: float) -> str:
        import datetime as dt
        d = dt.datetime.strptime(exp, '%Y-%m-%d')
        y = d.strftime('%y')
        m = d.strftime('%m')
        da = d.strftime('%d')
        strike_int = int(round(strike_price * 1000))
        return f"{sym}{y}{m}{da}{typ}{strike_int:08d}"

    call_symbol = occ(symbol, expiration, 'C', strike)
    put_symbol = occ(symbol, expiration, 'P', strike)

    legs: List[OptionLegRequest] = [
        OptionLegRequest(
            symbol=call_symbol, 
            ratio_qty=quantity, 
            side=OrderSide.SELL,
            position_intent=PositionIntent.SELL_TO_OPEN
        ),
        OptionLegRequest(
            symbol=put_symbol, 
            ratio_qty=quantity, 
            side=OrderSide.SELL,
            position_intent=PositionIntent.SELL_TO_OPEN
        ),
    ]

    if limit_price is not None:
        req = LimitOrderRequest(
            symbol=symbol,
            time_in_force=TimeInForce.DAY,
            order_class=OrderClass.MLEG,
            legs=legs,
            limit_price=limit_price,
        )
    else:
        # Market order for multi-leg
        from alpaca.trading.requests import MarketOrderRequest
        req = MarketOrderRequest(
            symbol=symbol,
            time_in_force=TimeInForce.DAY,
            order_class=OrderClass.MLEG,
            legs=legs,
        )

    order = clients.trading.submit_order(req)
    logger.info('Submitted short straddle %s x%d @ %s, id=%s', symbol, quantity, str(limit_price), order.id)
    return order.id