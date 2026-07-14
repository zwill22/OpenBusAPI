import gzip
import requests


def fetch_file(url: str, file: str):
    """
    Fetches stops data from url and writes it to compressed csv file.

    Args:
        url (str): url to fetch data from
        file (str): path of file to write to
    """
    try:
        response = requests.get(url, stream=True)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(e)

    with gzip.open(file, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
