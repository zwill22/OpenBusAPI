from open_bus_api.config import Config
from open_bus_api.functions import database_setup


def test_database_setup():
    config = Config(file="config.json")

    database_setup(
        reinitialise=True,
        url=config.database_url,
        encoding=config.database_encoding,
        db=config.database_file,
    )
