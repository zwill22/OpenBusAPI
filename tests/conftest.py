import pytest
from .analyse_xml import fetch_schema


@pytest.fixture(scope="session")
def schema():
    return fetch_schema()
