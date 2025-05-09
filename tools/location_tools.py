def bounding_box(latitude: tuple[float, float], longitude: tuple[float, float]) -> str:
    """
    Convert longitude and latitude to a string formatted as:
    "boundingBox={longitude[0]},{latitude[0]},{longitude[1]},{latitude[1]}"
    This conforms to the open Bus services API specifications:
    Bounding Box: Limit results to bus location data with vehicle position
    within the rectangular bounding box you set using co-ordinates:
    minLongitude, minLatitude, maxLongitude, maxLatitude.

    Args:
        latitude (tuple[float, float]): The minimum and maximum latitudes of the box
        longitude (tuple[float, float]): The minimum and maximum longitudes of the box

    """
    output_string = "&boundingBox="

    output_string += str(longitude[0]) + ","
    output_string += str(latitude[0]) + ","
    output_string += str(longitude[1]) + ","
    output_string += str(latitude[1])

    return output_string


def get_base_url(
    api_key=None,
    bus_data_url="https://data.bus-data.dft.gov.uk/api/v1/datafeed",
    **kwargs,
):
    """
    Gets the base URL of the Open Bus data API including the api key.

    Args:
        api_key (APIKey): The API key.
        bus_data_url (str): The base URL of the bus data API.

    Returns: Base URL for accessing the Open Bus data API using the API key.
    """
    if not api_key:
        raise ValueError("API key not provided")

    feed_url = bus_data_url + "?"

    feed_url += api_key.get_key()

    return feed_url


def get_location_url(
    min_latitude, min_longitude, max_latitude, max_longitude, **kwargs
):
    """
    Constructs the URL for accessing the location data from Open Bus data API.

    Args:
        min_latitude: Minimum latitude of the area
        min_longitude: Minimum longitude of the area
        max_latitude: Maximum latitude of the area
        max_longitude: Maximum longitude of the area

    Returns: URL for accessing the location data from Open Bus data API.
    """
    feed_url = get_base_url(**kwargs)

    latitude = (float(min_latitude), float(max_latitude))
    longitude = (float(min_longitude), float(max_longitude))

    feed_url += bounding_box(latitude, longitude)

    return feed_url
