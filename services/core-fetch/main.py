import logging
from core_fetch.scheduler import start_scheduler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_scheduler()
