import os.path
import sqlite3
import polars as pl

sql_path = os.path.join("operators", "operators.sql")


def fetch_operators_data(conn: sqlite3.Connection) -> str:
    """
    Fetches the contents of the operators database in JSON format from the
    sqlite3 database

    Args:
        conn: Connection to the sqlite3 database

    Returns: Data in JSON format
    """
    with open(sql_path, "r") as f:
        sql_query = f.read()
    df = pl.read_database(query=sql_query, connection=conn, infer_schema_length=None)

    return df.write_json()


def operators_info(conn: sqlite3.Connection) -> list:
    """
    Fetches a list of the fields in the operators database

    Args:
        conn: Connection to the sqlite3 database

    Returns: List of columns in the operators database
    """
    with open(sql_path, "r") as f:
        sql_query = f.read()
    df = pl.read_database(query=sql_query, connection=conn, infer_schema_length=None)

    return df.columns


if __name__ == "__main__":
    from io import StringIO
    from operators.initialise_database import setup_database

    connection = setup_database()
    json = fetch_operators_data(connection)

    out_df = pl.read_json(StringIO(json))

    print(out_df.head())
