import requests


def get_request(url: str):
    return requests.get(url)


def api_output(feed_url: str, get_fn=get_request) -> bytes:
    """
    Returns the content of a URL

    Args:
        feed_url (str): Lookup URL

    Returns: Content of URL in bytes
    """
    try:
        r = get_fn(feed_url)
    except requests.exceptions.ConnectionError:
        raise LookupError(503)

    if r.status_code != 200:
        raise LookupError(r.status_code)

    return r.content
