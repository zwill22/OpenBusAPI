import os.path
import sqlite3
import pandas as pd
from xml.etree import ElementTree
from tools.output import apiOutput


def get_data(tree: ElementTree.Element):
    data = {}
    for branch in tree:
        data[branch.tag] = branch.text

    return data


def noc_data(tree: ElementTree.Element):
    noc_table = tree.find("NOCTable")
    operators = []
    for record in noc_table.findall("NOCTableRecord"):
        record_data = get_data(record)
        operators.append(record_data)

    return pd.DataFrame(operators)


def setup_noc_table(root: ElementTree.Element, conn: sqlite3.Connection):
    df = noc_data(root)
    df = df.dropna(how="all", axis=1)
    df = df.drop(columns=["ChangeDate", "ChangeAgent", "ChangeComment"])
    df.to_sql("noc_table", conn, if_exists="replace", index=False)


def initialise_db(conn: sqlite3.Connection, url: str, encoding: str):
    output = apiOutput(url)
    root = ElementTree.fromstring(output.decode(encoding))

    setup_noc_table(root, conn)


def main():
    db_exists = False
    reinitialise = True
    db = "bus_operators.db"

    if os.path.isfile(db):
        db_exists = True

    conn = sqlite3.connect(db)
    url = "https://www.travelinedata.org.uk/noc/api/1.0/nocrecords.xml"
    encoding = "windows-1252"

    if not db_exists or reinitialise:
        initialise_db(conn, url, encoding)


if __name__ == "__main__":
    main()
