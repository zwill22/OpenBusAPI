import os


class APIKey:
    def __init__(self, api_file="api_key"):
        _api_key = os.getenv("OPEN_BUS_API_KEY")
        if not _api_key:
            print("Loading Key from file...")
            _api_key = ""
            with open(api_file, "r") as f:
                _api_key += f.read()

        self._api_key_ = _api_key.strip()

    def get_key(self):
        return "api_key=" + self._api_key_


api_key = APIKey()


def get_api_key():
    global api_key
    return api_key.get_key()


def bounding_box(latitude: tuple[float, float], longitude: tuple[float, float]):
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


def get_base_url():
    feed_url = "https://data.bus-data.dft.gov.uk/api/v1/datafeed?"

    feed_url += get_api_key()

    return feed_url


def get_location_url(min_latitude, min_longitude, max_latitude, max_longitude):
    feed_url = get_base_url()

    latitude = (float(min_latitude), float(max_latitude))
    longitude = (float(min_longitude), float(max_longitude))

    feed_url += bounding_box(latitude, longitude)

    return feed_url
