from flask import Flask
from flask_cors import CORS

from functions import fetch_index, location_data, vehicle_location_data, operators_data, operators_info_list, reinitialise_database

app = Flask("OpenBusAPI")
CORS(app)

# Reinitialise database on startup
reinitialise_database()

@app.route("/")
def index():
    return fetch_index()

@app.route("/location/area/<min_lat>/<min_long>/<max_lat>/<max_long>")
def get_location_data(min_lat, min_long, max_lat, max_long):
    return location_data(min_lat, min_long, max_lat, max_long)


@app.route("/location/vehicle/<vehicle_id>")
def get_vehicle_location_data(vehicle_id):
    return vehicle_location_data(vehicle_id)

@app.route("/operators/data")
def get_operators_data():
    return operators_data()

@app.route("/operators/info/list")
def get_operators_info_list():
    return operators_info_list()

if __name__ == "__main__":
    app.run(host="localhost", port=5134)
