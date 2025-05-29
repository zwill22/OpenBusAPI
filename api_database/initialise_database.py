import os.path
import sqlite3

from tools import printer
from .operators_database_setup import setup_operator_database
from .stop_database_setup import setup_stop_database


def setup_database(
    path: str, reinitialise: bool = False, **kwargs
) -> sqlite3.Connection:
    """
    Sets up connection to the database, if it exists. Else the database
    is initialised and the connection created

    Args:
        path (str): The (relative) path to the database file.
        reinitialise (bool, optional): Whether to reinitialise the database regardless of whether it already exists. Defaults to False.

    Returns:
        sqlite3.Connection: Connection to the database
    """
    db_exists = os.path.isfile(path)

    conn = sqlite3.connect(path)

    if not db_exists or reinitialise:
        printer.print_config("Initialising database", path, newline=True)
        setup_operator_database(conn, **kwargs)
        setup_stop_database(conn, **kwargs)

    return conn


if __name__ == "__main__":
    connection = setup_database("example.db", reinitialise=True)
    connection.close()
