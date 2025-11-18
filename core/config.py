import logging
import sys

class Config:
    DEBUG = False
    LOG_LEVEL = logging.INFO
    GRID_SIZE = (20, 20)
    DEFAULT_SPEED = 200

    @classmethod
    def set_debug(cls, debug):
        cls.DEBUG = debug
        cls.LOG_LEVEL = logging.DEBUG if debug else logging.INFO

    @classmethod
    def setup_logging(cls):
        logging.basicConfig(
            level=cls.LOG_LEVEL,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
