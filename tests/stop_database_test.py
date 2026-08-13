from io import StringIO
import os
from pathlib import Path
import sqlite3
import pytest
import polars as pl

from api_database.fetch_db_file import fetch_file
from api_database.fetch_stops import get_stops
from api_database.stop_database_setup import get_stop_data, setup_stop_database


def test_fetch_stops_file(tmp_path):
    file = tmp_path / "stops.csv"
    url = "https://github.com/zwill22/OpenBusAPI/blob/0a7de1c9a67225ddac53cb5db4d45f0ac639bb95/tests/sample_stops.csv?raw=true"

    with pytest.raises(RuntimeError):
        fetch_file("fakeurl", file)
    fetch_file(url, file)

    assert os.path.isfile(file)


def test_sample_stop_data():
    file = Path("static") / "sample_stops.csv"
    df = get_stop_data(file, "utf8")

    assert df.shape == (460, 26)

    with pytest.raises(KeyError):
        get_stop_data(file, "utf16")


def test_sample_stop_database(tmp_path):
    file = Path("static") / "sample_stops.csv"
    db = tmp_path / "stop.db"

    conn = sqlite3.Connection(db)

    setup_stop_database(conn, stop_file=file)

    stops = get_stops(conn, 50, -4, 60, 4)

    stop_df = pl.read_json(StringIO(stops))

    assert stop_df.shape == (460, 26)
