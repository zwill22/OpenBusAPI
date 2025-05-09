from flask import render_template

from tools import get_location_url, api_output, get_base_url
from operators import setup_database, fetch_operators_data, operators_info


def reinitialise_database():
    """
    Reinitialises the database, regardless of whether it was previously created
    """
    print("Reinitialising database")
    setup_database(reinitialise=True)
    print("Database reinitialised complete")


def fetch_index():
    """
    Returns the index page
    """
    return render_template("index.html")


def location_data(min_lat, min_long, max_lat, max_long):
    """
    Fetches the locations data on vehicles in the provided area from the API

    Args:
        min_lat: Minimum latitude
        min_long: Minimum longitude
        max_lat: Maximum latitude
        max_long: Maximum longitude

    Returns: API response data in XML format
    """
    feed_url = get_location_url(min_lat, min_long, max_lat, max_long)

    return api_output(feed_url)


def vehicle_location_data(vehicle_id):
    """
    Fetches the locations data on vehicle with id `vehicle_id` from the API

    Args:
        vehicle_id: Vehicle ID for the API request

    Returns: API response data in XML format
    """
    feed_url = get_base_url()

    feed_url += "&vehicleRef=" + vehicle_id

    return api_output(feed_url)


def operators_data():
    """
    Fetches the operators database

    Returns: The operators data in JSON format
    """
    conn = setup_database()
    return fetch_operators_data(conn)


def operators_info_list():
    """
    Returns a summary of the contents of the operators database

    Returns: Page describing the contents of the operators database
    """
    template_name = "operator_data.html"
    conn = setup_database()
    return render_template(template_name, columns=operators_info(conn))
