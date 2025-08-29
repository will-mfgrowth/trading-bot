import math
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class OptionContractId:
    symbol: str
    expiration: str  # YYYY-MM-DD
    strike: float
    right: str  # 'C' or 'P'

    def occ_symbol(self) -> str:
        """Convert to OCC format like AAPL240920C00190000"""
        import datetime as dt
        d = dt.datetime.strptime(self.expiration, '%Y-%m-%d')
        ymd = d.strftime('%y%m%d')
        strike_int = int(round(self.strike * 1000))
        return f"{self.symbol}{ymd}{self.right}{strike_int:08d}"

def nearest_atm_strike(underlying_price: float, increment: float = 1.0) -> float:
    """Round price to nearest strike increment (e.g., $1 or $5 increments)"""
    steps = round(underlying_price / increment)
    return round(steps * increment, 2)