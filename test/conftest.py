__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import pytest


@pytest.fixture
def show_log_output():
    """Turn on/off example code stdout logging output"""
    log_output = False
    return log_output
