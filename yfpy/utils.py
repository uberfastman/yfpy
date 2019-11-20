__author__ = "Wren J. R. (uberfastman)"
__email__ = "wrenjr@yahoo.com"

import logging
from collections import ChainMap, OrderedDict

import stringcase

logger = logging.getLogger(__name__)


# noinspection PyTypeChecker
def unpack_data(json_obj, parent_class=None):
    """Recursive utility to parse, clean, and assign custom data types to retrieved Yahoo fantasy sports data.

    :param json_obj: json object for parsing; can be dict, list, or primitive
    :param parent_class: parent class type used to extract custom subclass type options for casting
    :return: recursively returns json objects until data is completely parsed, cleaned, and typed (where applicable)
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
                return get_type({k: unpack_data(v, parent_class) for k, v in json_obj.items()}, parent_class,
                                subclasses)
            else:
                # assign/cast data type where applicable
                json_obj = get_type(
                    dict({k: unpack_data(v, parent_class) for k, v in json_obj.items() if k != "count"}),
                    parent_class, subclasses)

                # flatten dicts with keys "0", "1",..., "n" to a list of objects
                if "0" in json_obj.keys() and "1" in json_obj.keys():
                    json_obj = flatten_to_list(json_obj)
                return json_obj
        else:
            return json_obj


def get_type(json_obj_dict, parent_class, subclasses):
    """Cast json obj to custom subclass type extracted from parent class.

    :param json_obj_dict: json dictionary with strings of data type as keys and json objects as values
    :param parent_class: parent class from which to derive subclasses for casting
    :param subclasses: dictionary of subclasses with strings that match the json dict keys as keys and classes for
    casting as values
    :return: type-assigned/cast json object
    """
    for k, v in json_obj_dict.items():
        # check if key is in the provided subclasses dict, that the object isn't already cast
        if k in subclasses.keys() and isinstance(v, dict) and not isinstance(v, subclasses[k]):
            json_obj_dict[k] = subclasses[k](unpack_data(v, parent_class))
    return json_obj_dict


def flatten_json_dict_list(json_obj_dict_list, parent_class):
    """Recursive utility to flatten lists containing all disparate dicts with no overlapping keys.

    :param json_obj_dict_list: list of json dicts
    :param parent_class: parent class type used to extract custom subclass type options
    :return: returns a dict if list was flattened, else returns a cleaned list
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


def flatten_to_list(json_obj):
    """Utility to flatten json dictionaries with unnecessary keys to a list of objects.

    :param json_obj: json object (dict or list)
    :return: list made from flattened dictionary if json_obj was dictionary, else the original list if json_obj was list
    """
    if isinstance(json_obj, dict):
        out = []
        for k, v in json_obj.items():
            out.append(v)
        return out
    else:
        return json_obj


def flatten_to_objects(json_obj):
    """Utility to flatten a json dictionary to a dictionary of cast objects, or do the same to a json dict in a list.

    :param json_obj: json object (dict or list)
    :return: json dictionary/list with contents cast to objects.
    """
    if isinstance(json_obj, dict):
        return dict_to_list(json_obj)
    elif isinstance(json_obj, list):
        if isinstance(json_obj[0], dict):
            return dict_to_list(json_obj[0])
    else:
        return json_obj


def dict_to_list(json_dict):
    """Utility to convert a json dictionary to a list.

    :param json_dict: json dictionary
    :return: list derived from json dictionary, or the original dictionary if it does not contain dictionaries
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


def reorganize_json_dict(json_dict, obj_key, val_to_key):
    """Utility to reorganize a json dictionary of dictionaries into an ordered dictionary sorted by a specific
    attribute of the value dictionaries.

    :param json_dict: json dictionary of dictionaries
    :param obj_key: key to access the dictionaries contained in the json_dict
    :param val_to_key: key used to sort the dictionaries contained in the json_dict
    :return: ordered dictionary of dictionaries sorted by val_to_key
    """
    out = {}
    for k, v in json_dict.items():
        out[str(getattr(v.get(obj_key), val_to_key))] = v.get(obj_key)

    return OrderedDict(
        (str(k), out[str(k)]) for k in sorted(
            [int(k_v) if isinstance(k_v, int) else k_v for k_v in out.keys()]))


def complex_json_handler(obj):
    """Custom handler to allow custom yfpy objects to be serialized into json.

    :param obj: custom object to be serialized into json
    :return: serializable version of the custom object
    """
    if hasattr(obj, "serialized"):
        return obj.serialized()
    else:
        try:
            return str(obj, "utf-8")
        except TypeError:
            raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


def reformat_json_list(json_obj):
    """Utility to clean and reformat json lists to eliminate empty values and unnecessarily nested lists.

    :param json_obj: json object to be cleaned
    :return: reformatted list derived from original json object
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
