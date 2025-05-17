import os
import json
import jsonschema
import jsonschema_default
import argparse

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
        print_config(*self.message, newline=True)


def get_bool(bool_string: str) -> bool:
    """
    Converts a boolean string into a boolean.

    Args:
        bool_string: "True" or "False".

    Returns: True or False.
    """
    print(bool_string)
    if bool_string.lower() == "true":
        return True
    elif bool_string.lower() == "false":
        return False
    else:
        raise ValueError("Invalid value: {}".format(bool_string))


def parse_cmdline(args=None) -> argparse.Namespace:
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


def json_load(file):
    data = None
    with open(file, "r") as f:
        data = json.load(f)

    return data


def load_json(file):
    try:
        data = json_load(file)
        print("Configuration Data loaded from", file)
    except FileNotFoundError:
        print("No configuration file found at", file)
        data = {}

    return data


def load_config_data(args):
    try:
        options = parse_cmdline(args=args)
    except SystemExit:
        raise RuntimeError("Unable to parse command line options")

    file = os.path.abspath(options.config)

    return load_json(file)


def validate_config(input_data: dict, schema: dict):
    try:
        jsonschema.validate(instance=input_data, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        raise ValueError(e)

    jsonschema_default.fill_from(schema=schema, target=input_data)


class Config:
    """
    Open Bus API configuration
    """

    def __init__(self, args=None, schema_file="open_bus_config.schema.json", **kwargs):
        print("\n" + "-" * 32 + "\n\tOpen Bus API\n" + "-" * 32 + "\n")
        if not kwargs:
            data = load_config_data(args)
        else:
            data = kwargs

        dir_path = os.path.dirname(os.path.realpath(__file__))
        schema_path = os.path.join(dir_path, schema_file)
        schema = json_load(schema_path)
        validate_config(data, schema)

        self.name = data["name"]
        print_config("API Name", self.name, newline=True)

        self.database_filepath = os.path.abspath(data["database_file"])
        print_config("Database file", self.database_filepath)

        self.reinitialise = data["reinitialise"]
        if self.reinitialise:
            print("--> Database will be reinitialised")

        self.bus_data_url = data["bus_data_url"]
        print_config("Bus Data URL", self.bus_data_url, newline=True)
        api_key_env = data["api_key_env"]
        api_key_filepath = os.path.abspath(data["api_key_file"])
        self.api_key = APIKey(api_key_env, api_key_filepath)
        self.api_key.print_message()

        self.operator_database_url = data["operator_database_url"]
        self.operator_database_encoding = data["operator_database_encoding"]
        print_config("Operator Database URL", self.operator_database_url, newline=True)
        print_config("Operator Database encoding", self.operator_database_encoding)

        print()
