__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import logging

logger = logging.getLogger(__name__)


class YahooFantasySportsException(Exception):
    """Base yfpy exception class for Yahoo Fantasy Sport API exceptions."""


class YahooFantasySportsDataNotFound(YahooFantasySportsException):
    """Yfpy exception when no data was retrieved from the Yahoo fantasy sports API."""

    def __init__(self, message, payload=None):
        self.message = message
        self.payload = payload

    def __str__(self):
        return str(self.message)
