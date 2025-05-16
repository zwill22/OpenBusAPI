from open_bus_api.config import Config
from open_bus_api.functions import database_setup


def test_database_setup():
    config = Config(file="config.json")

    database_setup(
        config.database_filepath,
        reinitialise=True,
        url=config.operator_database_url,
        encoding=config.operator_database_encoding
    )
