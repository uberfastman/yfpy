import json
import logging
import os
from collections import ChainMap

import stringcase

from yffpy.dao import YahooFantasyObject, complex_json_handler

logger = logging.getLogger(__name__)


# noinspection PyTypeChecker
def unpack_data(json_obj, parent_class=None):
    subclasses = {}
    if parent_class:
        subclasses = {stringcase.snakecase(cls.__name__): cls for cls in parent_class.__subclasses__()}

    if json_obj:
        if isinstance(json_obj, list):
            json_obj = [obj for obj in json_obj if obj]

            if len(json_obj) == 1:
                return unpack_data(json_obj[0], parent_class)
            else:
                if any(isinstance(obj, dict) for obj in json_obj):
                    return flatten_dict_list(json_obj, parent_class)

                return [unpack_data(obj, parent_class) for obj in json_obj if obj]

        elif isinstance(json_obj, dict):

            if "0" in json_obj.keys() and "1" not in json_obj.keys():
                if len(json_obj.keys()) == 1:
                    return unpack_data(json_obj.get("0"), parent_class)
                else:
                    if isinstance(json_obj.get("0"), dict):
                        json_obj.update(json_obj.get("0"))

            if "count" in json_obj.keys() and "position" in json_obj.keys():
                return get_type({k: unpack_data(v, parent_class) for k, v in json_obj.items()}, parent_class,
                                subclasses)
            else:
                return get_type(dict({k: unpack_data(v, parent_class) for k, v in json_obj.items() if k != "count"}),
                                parent_class, subclasses)
        else:
            return json_obj


def flatten_dict_list(json_obj_dict_list, parent_class):
    json_obj_dict_list = [obj for obj in json_obj_dict_list if obj]
    item_keys = []
    ndx = 0
    for item in json_obj_dict_list:
        if isinstance(item, list):
            flattened_item = flatten_dict_list(item, parent_class)
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
        return [unpack_data(obj, parent_class) for obj in json_obj_dict_list if obj]


def get_type(json_obj_dict, parent_class, subclasses):
    for k, v in json_obj_dict.items():
        if k in subclasses.keys() and isinstance(v, dict) and not isinstance(v, subclasses[k]):
            json_obj_dict[k] = subclasses[k](unpack_data(v, parent_class))
    return json_obj_dict


def reformat_json_list(json_obj):
    if isinstance(json_obj[0], list):
        if len(json_obj) > 1:
            return reformat_json_list(
                [reformat_json_list(item) if isinstance(item, list) else item for item in json_obj])
        else:
            return reformat_json_list(json_obj[0])
    else:
        return ChainMap(*[value for value in json_obj if value])


def persist_and_retrieve_data(yff_query, data_dir, data_file_name, data_type_class=None, params=None,
                              persist_data=False, refresh_data=True):
    data_persistence_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), data_dir)

    if not os.path.exists(data_persistence_dir):
        os.makedirs(data_persistence_dir)

    if refresh_data:
        # run data query
        if params:
            query_output = yff_query(**params, run=True)
        else:
            query_output = yff_query(run=True)
        data = query_output.get("data")
        url = query_output.get("url")
        logger.info(
            "DATA FETCHED WITH QUERY URL: {}".format(url) + (" AND PARAMS: {}".format(params) if params else ""))
    else:
        persisted_data_file_path = os.path.join(data_persistence_dir, data_file_name + ".json")
        if os.path.exists(persisted_data_file_path):
            with open(persisted_data_file_path, "r", encoding="utf-8") as data_file:
                unpacked = unpack_data(json.load(data_file), YahooFantasyObject)
                data = data_type_class(unpacked) if data_type_class else unpacked
            logger.info("DATA RETRIEVED LOCALLY: {}".format(persisted_data_file_path))
        else:
            raise FileNotFoundError(
                "FILE {} DOES NOT EXIST. CANNOT RUN LOCALLY WITHOUT HAVING PREVIOUSLY PERSISTED DATA!".format(
                    persisted_data_file_path))

    if persist_data and refresh_data:
        persisted_data_file_path = os.path.join(data_persistence_dir, data_file_name + ".json")
        with open(persisted_data_file_path, "w", encoding="utf-8") as persisted_data_file:
            json.dump(data, persisted_data_file, ensure_ascii=False, indent=2, default=complex_json_handler)
        logger.info("DATA PERSISTED LOCALLY: {}".format(persisted_data_file_path))

    return data
