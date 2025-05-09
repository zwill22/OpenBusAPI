import os
import json


class APIKey:
    """
    Class to manage access to the Open Bus data API key.
    First it searches for a key in the system environment.
    Second it searches for a key in an `api_file`. If no
    key is found, an error occurs.
    """

    def __init__(self, api_env, api_file):
        _api_key = os.getenv(api_env)
        if _api_key:
            self.message = "API Key found from environment: {}".format(api_env)
        else:
            _api_key = ""
            with open(api_file, "r") as f:
                _api_key += f.read()
            self.message = "API Key loaded from file: {}".format(api_file)

        self._api_key_ = _api_key.strip()

    def get_key(self):
        """
        Returns a string containing the API key.
        """
        return "api_key=" + self._api_key_


class Config:
    """
    Open Bus API configuration
    """

    def __init__(self, file=None, **kwargs):
        if file:
            data = None
            try:
                with open(file, "r") as f:
                    data = json.load(f)
                print("Data loaded from", file)
            except FileNotFoundError:
                print("No configuration file found at", file)
                data = {}
        else:
            data = kwargs

        self.name = data.get("name", "OpenBusAPI")
        api_key_env = data.get("api_key_env", "OPEN_BUS_API_KEY")
        api_key_file = os.path.abspath(data.get("api_key_file", "api_key"))

        self.api_key = APIKey(api_key_env, api_key_file)

        self.database_url = data.get(
            "url", "https://www.travelinedata.org.uk/noc/api/1.0/nocrecords.xml"
        )
        self.database_encoding = data.get("encoding", "windows-1252")
        self.database_file = os.path.abspath(data.get("file", "operators.db"))
        self.reinitialise = bool(data.get("reinitialise", True))

        self.bus_data_url = data.get(
            "bus_data_url", "https://data.bus-data.dft.gov.uk/api/v1/datafeed"
        )

        print("Open Bus API configuration")
        print("Name: {}".format(self.name))
        print(self.api_key.message)
        print("Operator Database URL: {}".format(self.database_url))
        print("Operator Database encoding: {}".format(self.database_encoding))
        print("Operator Database file: {}".format(self.database_file))
        if self.reinitialise:
            print("Database will be reinitialised")
        print("Bus Data URL: {}".format(self.bus_data_url))
