import requests


def api_output(feed_url: str) -> bytes:
    try:
        r = requests.get(feed_url)
    except requests.exceptions.ConnectionError:
        raise LookupError(503)

    if r.status_code != 200:
        raise LookupError(r.status_code)

    return r.content
