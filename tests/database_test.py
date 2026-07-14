from open_bus_api.config import Config
from open_bus_api.functions import database_setup


def test_database_setup():
    config = Config()
    database_setup(config)
