import os.path
import sqlite3

import pandas as pd
from xml.etree import ElementTree
from tools import api_output, printer


def get_record(tree: ElementTree.Element) -> dict:
    """
    Gets the data from a record in the database

    Args:
        tree: A element in the element tree

    Returns: Dictionary of all data from the record
    """
    data = {}
    for branch in tree:
        data[branch.tag] = branch.text

    return data


def get_data(tree: ElementTree.Element) -> pd.DataFrame:
    """
    Converts the data tree element into a dataframe

    Args:
        tree: Element tree

    Returns: The data from the data tree as a dataframe
    """
    tag = tree.tag

    operators = []
    for record in tree.findall(tag + "Record"):
        record_data = get_record(record)
        operators.append(record_data)

    return pd.DataFrame(operators)


def setup_table(tree: ElementTree.Element, conn: sqlite3.Connection):
    """
    Sets up a table in the database

    Args:
        tree: Element tree containing the table data
        conn: Connection to the database
    """
    df = get_data(tree)
    df = df.dropna(how="all", axis=1)
    drop_columns = ["ChangeDate", "ChangeAgent", "ChangeComment"]
    df = df.drop(columns=[x for x in drop_columns if x in df.columns])
    df.to_sql(tree.tag, conn, if_exists="replace", index=False)


def initialise_db(conn: sqlite3.Connection, url: str, encoding: str):
    """
    Initialises the database by downloading the data from the specified url

    Args:
        conn: Connection to the database
        url: URL of the database
        encoding: Expeceted encoding of the data
    """
    output = api_output(url)
    root = ElementTree.fromstring(output.decode(encoding))

    for tree in root:
        setup_table(tree, conn)


def setup_operator_database(
        connection: sqlite3.Connection,
        operator_url="https://www.travelinedata.org.uk/noc/api/1.0/nocrecords.xml",
        operator_encoding="windows-1252",
        **kwargs
):
    """
    Sets up the operator part of the database at `connection` using the provided URL and encoding.

    Args:
        connection (sqlite3.Connection): Connection to the database
        operator_url (str, optional): URL for operator XML data. Defaults to "https://www.travelinedata.org.uk/noc/api/1.0/nocrecords.xml".
        operator_encoding (str, optional): Encoding for the XML file. Defaults to "windows-1252".
    """

    initialise_db(connection, operator_url, operator_encoding)
    print("-- Operator database initialised")


def setup_stop_database(
        connection: sqlite3.Connection,
        stop_url: str = "",
        stop_encoding: str = "UTF-8",
        **kwargs
):
    """
    Setups up the Stop database using the online version at `stop_url`.

    Args:
        connection (sqlite3.Connection): Connection to the database
        stop_url (str, optional): URL for the Stop data in CSV format. Defaults to "".
        stop_encoding (str, optional): Encoding of the CSV file. Defaults to "UTF-8".
    """
    pass


def setup_database(path: str, reinitialise: bool = False, **kwargs) -> sqlite3.Connection:
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
