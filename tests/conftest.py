import pytest
from tools.xml_tools import fetch_schema


@pytest.fixture(scope="session")
def schema():
    return fetch_schema()
