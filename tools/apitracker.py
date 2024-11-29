import json
import sys

import time
import requests

from tools.analyse_response import analyse_response

api_url = "https://fdo10eshm1.execute-api.eu-west-2.amazonaws.com/OpenBusLocationAPI/-3.00/-2.95/53.35/53.40"
token_url = "https://eu-west-2xqw1ltf7v.auth.eu-west-2.amazoncognito.com/oauth2/token"
client_id = "53bht8gs2qavgjnu9673bjft16"


def to_string(data: dict[str, str]) -> str:
    """
    Convert dictionary into a single string formatted as "&key=value".

    :param data: Data dictionary

    :return: Data string
    """
    output = ""
    first = True
    for k, v in data.items():
        if not first:
            output += "&"
        first = False

        output += "{0}={1}".format(k, v)

    return output


def request_token(secret: str) -> dict[str, str]:
    """
    Request a token from `token_url` using the `requests` module.

    :param secret: Client secret necessary to request a valid token.

    :return: A valid JSON token
    """
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": secret,
        "scope": "default-m2m-resource-server-tuzcmo/read"
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(token_url, data=to_string(data), headers=headers)

    content = response.json()

    if not response.ok:
        if content["error"] == "invalid_client":
            raise LookupError("Unable to authenticate token request")
        else:
            raise LookupError("Error occurred during token request")

    return content


def get_headers(access_token: str = None, token_type: str = None, **kwargs) -> dict[str, str]:
    """
    Create the headers dictionary for `requests.get`.

    :param access_token: API access token
    :param token_type: The type of token provided

    :return: Headers dictionary
    """
    return {"Authorization": "{0} {1}".format(token_type, access_token)}


def access_api(token: dict[str, str], verbose=True, **kwargs) -> str:
    """
    Call the API url `api_url` using `token` for authorisation and check for a valid response.

    :param token: Token in JSON format
    :param verbose: Whether to print details of response retrieval
    :param kwargs:
    :return: API response as a string
    """
    headers = get_headers(**token)
    print("Requesting response from api...", end='')
    t0 = time.time()
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print()
        if e.response.status_code == 401:
            print("Authorisation failed, has the token expired?", file=sys.stderr)
        raise SystemExit(e)
    except requests.exceptions.RequestException as e:
        print()
        raise SystemExit(e)

    t1 = time.time()
    print("Response retrieved, time: {:.2f}s\n".format(t1-t0))

    return response.content.decode()


def save_token(token: dict[str, str], filename):
    """
    Save a token to file `filename` in JSON format.

    :param token: Token in JSON (dictionary) format
    :param filename: Name of file to save token to.
    """
    with open(filename, 'w') as file:
        json.dump(token, file)


def load_token(filename: str) -> dict[str, str]:
    """
    Load a token in the form of a JSON object from file `filename`

    :param filename: Name of file containing JSON token

    :return: JSON token
    """
    with open(filename, 'r') as file:

        json_object = json.load(file)

    return json_object


def find_token(secret=None, token_file=None, **kwargs) -> dict[str, str]:
    """
    Find a token for API authorisation. If a secret is not provided, attempt to find a token in file `token_file`.
    If a `secret` is provided, check whether a token file is already present, if not use the secret to request a new
    token using `request_token` and save it as `token_file`.

    :param secret: Client secret needed to request a token.
    :param token_file: Name of file for loading/saving a token from/to.
    :param verbose: Whether to print details of search.

    :return: A token
    """
    if not secret:
        print("Searching for token file: {}".format(token_file))
        return load_token(token_file)

    try:
        print("Retrieving token file: {}".format(token_file))
        return load_token(token_file)
    except FileNotFoundError:
        print("File not found, requesting token...", end='')
        t0 = time.time()
        token = request_token(secret)
        t1 = time.time()
        print("Token retrieved, time: {}s".format(t1-t0))
        print("Saving token to file: {}".format(token_file))
        save_token(token, token_file)
        return token


def get_token(**kwargs) -> dict[str, str]:
    """
    Get a token to use to authorise the API using the function `find_token`.If the output is verbose, print details
    of the token.

    :param kwargs:
    :return: Token
    """
    token = find_token(**kwargs)

    verbose = kwargs.get("verbose", False)
    if verbose:
        print("Token retrieved")
        print("Token type: {}".format(token["token_type"]))

    return token


def save_xml(xml: str):
    with open("api_response.xml", 'w') as file:
        file.write(xml)


def main(**kwargs):
    token = get_token(**kwargs)

    api_response = access_api(token, **kwargs)
    analyse_response(api_response)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--secret", type=str, help="The client secret (for authorisation).")
    parser.add_argument("--token_file", type=str, help="File containing the JWT token", default="token.json")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")

    main(**vars(parser.parse_args()))
