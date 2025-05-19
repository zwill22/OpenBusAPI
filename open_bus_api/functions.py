import toml
from flask import render_template

from .config import Config
from tools import get_location_url, api_output, get_base_url
from api_database import setup_database, fetch_operators_data, operators_info, get_stops


def get_version() -> str:
    """
    Gets the version of Open-Bus API from its metadata.

    Returns: Version string
    """
    with open("pyproject.toml") as f:
        data = toml.load(f)

    return data["project"]["version"]


def database_setup(config: Config):
    """
    Wrapper for `setup_database`

    Args:
        config (Config): configuration object
    """
    setup_database(
        config.database_filepath,
        reinitialise=config.reinitialise,
        operator_url=config.operator_database_url,
        operator_encoding=config.operator_database_encoding,
        stop_file=config.stop_database_filepath,
        stop_url=config.stop_database_url,
        stop_encoding=config.stop_database_encoding,
    )

    config.print_footer()


def fetch_index() -> str:
    """
    Renders the index page

    Returns: The index page
    """
    return render_template("index.html")


def location_data(
    min_lat: float, min_long: float, max_lat: float, max_long: float, **kwargs
) -> bytes:
    """
    Fetches the locations data on vehicles in the provided area from the API

    Args:
        min_lat (float): Minimum latitude
        min_long (float): Minimum longitude
        max_lat (float): Maximum latitude
        max_long (float): Maximum longitude

    Returns: API response data in XML format
    """
    feed_url = get_location_url(min_lat, min_long, max_lat, max_long, **kwargs)

    return api_output(feed_url)


def vehicle_location_data(vehicle_id: str, **kwargs) -> bytes:
    """
    Fetches the locations data on vehicle with id `vehicle_id` from the API

    Args:
        vehicle_id (str): Vehicle ID for the API request

    Returns: API response data in XML format
    """
    feed_url = get_base_url(**kwargs)

    feed_url += "&vehicleRef=" + vehicle_id

    return api_output(feed_url)


def operators_data(path: str) -> str:
    """
    Fetches the operators database

    path (str): Path to the database

    Returns: The operators data in JSON format
    """
    conn = setup_database(path)
    return fetch_operators_data(conn)


def operators_info_list(path: str) -> str:
    """
    Returns a summary of the contents of the operators database

    path (str): Path to the database

    Returns: Page describing the contents of the operators database
    """
    template_name = "operator_data.html"
    conn = setup_database(path)
    return render_template(template_name, columns=operators_info(conn))


def fetch_stops_data(
    path, min_lat: float, min_long: float, max_lat: float, max_long: float
) -> str:
    """
    Fetches the stops data on vehicles in the provided area from the database

    Args:
        path (str): Path to the database
        min_lat (float): Minimum latitude
        min_long (float): Minimum longitude
        max_lat (float): Maximum latitude
        max_long (float): Maximum longitude

    Returns: Result of database query in JSON format
    """
    conn = setup_database(path)
    return get_stops(conn, min_lat, min_long, max_lat, max_long)
