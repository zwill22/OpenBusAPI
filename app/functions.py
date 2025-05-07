from flask import render_template, abort

from tools import get_location_url, api_output, get_base_url
from operators import setup_database, fetch_operators_data, operators_info

def reinitialise_database():
    print("Reinitialising database")
    setup_database(reinitialise=True)
    print("Database reinitialised complete")


def fetch_index():
    return render_template("index.html")

def fetch_api_output():
    try:
        return api_output()
    except LookupError as e:
        abort(int(str(e)))


def location_data(min_lat, min_long, max_lat, max_long):
    feed_url = get_location_url(min_lat, min_long, max_lat, max_long)

    return api_output(feed_url)


def vehicle_location_data(vehicle_id):
    feed_url = get_base_url()

    feed_url += "&vehicleRef=" + vehicle_id

    return api_output(feed_url)


def operators_data():
    conn = setup_database()
    try:
        return fetch_operators_data(conn)
    except FileNotFoundError:
        abort(404)


def operators_info_list():
    template_name = "operators_data.html"
    conn = setup_database()
    return render_template(template_name, columns=operators_info(conn))

