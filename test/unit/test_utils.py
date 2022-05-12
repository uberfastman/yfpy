# -*- coding: utf-8 -*-
"""Pytest unit tests for YFPY utils module.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import pytest

from yfpy.utils import prettify_data


@pytest.mark.unit
def test_prettify_data():
    """Unit test for util used to prettify JSON strings.

    Note:
        Tests :func:`~yfpy.utils.prettify_data`.

    Returns:
        None

    """
    result = prettify_data('{"test_key": "test_value"}')
    print(result)

    expected = (
        '\n'
        '"{'
        '\\"test_key\\": \\"test_value\\"'
        '}"'
        '\n'
    )

    assert result == expected


@pytest.mark.unit
def test_unpack_data():
    """Unit test for util used to unpack nested data.

    Note:
        Tests :func:`~yfpy.utils.unpack_data`.

    TODO: write unit test

    Returns:
        None

    """


@pytest.mark.unit
def test_convert_strings_to_numeric_equivalents():
    """Unit test for util used to convert strings to their numerical equivalents.

    Note:
        Tests :func:`~yfpy.utils.convert_strings_to_numeric_equivalents`.

    TODO: write unit test

    Returns:
        None

    """


@pytest.mark.unit
def test_get_type():
    """Unit test for util used to get Python object types.

    Note:
        Tests :func:`~yfpy.utils.get_type`.

    TODO: write unit test

    Returns:
        None

    """


@pytest.mark.unit
def test_flatten_json_dict_list():
    """Unit test for util used to flatten a JSON list of dictionaries with unique keys to a Python dictionary.

    Note:
        Tests :func:`~yfpy.utils.flatten_json_dict_list`.

    TODO: write unit test

    Returns:
        None

    """


@pytest.mark.unit
def test_flatten_to_list():
    """Unit test for util used to flatten a JSON dictionary with extraneous keys to a Python list.

    Note:
        Tests :func:`~yfpy.utils.flatten_to_list`.

    TODO: write unit test

    Returns:
        None

    """


@pytest.mark.unit
def test_flatten_to_objects():
    """Unit test for util used to flatten a JSON dictionary to a Python dictionary of class instances.

    Note:
        Tests :func:`~yfpy.utils.flatten_to_objects`.

    TODO: write unit test

    Returns:
        None

    """


@pytest.mark.unit
def test_dict_to_list():
    """Unit test for util used to convert a JSON dictionary to a list.

    Note:
        Tests :func:`~yfpy.utils.dict_to_list`.

    TODO: write unit test

    Returns:
        None

    """


@pytest.mark.unit
def test_reorganize_json_dict():
    """Unit test for util used to reorder a JSON dictionary of dictionaries to a Python OrderedDict sorted by a key.

    Note:
        Tests :func:`~yfpy.utils.reorganize_json_dict`.

    TODO: write unit test

    Returns:
        None

    """


@pytest.mark.unit
def test_complex_json_handler():
    """Unit test for custom JSON handler built to handle serialization/deserialization of YFPY objects.

    Note:
        Tests :func:`~yfpy.utils.complex_json_handler`.

    TODO: write unit test

    Returns:
        None

    """


@pytest.mark.unit
def test_reformat_json_list():
    """Unit test for util used clean and reformat a JSON list.

    Note:
        Tests :func:`~yfpy.utils.reformat_json_list`.

    TODO: write unit test

    Returns:
        None

    """
