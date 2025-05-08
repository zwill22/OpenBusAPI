import pytest
import polars as pl
from bs4 import BeautifulSoup

from io import StringIO
from open_bus_api.api import app as open_bus_api
from tools.location_reader import analyse_response


def test_index():
    response = open_bus_api.test_client().get("/")
    assert response.status_code == 200

    template = []
    with open("templates/index.html") as index_file:
        template = index_file.readlines()

    index_output = response.data.splitlines()
    l = len(index_output)
    assert l == len(template)
    for i in range(l):
        template_line = template[i].strip()
        index_line = index_output[i].decode().strip()
        assert template_line == index_line


cases = [
    ("/operators", 404),
    ("/operators/info", 404),
    ("/location", 404),
    ("/location/area", 404),
    ("/location/area/0", 404),
    ("/location/area/0/0", 404),
    ("/location/area/0/0/1", 404),
    ("/location/area/0/0/1/1", 200),
    ("/location/area/0/0/1/1/2", 404),
    ("/location/area/a/b/c/d", 500),
    ("/location/area/0.0/0.0/1.0/1.0", 200),
    ("/location/area/-1.0/-1.0/0.0/0.0", 200),
    ("/location/area/1/1/0/0", 200),
    ("/location", 404),
    ("/location/vehicle", 404),
    ("/location/vehicle/0", 200),
]

empty_keys = (
    "Siri",
    "ServiceDelivery",
    "ResponseTimestamp",
    "ProducerRef",
    "VehicleMonitoringDelivery",
    "RequestMessageRef",
    "ValidUntil",
    "ShortestPossibleCycle",
)


@pytest.mark.parametrize("path, output", cases)
def test_area_data(path, output, schema):
    response = open_bus_api.test_client().get(path)
    assert response.status_code == output
    if output == 200:
        output = response.data.decode()
        result = analyse_response(output, schema=schema)
        for key, value in result.items():
            assert key in empty_keys
            assert value == 1


real_data = [
    ("/location/area/53.0/-3.1/53.1/-3", 200, 0),
    ("/location/vehicle/1701", 200, 1),
]


@pytest.mark.parametrize("path, output, n", real_data)
def test_real_area_data(path, output, n, schema):
    response = open_bus_api.test_client().get(path)
    assert response.status_code == output
    output = response.data.decode()
    result = analyse_response(output, schema=schema)
    for key, value in result.items():
        if key in empty_keys:
            assert value == 1
        elif n == 0:
            assert value > 0
        else:
            assert value == n


expected_columns = (
    "NOCCODE",
    "OperatorPublicName",
    "PubNmId",
    "Mode",
    "TTRteEnq",
    "FareEnq",
    "ComplEnq",
    "Twitter",
    "Website",
)

transport_modes = (
    "Bus",
    "Ferry",
    "Section 19",
    "Underground",
    "Tram",
    "CT Operator",
    "Coach",
    "Partly DRT",
    "DRT",
    "Metro",
    "Airline",
    "Other",
    "Permit",
    "Cable Car",
    "Taxi",
    "Rail",
)


def test_operator_data():
    response = open_bus_api.test_client().get("/operators/data")
    assert response.status_code == 200
    output = response.data.decode()

    output_df = pl.read_json(StringIO(output))

    shape = output_df.shape
    assert shape[1] == 9
    n = shape[0]

    for column in output_df.columns:
        assert column in expected_columns

    for mode in output_df.get_column("Mode").unique():
        if mode is not None:
            assert mode in transport_modes

    assert len(output_df.get_column("NOCCODE").unique()) == n


def test_operator_info():
    response = open_bus_api.test_client().get("/operators/info/list")
    assert response.status_code == 200
    output = response.data.decode()
    soup = BeautifulSoup(output, features="html.parser")

    for item in soup.find("li"):
        assert item.text in expected_columns
