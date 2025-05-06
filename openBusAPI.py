from flask import Flask, render_template
from flask_cors import CORS

from tools import apiOutput, getLocationURL, getBaseURL
from operators import setup_database, operators_data, operators_info

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route(
    "/location/area/<min_latitude>/<min_longitude>/<max_latitude>/<max_longitude>"
)
def getLocationData(min_latitude, min_longitude, max_latitude, max_longitude):
    feed_url = getLocationURL(min_latitude, min_longitude, max_latitude, max_longitude)

    return apiOutput(feed_url)


@app.route("/location/vehicle/<vehicle_id>")
def getVehicleLocationData(vehicle_id):
    feed_url = getBaseURL()

    feed_url += "&vehicleRef=" + vehicle_id

    return apiOutput(feed_url)

@app.route("/operators/data")
def getOperatorsData():
    conn = setup_database()
    return operators_data(conn)


@app.route("/operators/info/list")
def getOperatorsInfoList():
    conn = setup_database()
    return render_template("operator_data.html", columns=operators_info(conn))


if __name__ == "__main__":
    app.run(host="localhost", port=5134)
