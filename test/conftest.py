# -*- coding: utf-8 -*-
"""Pytest top-level conftest.py.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import pytest


@pytest.fixture
def show_log_output():
    """Turn on/off example code stdout logging output.

    Returns:
        bool: Boolean value representing if log output is turned on or off.

    """
    log_output = False
    return log_output
