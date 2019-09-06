import json
import logging
import os

from yffpy.models import YahooFantasyObject
from yffpy.utils import complex_json_handler, unpack_data

logger = logging.getLogger(__name__)


class Data(object):

    def __init__(self, save_dir):
        self.save_dir = save_dir

    @staticmethod
    def get(yff_query, params=None):
        # run data query
        if params:
            query_output = yff_query(**params, run=True)
        else:
            query_output = yff_query(run=True)
        data = query_output.get("data")
        url = query_output.get("url")
        logger.info(
            "DATA FETCHED WITH QUERY URL: {}".format(url) + (" AND PARAMS: {}".format(params) if params else ""))
        return data

    def save(self, file_name, yff_query, params=None):

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        data = self.get(yff_query, params)

        saved_data_file_path = os.path.join(self.save_dir, file_name + ".json")
        with open(saved_data_file_path, "w", encoding="utf-8") as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=2, default=complex_json_handler)
        logger.info("DATA SAVED LOCALLY TO: {}".format(saved_data_file_path))
        return data

    def load(self, file_name, data_type_class=None):

        saved_data_file_path = os.path.join(self.save_dir, file_name + ".json")
        if os.path.exists(saved_data_file_path):
            with open(saved_data_file_path, "r", encoding="utf-8") as data_file:
                unpacked = unpack_data(json.load(data_file), YahooFantasyObject)
                data = data_type_class(unpacked) if data_type_class else unpacked
            logger.info("DATA LOADED LOCALLY FROM: {}".format(saved_data_file_path))
        else:
            raise FileNotFoundError(
                "FILE {} DOES NOT EXIST. CANNOT LOAD DATA LOCALLY WITHOUT HAVING PREVIOUSLY SAVED DATA!".format(
                    saved_data_file_path))
        return data

    # def persist_and_retrieve_data(self, yff_query, data_dir, data_file_name, data_type_class=None, params=None,
    #                               persist_data=False, refresh_data=True):
    #     data_persistence_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), data_dir)
    #
    #     if not os.path.exists(data_persistence_dir):
    #         os.makedirs(data_persistence_dir)
    #
    #     if refresh_data:
    #         # run data query
    #         if params:
    #             query_output = yff_query(**params, run=True)
    #         else:
    #             query_output = yff_query(run=True)
    #         data = query_output.get("data")
    #         url = query_output.get("url")
    #         logger.info(
    #             "DATA FETCHED WITH QUERY URL: {}".format(url) + (" AND PARAMS: {}".format(params) if params else ""))
    #     else:
    #         persisted_data_file_path = os.path.join(data_persistence_dir, data_file_name + ".json")
    #         if os.path.exists(persisted_data_file_path):
    #             with open(persisted_data_file_path, "r", encoding="utf-8") as data_file:
    #                 unpacked = unpack_data(json.load(data_file), YahooFantasyObject)
    #                 data = data_type_class(unpacked) if data_type_class else unpacked
    #             logger.info("DATA RETRIEVED LOCALLY: {}".format(persisted_data_file_path))
    #         else:
    #             raise FileNotFoundError(
    #                 "FILE {} DOES NOT EXIST. CANNOT RUN LOCALLY WITHOUT HAVING PREVIOUSLY PERSISTED DATA!".format(
    #                     persisted_data_file_path))
    #
    #     if persist_data and refresh_data:
    #         persisted_data_file_path = os.path.join(data_persistence_dir, data_file_name + ".json")
    #         with open(persisted_data_file_path, "w", encoding="utf-8") as persisted_data_file:
    #             json.dump(data, persisted_data_file, ensure_ascii=False, indent=2, default=complex_json_handler)
    #         logger.info("DATA PERSISTED LOCALLY: {}".format(persisted_data_file_path))
    #
    #     return data
