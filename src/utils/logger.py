import logging
class Logger:
    def __init__(self, level=logging.INFO):
        logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger()

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)