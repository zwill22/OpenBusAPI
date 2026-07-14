import os
import sqlite3
import polars as pl

from bng_latlon import OSGB36toWGS84 as convert_bng_to_latlon

from api_database.fetch_db_file import fetch_file


def convert_bng(easting, northing) -> tuple[float, float]:
    """
    Converts the BNG format to Longitude/Latitude

    Args:
        easting (int): Easting
        northing (int): Northing

    Returns: Longitude and Latitude as a pair

    """
    return convert_bng_to_latlon(easting, northing)


def get_stop_data(stop_file: str, stop_encoding: str) -> pl.DataFrame:
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
        "Status",
        "Lat",
        "Long",
    ]

    if stop_encoding != "utf8":
        raise KeyError("Invalid encoding for CSV")

    data = (
        pl.scan_csv(stop_file, infer_schema_length=None)
        .filter(pl.col("Status") == "active")
        .with_columns(
            pl.col("Easting").cast(pl.String).str.strip_chars().cast(pl.Int64)
        )
        .with_columns(
            pl.col("Northing").cast(pl.String).str.strip_chars().cast(pl.Int64)
        )
        .with_columns(
            pl.struct("Easting", "Northing")
            .map_elements(
                lambda x: convert_bng(x["Easting"], x["Northing"]),
                return_dtype=pl.List(pl.Float64),
            )
            .alias("LongLat")
        )
        .with_columns(pl.col("LongLat").list.to_struct(fields=["Long", "Lat"]))
        .unnest("LongLat")
        .with_columns(pl.col("Longitude").fill_null(pl.col("Long")))
        .with_columns(pl.col("Latitude").fill_null(pl.col("Lat")))
        .drop(*drop_cols)
    )

    return data.collect()


def setup_stop_database(
    conn: sqlite3.Connection,
    stop_file: str = "Stops.csv.gz",
    stop_url: str = "https://naptan.api.dft.gov.uk/v1/access-nodes?dataFormat=csv",
    stop_encoding: str = "utf8",
    **kwargs,
):
    """
    Setups up the Stop database using the local file `stop_file`, if it exists.
    Else the online version at `stop_url` is downloaded and saved to `stop_file`.
    The `stop_file` file can be either a CSV file or a GZIP file containing the CSV data.

    Args:
        conn (sqlite3.Connection): Connection to the database
        stop_file (str, optional): Path to the stops file. Defaults to "Stops.csv.gz".
        stop_url (str, optional): URL for the Stop data in CSV format. Defaults to "".
        stop_encoding (str, optional): Encoding of the CSV file. Defaults to "UTF-8".
    """

    if not os.path.isfile(stop_file):
        fetch_file(stop_url, stop_file)

    data = get_stop_data(stop_file, stop_encoding, **kwargs)

    data.to_pandas().to_sql("Stops", conn, if_exists="replace", index=False)

    print("-- Stops database initialised")
