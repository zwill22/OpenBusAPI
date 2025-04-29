import requests


def apiOutput(feed_url: str):
    try:
        r = requests.get(feed_url)
    except requests.exceptions.ConnectionError:
        print("Connection error!")
        return

    if r.status_code != 200:
        print("Request returned an invalid exit code: {}".format(r.status_code))

    return r.content
