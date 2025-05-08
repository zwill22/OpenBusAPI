from flask import render_template

from tools import get_location_url, api_output, get_base_url
from operators import setup_database, fetch_operators_data, operators_info


def reinitialise_database():
    print("Reinitialising database")
    setup_database(reinitialise=True)
    print("Database reinitialised complete")


def fetch_index():
    return render_template("index.html")


def location_data(min_lat, min_long, max_lat, max_long):
    feed_url = get_location_url(min_lat, min_long, max_lat, max_long)

    return api_output(feed_url)


def vehicle_location_data(vehicle_id):
    feed_url = get_base_url()

    feed_url += "&vehicleRef=" + vehicle_id

    return api_output(feed_url)


def operators_data():
    conn = setup_database()
    return fetch_operators_data(conn)


def operators_info_list():
    template_name = "operator_data.html"
    conn = setup_database()
    return render_template(template_name, columns=operators_info(conn))
