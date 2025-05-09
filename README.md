# OpenBusAPI

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](https://www.python.org)
[![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?logo=github&logoColor=white)](https://github.com/zwill22/OpenBusAPI)
[![License: MIT](https://img.shields.io/github/license/zwill22/iosbuild)](https://github.com/zwill22/OpenBusAPI/blob/main/LICENSE)
[![CI Build](https://github.com/zwill22/OpenBusAPI/actions/workflows/ci.yml/badge.svg)](https://github.com/zwill22/OpenBusAPI/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/zwill22/OpenBusAPI/graph/badge.svg)](https://codecov.io/gh/zwill22/OpenBusAPI)
[![Read the Docs](https://img.shields.io/badge/Read%20the%20Docs-8CA1AF?logo=readthedocs&logoColor=fff&labelColor=333)](https://openbusapi.readthedocs.io/en/latest)
[![Documentation Status](https://readthedocs.org/projects/openbusapi/badge/?version=latest)](https://openbusapi.readthedocs.io/en/latest/?badge=latest)

OpenBusAPI is the backend interface for the 
[BusTracker App](https://github.com/zwill22/BusTracker).
It provides a gateway API to access transport location data
from the [Bus Open Data Service](https://data.bus-data.dft.gov.uk) API.
The API also provides an endpoint to download data on transport operators taken from the
[NOC Database](https://www.travelinedata.org.uk/traveline-open-data/transport-operations/about-2/).

## Hosting the API

Hosting the API requires a key for the backend location API, which can be obtained above.
The code searches for an environment variable `OPEN_BUS_API_KEY` or a plain text file `api_key`
in the parent directory.

The API uses the [Flask framework](https://flask.palletsprojects.com/en/stable/),
in order to run the interface, I recommend the fantastic
[uv package manager](https://docs.astral.sh/uv),
which can be used to run the API directly with:
```shell
uv run open_bus_api
```

