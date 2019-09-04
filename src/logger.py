import sys
import logging


class Logger:
    FORMAT = '%(asctime)s - %(levelname)s - (%(threadName)s) - %(message)s'
    instance = None

    def __init__(self, name: str = __name__):
        if self.__class__.instance is None:
            raise Exception('Tried to allocate a second instance of a singleton.\nUse getInstance() instead.')
            sys.exit(-1)

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        log_formatter = logging.Formatter(self.__class__.FORMAT)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_formatter)
        console_handler.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler('Tweets-Collector.log')
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.INFO)

        if logger.handlers:
            logger.handlers = []

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        self.__class__.instance = logger

    @classmethod
    def get_instance(cls, name: str = __name__):
        if cls.instance is None:
            return cls(name)
        return cls.instance

    def debug(self, message: str):
        self.__class__.instance.debug(message)

    def info(self, message: str):
        self.__class__.instance.info(message)

    def warn(self, message: str):
        self.__class__.instance.warn(message)

    def error(self, message: str):
        self.__class__.instance.error(message)

    def critical(self, message: str):
        self.__class__.instance.critical(message)

    def exception(self, message: str):
        self.__class__.instance.exception(message)
