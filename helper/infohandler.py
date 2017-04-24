import logging


class InfoHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)

    def emit(self, record):
        if not record.levelno == logging.INFO:
            return
        logging.FileHandler.emit(self, record)