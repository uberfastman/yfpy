# -*- coding: utf-8 -*-
"""YFPY module for retrieving, saving, and loading all Yahoo Fantasy Sports data.

This module is designed to allow for easy data management, such that both retrieving and managing Yahoo Fantasy Sports
data can be done in one place without the need to manually run the queries and manage data saved to JSON files.

Example:
    The Data module can be used as follows::

        auth_directory = Path(__file__).parent / "auth"
        yahoo_query = YahooFantasySportsQuery(
            auth_directory,
            "<league_id>",
            game_id="<game_key>",
            game_code="<game_code>",
            offline=False,
            all_output_as_json=False,
            consumer_key=os.environ["YFPY_CONSUMER_KEY"],
            consumer_secret=os.environ["YFPY_CONSUMER_SECRET"],
            browser_callback=True
        )

        data_directory = Path(__file__).parent / "output"
        data = Data(data_dir)
        data.save("file_name", yahoo_query.get_all_yahoo_fantasy_game_keys)
        data.load("file_name")

Attributes:
    logger (Logger): Module level logger for usage and debugging.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import json
from pathlib import Path, PosixPath
from typing import Union, List, Dict, Callable, Type, Any

from yfpy.logger import get_logger
from yfpy.models import YahooFantasyObject
from yfpy.query import YahooFantasySportsQuery
from yfpy.utils import complex_json_handler, unpack_data

logger = get_logger(__name__)


class Data(object):
    """YFPY Data object for Yahoo Fantasy Sports data retrieval, saving, and loading data as JSON.
    """

    def __init__(self, data_dir: Union[Path, str], save_data: bool = False, dev_offline: bool = False):
        """Instantiate data object to retrieve, save, and load Yahoo Fantasy Sports data.

        Args:
            data_dir (Path | str): Directory path where data will be saved/loaded.
            save_data (bool, optional): Boolean determining whether data is saved after retrieval from the Yahoo FF API.
            dev_offline (bool, optional): Boolean for offline development (requires a prior online run with
                save_data = True).

        """
        self.data_dir = data_dir if type(data_dir) == PosixPath else Path(data_dir)  # type: Path
        self.save_data = save_data  # type: bool
        self.dev_offline = dev_offline  # type: bool

    def update_data_dir(self, new_save_dir: Union[Path, str]) -> None:
        """Modify the data storage directory if it needs to be updated.

        Args:
            new_save_dir (str | Path): Full path to new desired directory where data will be saved/loaded.

        Returns:
            None

        """
        self.data_dir = new_save_dir if type(new_save_dir) == PosixPath else Path(new_save_dir)  # type: Path

    @staticmethod
    def get(yf_query: Callable, params: Union[Dict[str, str], None] = None) -> Union[str, YahooFantasyObject,
                                                                                     List[YahooFantasyObject],
                                                                                     Dict[str, YahooFantasyObject]]:
        """Run query to retrieve Yahoo Fantasy Sports data.

        Args:
            yf_query (Callable of YahooFantasySportsQuery): Chosen yfpy query method to run.
            params (dict of str: str, optional): Dictionary of parameters to be passed to chosen yfpy query function.

        Returns:
            object: Data retrieved by the yfpy query.

        """
        if params:
            return yf_query(**params)
        else:
            return yf_query()

    def save(self, file_name: str, yf_query: Callable, params: Union[Dict[str, Any], None] = None,
             new_data_dir: Union[Path, str, None] = None) -> Union[str, YahooFantasyObject, List[YahooFantasyObject],
                                                                   Dict[str, YahooFantasyObject]]:
        """Retrieve and save Yahoo Fantasy Sports data locally.

        Args:
            file_name (str): Name of file to which data will be saved.
            yf_query (Callable of YahooFantasySportsQuery): Chosen yfpy query method to run.
            params (dict of str: str, optional): Dictionary of parameters to be passed to chosen yfpy query function.
            new_data_dir (str | Path, optional): Full path to new desired directory to which data will be saved.

        Returns:
            object: Data retrieved by the yfpy query.

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
        """Load Yahoo Fantasy Sports data already stored locally.

        Note:
            This method will fail if the `save` method has not been called previously.

        Args:
            file_name (str): Name of file from which data will be loaded.
            data_type_class (Type[YahooFantasyObject], optional): YFPY models.py class for data casting.
            new_data_dir (str | Path, optional): Full path to new desired directory from which data will be loaded.

        Returns:
            object: Data loaded from the selected JSON file.

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

        Args:
            file_name (str): Name of file to/from which data will be saved/loaded.
            yf_query (Callable of YahooFantasySportsQuery): Chosen yfpy query method to run.
            params (dict of str: str, optional): Dictionary of parameters to be passed to chosen yfpy query function.
            data_type_class (Type[YahooFantasyObject], optional): YFPY models.py class for data casting.
            new_data_dir (str | Path, optional): Full path to new desired directory to/from which data will be
                saved/loaded.

        Returns:
            object: Data retrieved by the yfpy query OR loaded from the selected JSON file.

        """
        if self.dev_offline:
            return self.load(file_name, data_type_class, new_data_dir)
        else:
            if self.save_data:
                return self.save(file_name, yf_query, params, new_data_dir)
            else:
                return self.get(yf_query, params)
