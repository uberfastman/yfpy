__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

from yfpy.logger import get_logger

logger = get_logger(__name__)


class YahooFantasySportsException(Exception):
    """Base yfpy exception class for Yahoo Fantasy Sport API exceptions."""

    def __init__(self, message, payload=None, url=None):
        self.message = message
        self.payload = payload
        self.url = url

    def __str__(self):
        return str(self.message)


class YahooFantasySportsDataNotFound(YahooFantasySportsException):
    """Yfpy exception when no data was retrieved from the Yahoo fantasy sports API."""
