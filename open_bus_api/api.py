from flask import Flask
from flask_cors import CORS

from open_bus_api.config import Config

from open_bus_api.functions import (
    fetch_index,
    location_data,
    vehicle_location_data,
    operators_data,
    operators_info_list,
    database_setup,
)

config = Config(args=None)

app = Flask(config.name)
CORS(app)

# Reinitialise database on startup
database_setup(config)


@app.route("/")
def index():
    """
    Open bus API Index page

    Returns: Index page
    """
    return fetch_index()


@app.route("/location/area/<min_lat>/<min_long>/<max_lat>/<max_long>")
def get_location_data(min_lat, min_long, max_lat, max_long):
    """
    Get location data from the Open Bus Database for vehicles in the range of
    latitude and longitude provided.

    Args:
        min_lat (float): Minimum latitude
        min_long (float): Minimum longitude
        max_lat (float): Maximum latitude
        max_long (float): Maximum longitude

    Returns: Location data in XML format
    """
    return location_data(
        min_lat,
        min_long,
        max_lat,
        max_long,
        bus_data_url=config.bus_data_url,
        api_key=config.api_key,
    )


@app.route("/location/vehicle/<vehicle_id>")
def get_vehicle_location_data(vehicle_id):
    """
    Get location data from the Open Bus Database for the vehicle with the id `vehicle_id`.

    Args:
        vehicle_id (str): Vehicle ID

    Returns: Vehicle location data in XML format

    """
    return vehicle_location_data(
        vehicle_id, bus_data_url=config.bus_data_url, api_key=config.api_key
    )


@app.route("/operators/data")
def get_operators_data():
    """
    Fetch the operators database in JSON format

    Returns: Operators data in JSON format
    """
    return operators_data(config.database_filepath)


@app.route("/operators/info/list")
def get_operators_info_list():
    """
    Info page contining details on the fields available
    in the operators database

    Returns: Operators information page
    """
    return operators_info_list(config.database_filepath)


if __name__ == "__main__":
    app.run(host="localhost", port=5134)
