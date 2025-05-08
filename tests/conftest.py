import pytest
from tools.xml_tools import fetch_schema


@pytest.fixture
def schema():
    return fetch_schema()
