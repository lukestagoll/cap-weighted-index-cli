from numpy import float64

from cap_weighted_index_cli.logging.logger import get_console

def log_profit(funds_start: float64, funds_end: float64):
    console = get_console()
    
    diff = funds_end - funds_start
    pct_change = (diff / funds_start) * 100
    status = "profit" if diff > 0 else "loss" if diff < 0 else "no change"
    
    style = "[yellow]You Broke Even - "
    
    if diff > 0:
        style = "[green]You Made a Profit of "
    elif diff < 0:
        style = "[red]You Lost "
        
    console.print(f"{style}${abs(diff):,.2f} ({pct_change:,.2f}%)")
