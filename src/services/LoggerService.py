import logging


class LoggerService:
    def __init__(self):
        formatter = "%(asctime)s - %(message)s"
        logging.basicConfig(format=formatter)

        self.logger = logging.getLogger("CollectorService")
        self.logger.setLevel(logging.DEBUG)


    def log(self, message: str):
        self.logger.log(msg=message, level=logging.INFO)

