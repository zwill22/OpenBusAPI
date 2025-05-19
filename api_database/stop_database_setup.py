import os
import gzip
import sqlite3
import requests

import polars as pl

def fetch_stops_file(url: str, file: str):
    response = requests.get(url, stream=True)
    with gzip.open(file, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)


def setup_stop_database(
    conn: sqlite3.Connection,
    stop_file: str = "Stops.csv.gz",
    stop_url: str = "https://naptan.api.dft.gov.uk/v1/access-nodes?dataFormat=csv",
    stop_encoding: str = "utf8",
    **kwargs,
):
    """
    Setups up the Stop database using the online version at `stop_url`.

    Args:
        conn (sqlite3.Connection): Connection to the database
        stop_url (str, optional): URL for the Stop data in CSV format. Defaults to "".
        stop_encoding (str, optional): Encoding of the CSV file. Defaults to "UTF-8".
    """

    drop_cols = [
        "CleardownCode",
        "CommonNameLang",
        "ShortCommonNameLang",
        "LandmarkLang",
        "StreetLang",
        "Crossing",
        "CrossingLang",
        "IndicatorLang",
        "GrandParentLocalityName",
        "TownLang",
        "SuburbLang",
        "Easting",
        "Northing",
        "DefaultWaitTime",
        "Notes",
        "NotesLang",
        "Status"
    ]
    if not os.path.isfile(stop_file):
        fetch_stops_file(stop_url, stop_file)

    data = (
        pl.scan_csv(stop_file, encoding=stop_encoding, infer_schema_length=None)
        .filter(pl.col("Status") == "active")
        .drop(*drop_cols)
    )

    data.collect().to_pandas().to_sql("Stops", conn, if_exists="replace", index=False)

    print("-- Stops database initialised")
