# OpenBusAPI

[![Python][python-badge]][python]
[![GitHub][github-badge]][open-bus-api]
[![uv][uv-badge]][uv]
[![Polars][polars-badge]][polars]
[![Pytest][pytest-badge]][pytest]
[![Flask][flask-badge]][flask]
[![PythonAnywhere][python-anywhere-badge]][python-anywhere]
[![GitHub Actions][github-actions-badge]][github-actions]
[![CI Build][ci-badge]][ci-build]
[![Codecov][codecov-badge]][codecov]
[![Coverage][coverage-badge]][coverage]
[![Read the Docs][rtd-badge]][rtd]
[![Documentation Status][docs-badge]][docs]
[![Buy Me A Coffee][buy-me-a-coffee-badge]][buy-me-a-coffee]
[![License: MIT][license-badge]][license]
[![No AI][noai-badge]](#)

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

## Dependencies

- [Flask API](https://flask.palletsprojects.com/en/stable/) - API framework
- [Pandas](https://pandas.pydata.org) - Converting XML data to SQL
- [Polars](https://pola.rs) - Querying databases
- [BNG-latlon](https://github.com/fmalina/blocl-bnglatlon) - Converting British National Grid coordinates to Latitude and longitude
- [xmlschema](https://xmlschema.readthedocs.io/en/latest/index.html) - Verifying XML data
- [jsonschema](https://github.com/python-jsonschema/jsonschema) - Verifying JSON data
- [jsonschema-default](https://github.com/mnboos/jsonschema-default) - For creating a default object from a JSON schema
- [toml](https://github.com/uiri/toml) - For parsing TOML files

<!-- Badges -->

[python-badge]: https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge
[github-badge]: https://img.shields.io/badge/GitHub-%23121011.svg?logo=github&logoColor=white&style=for-the-badge
[license-badge]: https://img.shields.io/github/license/zwill22/openbusapi?style=for-the-badge
[ci-badge]: https://img.shields.io/github/actions/workflow/status/zwill22/openbusapi/ci.yml?style=for-the-badge&logo=github
[coverage-badge]: https://img.shields.io/codecov/c/github/zwill22/openbusapi?style=for-the-badge&logo=codecov
[rtd-badge]: https://img.shields.io/badge/Read%20the%20Docs-8CA1AF?logo=readthedocs&logoColor=fff&labelColor=333&style=for-the-badge
[docs-badge]: https://img.shields.io/readthedocs/openbusapi?style=for-the-badge&logo=rtd
[buy-me-a-coffee-badge]: https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?&logo=buy-me-a-coffee&logoColor=black&style=for-the-badge
[noai-badge]: https://custom-icon-badges.demolab.com/badge/No%20AI-2f2f2f?logo=non-ai&logoColor=white&style=for-the-badge
[github-actions-badge]: https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white&style=for-the-badge
[codecov-badge]: https://img.shields.io/badge/Codecov-F01F7A?logo=codecov&logoColor=fff&style=for-the-badge
[flask-badge]: https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff&style=for-the-badge
[uv-badge]: https://img.shields.io/badge/uv-%23DE5FE9.svg?style=for-the-badge&logo=uv&logoColor=white
[python-anywhere-badge]: https://img.shields.io/badge/pythonanywhere-%232F9FD7.svg?style=for-the-badge&logo=pythonanywhere&logoColor=151515
[polars-badge]: https://img.shields.io/badge/polars-0075ff?style=for-the-badge&logo=polars&logoColor=white
[pytest-badge]: https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3

<!-- Links -->

[python]: https://www.python.org
[open-bus-api]: https://github.com/zwill22/OpenBusAPI
[license]: https://github.com/zwill22/OpenBusAPI/blob/main/LICENSE
[ci-build]: https://github.com/zwill22/OpenBusAPI/actions/workflows/ci.yml
[coverage]: https://codecov.io/gh/zwill22/OpenBusAPI
[rtd]: https://openbusapi.readthedocs.io/en/latest
[docs]: https://openbusapi.readthedocs.io/en/latest
[buy-me-a-coffee]: https://coff.ee/zmwill
[codecov]: https://about.codecov.io/
[flask]: https://flask.palletsprojects.com/en/stable/
[uv]: https://docs.astral.sh/uv/
[python-anywhere]: https://www.pythonanywhere.com/
[github-actions]: https://github.com/zwill22/OpenBusAPI/actions
[polars]: https://pola.rs
[pytest]: https://docs.pytest.org/
