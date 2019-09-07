__author__ = "Wren J. R. (uberfastman)"
__email__ = "wrenjr@yahoo.com"

import json
import logging
import os

from yffpy.models import YahooFantasyObject
from yffpy.utils import complex_json_handler, unpack_data

logger = logging.getLogger(__name__)


class Data(object):
    """
    Retrieve, save, and load Yahoo fantasy football data
    """

    def __init__(self, data_dir, save_data=False, dev_offline=False):
        # data storage directory
        self.data_dir = data_dir
        self.save_data = save_data
        self.dev_offline = dev_offline

    def update_data_dir(self, new_save_dir):
        # modify data storage directory
        self.data_dir = new_save_dir

    @staticmethod
    def get(yff_query, params=None):
        # run query to retrieve Yahoo fantasy football data
        if params:
            query_output = yff_query(**params)
        else:
            query_output = yff_query()
        data = query_output.get("data")
        url = query_output.get("url")
        logger.debug(
            "DATA FETCHED WITH QUERY URL: {}".format(url) + (" AND PARAMS: {}".format(params) if params else ""))
        return data

    def save(self, file_name, yff_query, params=None, new_data_dir=None):
        # retrieve and save locally Yahoo fantasy football data
        if new_data_dir:
            self.update_data_dir(new_data_dir)

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        data = self.get(yff_query, params)

        saved_data_file_path = os.path.join(self.data_dir, file_name + ".json")
        with open(saved_data_file_path, "w", encoding="utf-8") as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=2, default=complex_json_handler)
        logger.debug("DATA SAVED LOCALLY TO: {}".format(saved_data_file_path))
        return data

    def load(self, file_name, data_type_class=None, new_data_dir=None):
        # load Yahoo fantasy football data already stored locally (CANNOT BE RUN IF SAVE HAS NEVER BEEN RUN)
        if new_data_dir:
            self.update_data_dir(new_data_dir)

        saved_data_file_path = os.path.join(self.data_dir, file_name + ".json")
        if os.path.exists(saved_data_file_path):
            with open(saved_data_file_path, "r", encoding="utf-8") as data_file:
                unpacked = unpack_data(json.load(data_file), YahooFantasyObject)
                data = data_type_class(unpacked) if data_type_class else unpacked
            logger.debug("DATA LOADED LOCALLY FROM: {}".format(saved_data_file_path))
        else:
            raise FileNotFoundError(
                "FILE {} DOES NOT EXIST. CANNOT LOAD DATA LOCALLY WITHOUT HAVING PREVIOUSLY SAVED DATA!".format(
                    saved_data_file_path))
        return data

    def retrieve(self, file_name, yff_query, params=None, data_type_class=None, new_data_dir=None):
        # fetch data from the web or load it locally depending on the configurations set for save_data and dev_offline
        if self.dev_offline:
            return self.load(file_name, data_type_class, new_data_dir)
        else:
            if self.save_data:
                return self.save(file_name, yff_query, params, new_data_dir)
            else:
                return self.get(yff_query, params)
