import threading
import time
import logging

logger = logging.getLogger(__name__)


def log_data():
    while True:
        logger.debug("Logging data every second...")
        time.sleep(1)


def start_logging_task():
    thread = threading.Thread(target=log_data)
    thread.daemon = True  # Daemonize thread
    thread.start()


# if __name__ == "__main__":
#     start_logging_task()
