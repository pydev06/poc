import logging
import time
from threading import Thread
from .websocket_logging_handler import WebSocketLoggingHandler


class CustomFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        if not filename:
            raise ValueError("Filename must be provided for CustomFileHandler")
        super().__init__(filename, mode, encoding, delay)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        self.setFormatter(formatter)


def log_every_second():
    logger = logging.getLogger('background_logger')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Add handlers if they are not already added
        file_handler = CustomFileHandler('log_file.log')
        websocket_handler = WebSocketLoggingHandler()
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        file_handler.setFormatter(formatter)
        websocket_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(websocket_handler)

    while True:
        logger.info("Logging message every second..")
        time.sleep(1)


# Start the background thread
thread = Thread(target=log_every_second, daemon=True)
thread.start()
