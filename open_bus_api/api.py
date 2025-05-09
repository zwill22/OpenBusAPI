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

config = Config(file="config.json")

app = Flask(config.name)
CORS(app)

# Reinitialise database on startup
database_setup(
    reinitialise=config.reinitialise,
    url=config.database_url,
    encoding=config.database_encoding,
    db=config.database_file,
)


@app.route("/")
def index():
    return fetch_index()


@app.route("/location/area/<min_lat>/<min_long>/<max_lat>/<max_long>")
def get_location_data(min_lat, min_long, max_lat, max_long):
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
    return vehicle_location_data(
        vehicle_id, bus_data_url=config.bus_data_url, api_key=config.api_key
    )


@app.route("/operators/data")
def get_operators_data():
    return operators_data(db=config.database_file)


@app.route("/operators/info/list")
def get_operators_info_list():
    return operators_info_list(db=config.database_file)


if __name__ == "__main__":
    app.run(host="localhost", port=5134)
