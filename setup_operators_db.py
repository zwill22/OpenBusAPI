import os.path
import sqlite3
import pandas as pd
from xml.etree import ElementTree
from tools.output import apiOutput


def get_record(tree: ElementTree.Element) -> dict:
    data = {}
    for branch in tree:
        data[branch.tag] = branch.text

    return data


def get_data(tree: ElementTree.Element) -> pd.DataFrame:
    tag = tree.tag

    operators = []
    for record in tree.findall(tag + "Record"):
        record_data = get_record(record)
        operators.append(record_data)

    return pd.DataFrame(operators)


def setup_table(tree: ElementTree.Element, conn: sqlite3.Connection):
    df = get_data(tree)
    df = df.dropna(how="all", axis=1)
    drop_columns = ["ChangeDate", "ChangeAgent", "ChangeComment"]
    df = df.drop(columns=[x for x in drop_columns if x in df.columns])
    df.to_sql(tree.tag, conn, if_exists="replace", index=False)


def initialise_db(conn: sqlite3.Connection, url: str, encoding: str):
    output = apiOutput(url)
    root = ElementTree.fromstring(output.decode(encoding))

    for tree in root:
        setup_table(tree, conn)


def setup_database(
    reinitialise=False,
    url="https://www.travelinedata.org.uk/noc/api/1.0/nocrecords.xml",
    encoding="windows-1252",
    db="operators.db",
) -> sqlite3.Connection:
    db_exists = False

    if os.path.isfile(db):
        db_exists = True

    conn = sqlite3.connect(db)

    if not db_exists or reinitialise:
        initialise_db(conn, url, encoding)

    return conn


if __name__ == "__main__":
    connection = setup_database(reinitialise=True)
    connection.close()
