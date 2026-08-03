import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

from api.services.queue import start_consumer
from api.services.trade_execution import execute_order

if __name__ == "__main__":
    print("Starting order consumer...")
    start_consumer(execute_order)
