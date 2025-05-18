import logging
from rich.console import Console
from rich.logging import RichHandler

console = Console()


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler()]
)
logger = logging.getLogger("rich")

def log_info(message):
    logger.info(message)

def log_error(e):
    logger.exception(e)
    
def get_console():
    return console