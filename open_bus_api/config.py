import os
import json
import jsonschema
import jsonschema_default
from dotenv import load_dotenv
from jsonschema.exceptions import ValidationError

from tools import version_str
from tools.printer import print_config

load_dotenv()


class APIKey:
    """
    Class to manage access to the Open Bus data API key.

    It searches for an environment variable with the name
    provided in the config, if it cannot find it, an
    error is thrown.
    """

    def __init__(self, env: str):
        _api_key = os.getenv(env)
        if not _api_key:
            raise EnvironmentError(
                "No API key found. Environment variable {env} not set!"
            )

        self._api_key_ = _api_key.strip()

        print_config("API key found in environment", env, newline=True)

    def get_key(self):
        """
        Returns a string containing the API key.
        """
        return "api_key=" + self._api_key_


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
    except ValidationError as e:
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
        self,
        config_file: str | Path | None = None,
        schema_file: str = "config.schema.json",
        schema_dir: str = "static",
        **kwargs,
    ):
        print_header()
        if not kwargs and config_file:
            options = load_json(config_file)
        else:
            options = kwargs

        self.line_length = 100

        schema_path = os.path.join(schema_dir, schema_file)
        schema = json_load(schema_path)
        validate_config(options, schema)

        self.name = options["name"]
        self.version = version_str()
        self.dev = options["dev"]
        print_config("API Name", self.name, newline=True)
        print_config("Version", self.version, newline=False)
        if self.dev:
            print_config("Mode", "Development")
        else:
            print_config("Mode", "Production")

        self.database_filepath = os.path.abspath(options["database_file"])
        print_config("Database file", self.database_filepath, newline=True)

        self.reinitialise = options["reinitialise"]
        if self.reinitialise:
            print("--> Database will be reinitialised")

        self.bus_data_url = options["bus_data_url"]
        print_config("Bus Data URL", self.bus_data_url, newline=False)
        api_key_env = options["api_key_env"]
        self.api_key = APIKey(api_key_env)

        # TODO Change database to data file when referring to an xml/json/csv file
        self.operator_database_filepath = os.path.abspath(
            options["operator_database_file"]
        )
        self.operator_database_url = options["operator_database_url"]
        self.operator_database_encoding = options["operator_database_encoding"]
        if os.path.exists(self.operator_database_filepath):
            print_config(
                "Operator Database Filepath",
                self.operator_database_filepath,
                newline=True,
            )
        else:
            print("\nOperator data file not found, will download it")
            print_config("Operator data file URL", self.operator_database_url)
            print_config(
                "Operator data file save path", self.operator_database_filepath
            )
        print_config("Operator data file encoding", self.operator_database_encoding)

        self.stop_database_filepath = os.path.abspath(options["stop_database_file"])
        self.stop_database_url = options["stop_database_url"]
        self.stop_database_encoding = options["stop_database_encoding"]
        if os.path.exists(self.stop_database_filepath):
            print_config(
                "Stop data filepath", self.stop_database_filepath, newline=True
            )
        else:
            print("\nStop data file not found, will download it")
            print_config("Stop data file URL", self.stop_database_url)
            print_config("Stop data file save path", self.stop_database_filepath)
        print_config("Stop data file encoding", self.stop_database_encoding)
