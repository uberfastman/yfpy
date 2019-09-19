__author__ = "Wren J. R. (uberfastman)"
__email__ = "wrenjr@yahoo.com"

import json
import logging
import os

from yffpy.models import YahooFantasyObject
from yffpy.utils import complex_json_handler, unpack_data

logger = logging.getLogger(__name__)


class Data(object):

    def __init__(self, data_dir, save_data=False, dev_offline=False):
        """Instantiate data object to retrieve, save, and load Yahoo fantasy football data.

        :param data_dir: directory path where data will be saved/loaded
        :param save_data: (optional) boolean determining whether or not data is saved after retrieval from the Yahoo FF API
        :param dev_offline: (optional) boolean for offline development (requires a prior online run with save_data = True
        """
        self.data_dir = data_dir
        self.save_data = save_data
        self.dev_offline = dev_offline

    def update_data_dir(self, new_save_dir):
        """Modify the data storage directory if it needs to be updated.

        :param new_save_dir: full path to new desired directory where data will be saved/loaded
        """
        self.data_dir = new_save_dir

    @staticmethod
    def get(yff_query, params=None):
        """Run query to retrieve Yahoo fantasy football data.

        :param yff_query: chosen yffpy query method to run
        :param params: (optional) dict of parameters to be passed to chosen yffpy query function
        :return: result of the yffpy query
        """
        if params:
            return yff_query(**params)
        else:
            return yff_query()

    def save(self, file_name, yff_query, params=None, new_data_dir=None):
        """Retrieve and save Yahoo fantasy football data locally.

        :param file_name: name of file to which data will be saved
        :param yff_query: chosen yffpy query method to run
        :param params: (optional) dict of parameters to be passed to chosen yffpy query function
        :param new_data_dir: (optional) full path to new desired directory to which data will be saved
        :return:
        """
        # change data save directory
        if new_data_dir:
            logger.debug("Data directory changed from {} to {}.".format(self.data_dir, new_data_dir))
            self.update_data_dir(new_data_dir)

        # create full directory path if any directories in it do not already exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # run the actual yffpy query and retrieve the query results
        data = self.get(yff_query, params)

        # save the retrieved data locally
        saved_data_file_path = os.path.join(self.data_dir, file_name + ".json")
        with open(saved_data_file_path, "w", encoding="utf-8") as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=2, default=complex_json_handler)
        logger.debug("Data saved locally to: {}".format(saved_data_file_path))
        return data

    def load(self, file_name, data_type_class=None, new_data_dir=None):
        """Load Yahoo fantasy football data already stored locally (CANNOT BE RUN IF save METHOD HAS NEVER BEEN RUN).

        :param file_name: name of file from which data will be loaded
        :param data_type_class: (optional) yffpy models.py class for data casting
        :param new_data_dir: (optional) full path to new desired directory from which data will be loaded
        :return:
        """
        # change data load directory
        if new_data_dir:
            self.update_data_dir(new_data_dir)

        # load selected data file
        saved_data_file_path = os.path.join(self.data_dir, file_name + ".json")
        if os.path.exists(saved_data_file_path):
            with open(saved_data_file_path, "r", encoding="utf-8") as data_file:
                unpacked = unpack_data(json.load(data_file), YahooFantasyObject)
                data = data_type_class(unpacked) if data_type_class else unpacked
            logger.debug("Data loaded locally from: {}".format(saved_data_file_path))
        else:
            raise FileNotFoundError(
                "FILE {} DOES NOT EXIST. CANNOT LOAD DATA LOCALLY WITHOUT HAVING PREVIOUSLY SAVED DATA!".format(
                    saved_data_file_path))
        return data

    def retrieve(self, file_name, yff_query, params=None, data_type_class=None, new_data_dir=None):
        """Fetch data from the web or load it locally (combination of the save and load methods).

        :param file_name: name of file to/from which data will be saved/loaded
        :param yff_query: chosen yffpy query method to run
        :param params: (optional) dict of parameters to be passed to chosen yffpy query function
        :param data_type_class: (optional) yffpy models.py class for data casting
        :param new_data_dir: (optional) full path to new desired directory to/from which data will be saved/loaded
        :return:
        """
        if self.dev_offline:
            return self.load(file_name, data_type_class, new_data_dir)
        else:
            if self.save_data:
                return self.save(file_name, yff_query, params, new_data_dir)
            else:
                return self.get(yff_query, params)
