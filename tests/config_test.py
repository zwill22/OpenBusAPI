import os
from pathlib import Path

import pytest

from open_bus_api.config import Config


def check_default_config(config: Config, reinitialisation_value: bool = False):
    assert config.bus_data_url == "https://data.bus-data.dft.gov.uk/api/v1/datafeed"
    assert config.name == "OpenBusAPI"
    assert config.api_key.get_key() == "api_key=FAKE_API_KEY"

    db_url = "https://www.travelinedata.org.uk/noc/api/1.0/nocrecords.xml"
    assert config.operator_database_url == db_url
    assert config.database_filepath == Path("open_bus_database.db").absolute()
    assert config.reinitialise == reinitialisation_value
    assert config.operator_database_encoding == "windows-1252"


def test_config():
    with pytest.raises(
        EnvironmentError,
        match="No API key found. Environment variable RIDICULOUS_ENVIRONMENT_VARIABLE_NAME_ not set!",
    ):
        Config(
            api_key_env="RIDICULOUS_ENVIRONMENT_VARIABLE_NAME_",
            api_key_file="non_existing_file",
        )

    os.environ["OPEN_BUS_API_KEY"] = "FAKE_API_KEY"

    config_path = Path("config.json").absolute()
    if not config_path.exists():
        config = Config()
        check_default_config(config)

    config = Config(config_file=Path("fake_config_file.json"))
    check_default_config(config)

    for reinitialisation_value in [True, False]:
        config = Config(reinitialise=reinitialisation_value)
        check_default_config(config, reinitialisation_value=reinitialisation_value)

    with pytest.raises(ValueError):
        Config(reinitialise="true")
    with pytest.raises(ValueError):
        Config(reinitialise="false")
