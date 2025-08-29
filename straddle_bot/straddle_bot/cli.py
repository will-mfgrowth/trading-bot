import os
import logging
import typer
from rich.console import Console
from dotenv import load_dotenv
from .config import get_settings
from .strategy import ShortStraddleStrategy

app = typer.Typer(add_completion=False, help="Alpaca Short Straddle Trading Bot")
console = Console()

@app.command()
def open_straddle(
    symbol: str = typer.Argument(..., help="Stock symbol (e.g., AAPL, SPY)"),
    expiry_days: int = typer.Option(7, help="Days until expiration"),
    qty: int = typer.Option(1, help="Number of contracts"),
    limit_credit: float = typer.Option(None, help="Limit price for credit received")
):
    """Open a short straddle position"""
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    s = get_settings()
    if not s.alpaca_key or not s.alpaca_secret:
        console.print('[red]Missing ALPACA_API_KEY_ID or ALPACA_API_SECRET_KEY environment variables[/red]')
        console.print('[yellow]Create a .env file with your Alpaca API credentials[/yellow]')
        raise typer.Exit(code=1)
    
    console.print(f'[blue]Opening short straddle on {symbol}[/blue]')
    console.print(f'[blue]Expiry: {expiry_days} days, Quantity: {qty}, Limit: {limit_credit}[/blue]')
    
    try:
        strat = ShortStraddleStrategy(symbol=symbol, expiry_days=expiry_days, qty=qty, limit_credit=limit_credit)
        order_id = strat.run_once()
        console.print(f'[green]✓ Submitted straddle order id={order_id}[/green]')
    except Exception as e:
        console.print(f'[red]✗ Error: {e}[/red]')
        raise typer.Exit(code=1)

@app.command()
def check_config():
    """Check API configuration"""
    load_dotenv()
    s = get_settings()
    
    console.print("[blue]Configuration Status:[/blue]")
    console.print(f"API Key: {'✓ Set' if s.alpaca_key else '✗ Missing'}")
    console.print(f"Secret: {'✓ Set' if s.alpaca_secret else '✗ Missing'}")
    console.print(f"Base URL: {s.base_url}")
    console.print(f"Data URL: {s.data_url}")
    
    if not s.alpaca_key or not s.alpaca_secret:
        console.print("\n[yellow]Create a .env file with:[/yellow]")
        console.print("ALPACA_API_KEY_ID=your_key_here")
        console.print("ALPACA_API_SECRET_KEY=your_secret_here")

if __name__ == '__main__':
    app()