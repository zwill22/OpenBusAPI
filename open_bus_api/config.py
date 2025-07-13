import os
import json
import jsonschema
import jsonschema_default
import argparse

from tools import version_str
from tools.printer import print_config


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
            self.message = ("API Key found from environment", api_env)
        else:
            _api_key = ""
            with open(api_file, "r") as f:
                _api_key += f.read()
            self.message = ("API Key loaded from file", api_file)

        self._api_key_ = _api_key.strip()

    def get_key(self):
        """
        Returns a string containing the API key.
        """
        return "api_key=" + self._api_key_

    def print_message(self):
        """
        Print the message to the console explaining the
        API key.
        """
        print_config(*self.message, newline=True)


def parse_cmdline(args=None) -> argparse.Namespace:
    """
    Parse commandline arguments and return an argparse.Namespace

    Args:
        args (list, optional): Arguments to parse directly

    Returns: Argparse Namespace
    """
    parser = argparse.ArgumentParser(
        prog="OpenBusAPI",
        description="""
        Welcome to the OpenBusAPI which provides an interface to bus data for the
        BusTracker App.
        """,
        epilog="Diolch yn fawr iawn.",
    )

    parser.add_argument(
        "config", help="Filepath for config file", nargs="?", default="config.json"
    )

    return parser.parse_args(args=args)


def json_load(file: str) -> dict:
    """
    Read JSON file to dictionary

    Args:
        file (str): JSON file path

    Returns: JSON dictionary
    """
    data = None
    with open(file, "r") as f:
        data = json.load(f)

    return data


def load_json(file):
    """
    Load JSON file to dictionary or return empty dictionary
    if file does not exist.

    Args:
        file (str): JSON file path

    Returns: JSON dictionary
    """
    try:
        data = json_load(file)
        print_config("Config file", file)
    except FileNotFoundError:
        print_config("No config file", "Using default configuration")
        data = {}

    return data


def load_config_data(args):
    """
    Parse command line arguments for config file name and
    read the config file to dictionary
    Args:
        args (list, optional): Arguments to parse directly

    Returns: Config dictionary
    """
    try:
        options = parse_cmdline(args=args)
    except SystemExit:
        raise RuntimeError("Unable to parse command line options")

    file = os.path.abspath(options.config)

    return load_json(file)


def validate_config(input_data: dict, schema: dict):
    """
    Validate the configuration data against the schema. Fill the
    data with default values for missing fields.

    Args:
        input_data (dict): Input configuration data
        schema (dict): Configuration data schema
    """
    try:
        jsonschema.validate(instance=input_data, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        raise ValueError(e)

    jsonschema_default.fill_from(schema=schema, target=input_data)


def print_header():
    logo = ""
    with open("static/logo.txt", "r") as f:
        logo = f.read()
    print()
    print(logo)


def print_footer(char="=", n=100):
    print(char * n)


class Config:
    """
    Open Bus API configuration
    """

    def __init__(
        self, args=None, schema_file="config.schema.json", schema_dir="static", **kwargs
    ):
        print_header()
        if not kwargs:
            data = load_config_data(args)
        else:
            data = kwargs

        self.line_length = 100

        schema_path = os.path.join(schema_dir, schema_file)
        schema = json_load(schema_path)
        validate_config(data, schema)

        self.name = data["name"]
        self.version = version_str()
        print_config("API Name", self.name, newline=True)
        print_config("Version", self.version, newline=False)

        self.database_filepath = os.path.abspath(data["database_file"])
        print_config("Database file", self.database_filepath, newline=True)

        self.reinitialise = data["reinitialise"]
        if self.reinitialise:
            print("--> Database will be reinitialised")

        self.bus_data_url = data["bus_data_url"]
        print_config("Bus Data URL", self.bus_data_url, newline=False)
        api_key_env = data["api_key_env"]
        api_key_filepath = os.path.abspath(data["api_key_file"])
        self.api_key = APIKey(api_key_env, api_key_filepath)
        self.api_key.print_message()

        self.operator_database_url = data["operator_database_url"]
        self.operator_database_encoding = data["operator_database_encoding"]
        print_config("Operator Database URL", self.operator_database_url, newline=True)
        print_config("Operator Database encoding", self.operator_database_encoding)

        self.stop_database_filepath = os.path.abspath(data["stop_database_file"])
        self.stop_database_url = data["stop_database_url"]
        self.stop_database_encoding = data["stop_database_encoding"]
        if os.path.exists(self.stop_database_filepath):
            print_config(
                "Stop Database Filepath", self.stop_database_filepath, newline=True
            )
        else:
            print("\nStop database file not found, will create it")
            print_config("Stop database URL", self.stop_database_url)
            print_config("Stop database save filepath", self.stop_database_filepath)
        print_config("Stop database encoding", self.stop_database_encoding)
