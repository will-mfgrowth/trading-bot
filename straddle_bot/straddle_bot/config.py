from pydantic import BaseModel
from functools import lru_cache
import os

class Settings(BaseModel):
    alpaca_key: str
    alpaca_secret: str
    base_url: str = 'https://paper-api.alpaca.markets'
    data_url: str = 'https://data.alpaca.markets'
    account_id: str | None = None

    class Config:
        extra = 'ignore'

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        alpaca_key=os.getenv('ALPACA_API_KEY_ID', ''),
        alpaca_secret=os.getenv('ALPACA_API_SECRET_KEY', ''),
        base_url=os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets'),
        data_url=os.getenv('ALPACA_DATA_URL', 'https://data.alpaca.markets'),
        account_id=os.getenv('ALPACA_ACCOUNT_ID'),
    )