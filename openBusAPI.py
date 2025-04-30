from flask import Flask
from flask_cors import CORS
from tools.output import apiOutput
from tools.location_tools import getLocationURL, getBaseURL

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Index"


@app.route(
    "/location/area/<min_latitude>/<min_longitude>/<max_latitude>/<max_longitude>"
)
def getLocationData(min_latitude, min_longitude, max_latitude, max_longitude):
    feed_url = getLocationURL(min_latitude, min_longitude, max_latitude, max_longitude)
    print(feed_url)

    return apiOutput(feed_url)


@app.route("/location/vehicle/<vehicle_id>")
def getVehicleLocationData(vehicle_id):
    feed_url = getBaseURL()

    feed_url += "&vehicleRef=" + vehicle_id

    return apiOutput(feed_url)


if __name__ == "__main__":
    app.run()
