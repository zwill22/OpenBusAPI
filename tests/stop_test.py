import json

import open_bus_api.config
from api_database import fetch_stops, setup_database

keys = [
    "ATCOCode",
    "NaptanCode",
    "PlateCode",
    "CommonName",
    "ShortCommonName",
    "Landmark",
    "Street",
    "Indicator",
    "Bearing",
    "NptgLocalityCode",
    "LocalityName",
    "ParentLocalityName",
    "Town",
    "Suburb",
    "LocalityCentre",
    "GridType",
    "Longitude",
    "Latitude",
    "StopType",
    "BusStopType",
    "TimingStatus",
    "AdministrativeAreaCode",
    "CreationDateTime",
    "ModificationDateTime",
    "RevisionNumber",
    "Modification",
]


def test_stop():
    config = open_bus_api.config.Config()
    conn = setup_database(config.database_filepath)

    data = fetch_stops.get_stops(conn, 53.0, -3.05, 53.05, -3.04)

    json_data = json.loads(data)

    for entry in json_data:
        for key in keys:
            assert key in entry


def test_stop_code():
    config = open_bus_api.config.Config()
    conn = setup_database(config.database_filepath)

    codes = ["wregpjd", "wregtmd", "wregtmt", "wregdat", "wregawg"]
    data = fetch_stops.get_stops_code(conn, codes)

    json_data = json.loads(data)

    for entry in json_data:
        for key in keys:
            assert key in entry
        assert entry["NaptanCode"] in codes
