__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import json
from pathlib import Path, PosixPath
from typing import Union, List, Dict, Callable, Type

from yfpy.logger import get_logger
from yfpy.models import YahooFantasyObject
from yfpy.utils import complex_json_handler, unpack_data

logger = get_logger(__name__)


class Data(object):

    def __init__(self, data_dir: Union[Path, str], save_data: bool = False, dev_offline: bool = False):
        """Instantiate data object to retrieve, save, and load Yahoo fantasy football data.

        :param data_dir: directory path where data will be saved/loaded
        :param save_data: (optional) bool determining whether or not data is saved after retrieval from the Yahoo FF API
        :param dev_offline: (optional) bool for offline development (requires a prior online run with save_data = True
        """
        self.data_dir = data_dir if type(data_dir) == PosixPath else Path(data_dir)  # type: Path
        self.save_data = save_data  # type: bool
        self.dev_offline = dev_offline  # type: bool

    def update_data_dir(self, new_save_dir: Union[Path, str]) -> None:
        """Modify the data storage directory if it needs to be updated.

        :param new_save_dir: full path to new desired directory where data will be saved/loaded
        """
        self.data_dir = new_save_dir if type(new_save_dir) == PosixPath else Path(new_save_dir)  # type: Path

    @staticmethod
    def get(yf_query: Callable, params: Union[Dict[str, str], None] = None) -> Union[str, YahooFantasyObject,
                                                                                     List[YahooFantasyObject],
                                                                                     Dict[str, YahooFantasyObject]]:
        """Run query to retrieve Yahoo fantasy football data.

        :param yf_query: chosen yfpy query method to run
        :param params: (optional) dict of parameters to be passed to chosen yfpy query function
        :return: result of the yfpy query
        """
        if params:
            return yf_query(**params)
        else:
            return yf_query()

    def save(self, file_name: str, yf_query: Callable, params: Union[Dict[str, str], None] = None,
             new_data_dir: Union[Path, str, None] = None) -> Union[str, YahooFantasyObject, List[YahooFantasyObject],
                                                                   Dict[str, YahooFantasyObject]]:
        """Retrieve and save Yahoo fantasy football data locally.

        :param file_name: name of file to which data will be saved
        :param yf_query: chosen yfpy query method to run
        :param params: (optional) dict of parameters to be passed to chosen yfpy query function
        :param new_data_dir: (optional) full path to new desired directory to which data will be saved
        :return:
        """
        # change data save directory
        if new_data_dir:
            new_data_dir = new_data_dir if type(new_data_dir) == PosixPath else Path(new_data_dir)
            logger.debug(f"Data directory changed from {self.data_dir} to {new_data_dir}.")
            self.update_data_dir(new_data_dir)

        # create full directory path if any directories in it do not already exist
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)

        # run the actual yfpy query and retrieve the query results
        data = self.get(yf_query, params)

        # save the retrieved data locally
        saved_data_file_path = self.data_dir / (file_name + ".json")
        with open(saved_data_file_path, "w", encoding="utf-8") as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=2, default=complex_json_handler)
        logger.debug(f"Data saved locally to: {saved_data_file_path}")
        return data

    def load(self, file_name: str, data_type_class: Type[YahooFantasyObject] = None,
             new_data_dir: Union[Path, str, None] = None) -> Union[str, YahooFantasyObject, List[YahooFantasyObject],
                                                                   Dict[str, YahooFantasyObject]]:
        """Load Yahoo fantasy football data already stored locally (CANNOT BE RUN IF save METHOD HAS NEVER BEEN RUN).

        :param file_name: name of file from which data will be loaded
        :param data_type_class: (optional) yfpy models.py class for data casting
        :param new_data_dir: (optional) full path to new desired directory from which data will be loaded
        :return:
        """
        # change data load directory
        if new_data_dir:
            new_data_dir = new_data_dir if type(new_data_dir) == PosixPath else Path(new_data_dir)
            self.update_data_dir(new_data_dir)

        # load selected data file
        saved_data_file_path = self.data_dir / (file_name + ".json")
        if saved_data_file_path.exists():
            with open(saved_data_file_path, "r", encoding="utf-8") as data_file:
                unpacked = unpack_data(json.load(data_file), YahooFantasyObject)
                data = data_type_class(unpacked) if data_type_class else unpacked
            logger.debug(f"Data loaded locally from: {saved_data_file_path}")
        else:
            raise FileNotFoundError(f"File {saved_data_file_path} does not exist. Cannot load data locally without "
                                    f"having previously saved data.")
        return data

    def retrieve(self, file_name: str, yf_query: Callable, params: Union[Dict[str, str], None] = None,
                 data_type_class: Type[YahooFantasyObject] = None,
                 new_data_dir: Union[Path, str, None] = None) -> Union[str, YahooFantasyObject,
                                                                       List[YahooFantasyObject],
                                                                       Dict[str, YahooFantasyObject]]:
        """Fetch data from the web or load it locally (combination of the save and load methods).

        :param file_name: name of file to/from which data will be saved/loaded
        :param yf_query: chosen yfpy query method to run
        :param params: (optional) dict of parameters to be passed to chosen yfpy query function
        :param data_type_class: (optional) yfpy models.py class for data casting
        :param new_data_dir: (optional) full path to new desired directory to/from which data will be saved/loaded
        :return:
        """
        if self.dev_offline:
            return self.load(file_name, data_type_class, new_data_dir)
        else:
            if self.save_data:
                return self.save(file_name, yf_query, params, new_data_dir)
            else:
                return self.get(yf_query, params)
