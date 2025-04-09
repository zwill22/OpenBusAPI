import requests

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Index"


def apiKey():
    api_key = "api_key="
    with open("api_key", "r") as f:
        api_key += f.read()

    return api_key.strip()


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


def getLocationURL(min_latitude, min_longitude, max_latitude, max_longitude):
    feed_url = "https://data.bus-data.dft.gov.uk/api/v1/datafeed?"

    feed_url += apiKey()

    latitude = (float(min_latitude), float(max_latitude))
    longitude = (float(min_longitude), float(max_longitude))

    feed_url += boundingBox(latitude, longitude)

    return feed_url

def apiOutput(feed_url: str):
    try:
        r = requests.get(feed_url)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Unable to establish internet connection")
    
    if r.status_code != 200:
        raise RuntimeError("Unable to access output")
    
    return r.content


@app.route("/location/<min_latitude>/<min_longitude>/<max_latitude>/<max_longitude>")
def getLocationData(min_latitude, min_longitude, max_latitude, max_longitude):
    feed_url = getLocationURL(min_latitude, min_longitude, max_latitude, max_longitude)

    return apiOutput(feed_url)

