import os
import pytest

from api_database.fetch_db_file import fetch_file


def test_fetch_stops_file(tmp_path):
    file = str(tmp_path / "stops.csv")
    url = "https://github.com/zwill22/OpenBusAPI/blob/0a7de1c9a67225ddac53cb5db4d45f0ac639bb95/tests/sample_stops.csv?raw=true"

    with pytest.raises(RuntimeError):
        fetch_file("fakeurl", file)
    fetch_file(url, file)

    assert os.path.isfile(file)
