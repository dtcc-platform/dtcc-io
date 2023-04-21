# Copyright(C) 2023 Anders Logg
# Licensed under the MIT License

import logging

format = "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
logging.basicConfig(format=format)
logger = logging.getLogger("dtcc_io")


debug = logger.debug
info = logger.info
warning = logger.warning


def error(msg):
    logger.error(msg)
    raise RuntimeError(msg)


def critical(msg):
    logger.critical(msg)
    raise RuntimeError(msg)


def set_log_level(level):
    "Set log level"
    logger.setLevel(level)
