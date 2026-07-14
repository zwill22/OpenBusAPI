import pytest
import requests

from tools.output import api_output


class ResponseStatus:
    def __init__(self, code: int):
        self.status_code = code


def get_mocker(url: str):
    if url == "connection":
        raise requests.exceptions.ConnectionError("Example error")

    return ResponseStatus(400)


def test_api_output():
    with pytest.raises(LookupError) as e:
        api_output("connection", get_fn=get_mocker)

    assert e.value.args[0] == 503

    with pytest.raises(LookupError) as e2:
        api_output("url", get_fn=get_mocker)

    assert e2.value.args[0] == 400
