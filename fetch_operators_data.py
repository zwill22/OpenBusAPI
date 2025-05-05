import sqlite3
import polars as pl

def operators_data(conn: sqlite3.Connection) -> str:
    sql_path = "operators.sql"
    with open(sql_path, 'r') as f:
        sql_query = f.read()
    df = pl.read_database(query=sql_query, connection=conn, infer_schema_length=None)

    return df.write_json()


def operators_info(conn: sqlite3.Connection) -> list:
    sql_path = "operators.sql"
    with open(sql_path, 'r') as f:
        sql_query = f.read()
    df = pl.read_database(query=sql_query, connection=conn, infer_schema_length=None)

    return df.columns


if __name__ == "__main__":
    from io import StringIO
    from setup_operators_db import setup_database
    conn = setup_database()
    json = operators_data(conn)

    out_df = pl.read_json(StringIO(json))

    shape = out_df.shape
    print("Number of rows = {}".format(shape[0]))
    print("Number of columns = {}".format(shape[1]))
    print("Columns:")
    for column in out_df.columns:
        print(column)
    for mode in (out_df.get_column("Mode").unique()):
        print(mode)
