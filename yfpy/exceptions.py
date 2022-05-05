# -*- coding: utf-8 -*-
"""YFPY module for throwing custom exceptions.

Attributes:
    logger (Logger): Module level logger for usage and debugging.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

from yfpy.logger import get_logger

logger = get_logger(__name__)


class YahooFantasySportsException(Exception):
    """Base YFPY exception class for Yahoo Fantasy Sports API exceptions.
    """
    def __init__(self, message, payload=None, url=None):
        """Instantiate YFPY exception.

        Args:
            message (str): Human readable string describing the exception.
            payload (str, optional): The API exception error payload.
            url (str, optional): Yahoo Fantasy Sports REST API URL.

        Attributes:
            message (str): Human readable string describing the exception.
            payload (str): The API exception error payload.
            url (str): Yahoo Fantasy Sports REST API URL.

        """
        self.message = message
        self.payload = payload
        self.url = url

    def __str__(self):
        return str(self.message)


class YahooFantasySportsDataNotFound(YahooFantasySportsException):
    """YFPY exception when no data was retrieved from the Yahoo Fantasy Sports REST API."""
