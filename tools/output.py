import requests


def api_output(feed_url: str) -> bytes:
    """
    Returns the content of a URL

    Args:
        feed_url: Lookup URL

    Returns: Content of URL in bytes
    """
    try:
        r = requests.get(feed_url)
    except requests.exceptions.ConnectionError:
        raise LookupError(503)

    if r.status_code != 200:
        raise LookupError(r.status_code)

    return r.content
