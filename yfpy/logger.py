# -*- coding: utf-8 -*-
"""YFPY module for configuring and formatting the custom logger.
"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

from logging import getLogger, Logger, Formatter, StreamHandler, INFO


def get_logger(name: str, level: int = INFO) -> Logger:
    """Get custom YFPY logger object.

    Args:
        name (str): The module name for the logger.
        level (int): The log level for the logger. Default level set to INFO.

    Returns:
        Logger: A Python Logger object with custom configuration and formatting.

    """
    logger = getLogger(name)
    if len(logger.handlers) > 0:
        logger.handlers = []
    if level:
        logger.setLevel(level)

    sh = StreamHandler()
    if level:
        sh.setLevel(level)

    formatter = Formatter(
        fmt="%(asctime)s.%(msecs)03d - %(levelname)s - %(filename)s - %(name)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    sh.setFormatter(formatter)

    logger.addHandler(sh)

    return logger
