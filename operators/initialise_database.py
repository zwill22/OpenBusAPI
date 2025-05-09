import os.path
import sqlite3

import pandas as pd
from xml.etree import ElementTree
from tools import api_output


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


def setup_database(
    reinitialise=False,
    url="https://www.travelinedata.org.uk/noc/api/1.0/nocrecords.xml",
    encoding="windows-1252",
    db="operators.db",
) -> sqlite3.Connection:
    """
    Sets up a connection to the database, if it exists.
    Else the database is initialised and the connection created.

    Args:
        reinitialise: Whether to reinitialise the database regardless of whether it exists
        url: URL of the database
        encoding: Expeceted encoding of the data
        db: Database name

    Returns: Connection to the database
    """
    db_exists = False

    if os.path.isfile(db):
        db_exists = True

    conn = sqlite3.connect(db)

    if not db_exists or reinitialise:
        print("Initialising database: {}".format(db))
        initialise_db(conn, url, encoding)
        print("Database initialised")

    return conn


if __name__ == "__main__":
    connection = setup_database(reinitialise=True)
    connection.close()
