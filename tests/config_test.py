import os

import pytest
from open_bus_api.config import Config


def check_default_config(config: Config, reinitialisation_value: bool = True):
    assert config.bus_data_url == "https://data.bus-data.dft.gov.uk/api/v1/datafeed"
    assert config.name == "OpenBusAPI"
    assert config.api_key.get_key() == "api_key=FAKE_API_KEY"

    db_url = "https://www.travelinedata.org.uk/noc/api/1.0/nocrecords.xml"
    assert config.database_url == db_url
    assert config.database_file == os.path.abspath("operators.db")
    assert config.reinitialise == reinitialisation_value
    assert config.database_encoding == "windows-1252"


def test_config():
    with pytest.raises(FileNotFoundError):
        Config(
            api_key_env="RIDICULOUS_ENVIRONMENT_VARIABLE_NAME_",
            api_key_file="non_existing_file",
        )

    os.environ["OPEN_BUS_API_KEY"] = "FAKE_API_KEY"

    config = Config()
    check_default_config(config)
    config = Config(file="fake_config_file.json")
    check_default_config(config)

    config = Config(reinitialise="true")
    check_default_config(config)
    config = Config(reinitialise="false")
    check_default_config(config, reinitialisation_value=False)

    with pytest.raises(ValueError):
        Config(reinitialise="")
