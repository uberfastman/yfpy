# -*- coding: utf-8 -*-
"""YFPY module for managing complex JSON data structures.

Attributes:
    logger (Logger): Module level logger for usage and debugging.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import json
import re
from collections import ChainMap, OrderedDict
from typing import Any, Union, Type, Dict, List

import stringcase

from yfpy.logger import get_logger

logger = get_logger(__name__)


def prettify_data(data: object) -> str:
    """Function to return pretty formatted JSON strings for easily readable output from objects.

    Args:
        data (object): Data object to be printed as an easily readable JSON string.

    Returns:
        str: JSON string that has been formatted with indents (two spaces).

    """
    return f"\n{json.dumps(data, indent=2, default=complex_json_handler, ensure_ascii=False)}\n"


# noinspection PyTypeChecker
def unpack_data(json_obj: Any, parent_class: Type = None) -> Any:
    """Recursive function to parse, clean, and assign custom data types to retrieved Yahoo Fantasy Sports data.

    Args:
        json_obj (Any): JSON object for parsing (can be a dictionary, list, or primitive).
        parent_class (Type): Parent class type used to extract custom subclass type options for casting.

    Returns:
        Any: Recursively returns JSON objects until data is completely parsed, cleaned, and typed (where applicable).

    """
    # extract subclasses from parent class for typing
    subclasses = {}
    if parent_class:
        subclasses = {stringcase.snakecase(cls.__name__): cls for cls in parent_class.__subclasses__()}

    # discard empty lists and dictionaries and include when json value = 0
    if json_obj == 0 or json_obj:
        # handle lists
        if isinstance(json_obj, list):
            json_obj = [obj for obj in json_obj if (obj == 0 or obj)]

            if len(json_obj) == 1:
                return unpack_data(json_obj[0], parent_class)
            else:
                # flatten list of dicts if any objects in the list are dicts
                if any(isinstance(obj, dict) for obj in json_obj):
                    return flatten_json_dict_list(json_obj, parent_class)

                return [unpack_data(obj, parent_class) for obj in json_obj if (obj == 0 or obj)]

        # handle dictionaries
        elif isinstance(json_obj, dict):

            # eliminate odd single-key Yahoo dicts with key = "0" and value = <next layer of desired data>
            if "0" in json_obj.keys() and "1" not in json_obj.keys():
                if len(json_obj.keys()) == 1:
                    return unpack_data(json_obj.get("0"), parent_class)
                else:
                    if isinstance(json_obj.get("0"), dict):
                        json_obj.update(json_obj.pop("0"))

            # eliminate data obj counts (except in player_position dicts, which have position counts in league settings)
            if "count" in json_obj.keys() and "position" in json_obj.keys():
                # assign/cast data type where applicable
                # TODO: figure out how to do this without explicit object type keys
                return get_type(
                    {k: unpack_data(v, parent_class) for k, v in json_obj.items()},
                    parent_class,
                    subclasses
                )
            else:
                # assign/cast data type where applicable
                # TODO: figure out how to do this without explicit object type keys
                json_obj = get_type(
                    dict({k: unpack_data(v, parent_class) for k, v in json_obj.items() if k != "count"}),
                    parent_class,
                    subclasses
                )

                # flatten dicts with keys "0", "1",..., "n" to a list of objects
                if "0" in json_obj.keys() and "1" in json_obj.keys():
                    json_obj = flatten_to_list(json_obj)
                # TODO: figure out how to do this without breaking the above unpacking using explicit type keys
                # else:
                #     # flatten dicts with redundant keys to a list of objects
                #     if len(json_obj.keys()) == 1 and len(json_obj.values()) == 1:
                #         key = list(json_obj.keys())[0]
                #         value = list(json_obj.values())[0]
                #         json_obj = value

                return json_obj
        else:
            return convert_strings_to_numeric_equivalents(json_obj)


def convert_strings_to_numeric_equivalents(json_obj: Any) -> Union[int, float, Any]:
    """Convert JSON strings with integer or float numeric representations to their respective integer or float values.

    Args:
        json_obj (Any): JSON object (typically a dictionary or list, but can also be a primitive).

    Returns:
        int | float | Any: The numeric representation of any JSON strings that can be represented as integers or floats,
        else the original JSON object.

    """
    if type(json_obj) == str:

        if len(json_obj) > 1 and str.startswith(json_obj, "0"):
            return json_obj
        else:
            if str.isdigit(json_obj):
                return int(json_obj)
            elif str.isdigit(re.sub("[-]", "", re.sub("[.]", "", json_obj, count=1), count=1)):
                return float(json_obj)
            else:
                return json_obj
    else:
        return json_obj


def get_type(json_obj_dict: Dict[str, Any], parent_class: Type, subclasses: Dict[str, Type]) -> Dict[str, Any]:
    """Cast JSON object to custom subclass type extracted from parent class.

    Args:
        json_obj_dict (dict of str: Any): JSON dictionary with strings of data type as keys and JSON objects as values.
        parent_class (Type): Parent class from which to derive subclasses for casting.
        subclasses (dict of str: Type): Dictionary of subclasses with strings that match the json dict keys as keys
            and classes for casting as values.

    Returns:
        object: A Python object (representing the original JSON object) that has been cast to the specified type.

    """
    for k, v in json_obj_dict.items():
        # check if key is in the provided subclasses' dict, that the object isn't already cast
        if k in subclasses.keys() and isinstance(v, dict) and not isinstance(v, subclasses.get(k)):
            json_obj_dict[k] = subclasses[k](unpack_data(v, parent_class))
    return json_obj_dict


def flatten_json_dict_list(json_obj_dict_list: List[Dict[str, Any]], parent_class: Type) -> Any:
    """Recursive function to flatten JSON lists containing all disparate JSON dictionaries with no overlapping keys.

    Args:
        json_obj_dict_list (list[dict[str, Any]]): List of JSON dictionaries.
        parent_class (Type): Parent class type used to extract custom subclass type options.

    Returns:
        dict | list: Returns a dictionary if the list was flattened, else a cleaned list if no flattening was needed.

    """
    # filter out empty lists and dicts but include when value = 0
    json_obj_dict_list = [obj for obj in json_obj_dict_list if (obj == 0 or obj)]
    item_keys = []
    ndx = 0
    for item in json_obj_dict_list:
        if isinstance(item, list):
            flattened_item = flatten_json_dict_list(item, parent_class)
            json_obj_dict_list[ndx] = flattened_item
            item_keys.extend(list(flattened_item.keys()))
        else:
            item_keys.extend(list(item.keys()))
        ndx += 1

    if len(item_keys) == len(set(item_keys)):
        agg_dict = {}
        for dict_item in json_obj_dict_list:
            agg_dict.update(dict_item)

        return unpack_data(agg_dict, parent_class)
    else:
        return [unpack_data(obj, parent_class) for obj in json_obj_dict_list if (obj == 0 or obj)]


def flatten_to_list(json_obj: Any) -> Any:
    """Function to flatten JSON dictionaries with unnecessary keys to a list of objects.

    Args:
        json_obj (Any): JSON object (typically a dictionary or list, but can also be a primitive).

    Returns:
        list: A list made from a flattened dictionary if json_obj was a dictionary, the original list if json_obj was a
        list, or the original value if json_obj was a primitive.

    """
    if isinstance(json_obj, dict):
        out = []
        for k, v in json_obj.items():
            out.append(v)
        return out
    else:
        return json_obj


def flatten_to_objects(json_obj: Any) -> Any:
    """Function to flatten a JSON dictionary (or a JSON dictionary in a list) to a dictionary of cast objects.

    Args:
        json_obj (Any): JSON object (typically a dictionary or list, but can also be a primitive).

    Returns:
        dict | list | int | float | str | bool: JSON dictionary/list/primitive with contents cast to Python objects.

    """
    if isinstance(json_obj, dict):
        return dict_to_list(json_obj)
    elif isinstance(json_obj, list):
        if isinstance(json_obj[0], dict):
            return dict_to_list(json_obj[0])
    else:
        return json_obj


def dict_to_list(json_dict: Dict[str, Any]) -> Any:
    """Function to convert a JSON dictionary to a list.

    Args:
        json_dict (dict[str, Any]): JSON dictionary.

    Returns:
        list: A list derived from a JSON dictionary, or the original dictionary if it does not contain dictionaries as
        values.

    """
    first_key = list(json_dict.keys())[0]
    if isinstance(json_dict.get(first_key), dict):
        first_val_key = list(json_dict.get(first_key).keys())[0]
        if first_key[:-1] == first_val_key:
            out = []
            for k, v in json_dict.items():
                out.append(v.get(first_val_key))
            return out
    return json_dict


def reorganize_json_dict(json_dict: Dict[str, Any], obj_key: str, val_to_key: str) -> Dict[str, Any]:
    """Function to reorganize a JSON dictionary of dictionaries.

    The reorganized JSON dictionary is an ordered dictionary sorted by a specific attribute of the value dictionaries.

    Args:
        json_dict (dict of str: Any): JSON dictionary.
        obj_key (str): Key to access the dictionaries contained in json_dict.
        val_to_key (str): Key used to sort the dictionaries contained in json_dict.

    Returns:
        dict[str, Any]: An ordered dictionary of dictionaries sorted by val_to_key.

    """
    out = {}
    for k, v in json_dict.items():
        out[str(getattr(v.get(obj_key), val_to_key))] = v.get(obj_key)

    return OrderedDict(
        (str(k), out[str(k)]) for k in sorted(
            [int(k_v) if isinstance(k_v, int) else k_v for k_v in out.keys()]))


def complex_json_handler(obj: Any) -> Any:
    """Custom handler to allow custom YFPY objects to be serialized into JSON.

    Args:
        obj (Any): Unserializable Python object to be serialized into JSON.

    Returns:
        Any: Serializable version of the Python object.

    """
    if hasattr(obj, "serialized"):
        return obj.serialized()
    else:
        try:
            return str(obj, "utf-8")
        except TypeError:
            raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


def reformat_json_list(json_obj: Any) -> Any:
    """Function to clean and reformat JSON lists to eliminate empty values and unnecessarily nested lists.

    Args:
        json_obj (Any): JSON object (typically a dictionary or list, but can also be a primitive) to be cleaned.

    Returns:
        Any: Reformatted JSON list derived from original JSON object.

    """
    if isinstance(json_obj[0], list):
        if len(json_obj) > 1:
            return reformat_json_list(
                [reformat_json_list(item) if isinstance(item, list) else item for item in json_obj])
        else:
            return reformat_json_list(json_obj[0])
    else:
        # create chain map that filters out empty lists/dicts but leaves objects where value = 0
        return ChainMap(*[value for value in json_obj if (value == 0 or value)])
