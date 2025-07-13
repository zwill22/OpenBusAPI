import os
import sqlite3

import pandas as pd
from xml.etree import ElementTree

from api_database.fetch_db_file import fetch_file

def get_record(tree: ElementTree.Element) -> dict:
    """
    Gets the data from a record in the database

    Args:
        tree (ElementTree.Element): A element in the element tree

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
        tree (ElementTree.Element): A element in the element tree

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
        tree (ElementTree.Element): Element tree containing the table data
        conn (sqlite3.Connection): Connection to the database
    """
    df = get_data(tree)
    df = df.dropna(how="all", axis=1)
    drop_columns = ["ChangeDate", "ChangeAgent", "ChangeComment"]
    df = df.drop(columns=[x for x in drop_columns if x in df.columns])
    df.to_sql(tree.tag, conn, if_exists="replace", index=False)


def initialise_operator_db(
    conn: sqlite3.Connection, filepath: str, encoding: str
):
    """
    Initialises the database by downloading the data from the specified url

    Args:
        conn (sqlite3.Connection): Connection to the database
        filepath (str): Path to the operator data file
        encoding (str): Expected encoding of the data
    """
    root = ElementTree.parse(filepath).getroot()

    for tree in root:
        setup_table(tree, conn)


def setup_operator_database(
    conn: sqlite3.Connection,
    operator_filepath: str = "nocrecords.xml.gz",
    operator_url: str = "https://www.travelinedata.org.uk/noc/api/1.0/nocrecords.xml",
    operator_encoding: str = "windows-1252",
    **kwargs,
):
    """
    Sets up the operator part of the database at `connection` using the provided URL and encoding.

    Args:
        conn (sqlite3.Connection): Connection to the database
        operator_filepath (str): Path to the operator file. Defaults to "nocrecords.xml.gz"
        operator_url (str, optional): URL for operator XML data. Defaults to "https://www.travelinedata.org.uk/noc/api/1.0/nocrecords.xml".
        operator_encoding (str, optional): Encoding for the XML file. Defaults to "windows-1252".
    """
    if not os.path.isfile(operator_filepath):
        fetch_file(operator_url, operator_filepath)


    initialise_operator_db(conn, operator_filepath, operator_encoding)
    print("-- Operator database initialised")
