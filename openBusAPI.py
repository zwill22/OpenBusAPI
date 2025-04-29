from flask import Flask
from flask_cors import CORS
from tools.output import apiOutput

app = Flask(__name__)
CORS(app)


class APIKey:
    def __init__(self, api_file="api_key"):
        api_key = ""

        with open(api_file, "r") as f:
            api_key += f.read()

        self._api_key_ = api_key.strip()

    def getAPIKey(self):
        return "api_key=" + self._api_key_


api_key = APIKey()


@app.route("/")
def index():
    return "Index"


def apiKey():
    return api_key.getAPIKey()


def boundingBox(latitude: tuple[float, float], longitude: tuple[float, float]):
    """
    Convert longitude and latitude to a string formatted as:
    "boundingBox={longitude[0]},{latitude[0]},{longitude[1]},{latitude[1]}"
    This conforms to the open Bus services API specifications:
    Bounding Box:   Limit results to bus location data with vehicle position
                    within the rectangular bounding box you set using co-ordinates:
                    minLongitude, minLatitude, maxLongitude, maxLatitude.

    Args:
        latitude (tuple[float, float]): The minimum and maxium latitudes of the box
        longitude (tuple[float, float]): The minimum and maxium longitudes of the box


    """
    output_string = "&boundingBox="

    output_string += str(longitude[0]) + ","
    output_string += str(latitude[0]) + ","
    output_string += str(longitude[1]) + ","
    output_string += str(latitude[1])

    return output_string


def getBaseURL():
    feed_url = "https://data.bus-data.dft.gov.uk/api/v1/datafeed?"

    feed_url += apiKey()

    return feed_url


def getLocationURL(min_latitude, min_longitude, max_latitude, max_longitude):
    feed_url = getBaseURL()

    latitude = (float(min_latitude), float(max_latitude))
    longitude = (float(min_longitude), float(max_longitude))

    feed_url += boundingBox(latitude, longitude)

    return feed_url


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
