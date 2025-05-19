import sqlite3
import polars as pl


def get_stops(
    conn: sqlite3.Connection,
    min_lat: float,
    min_long: float,
    max_lat: float,
    max_long: float,
    **kwargs,
):
    """
    Return all stops in the requested area

    Args:
        conn (sqlite3.Connection): Connection to the database
        min_lat (float): Minimum latitude
        min_long (float): Minimum longitude
        max_lat (float): Maximum latitude
        max_long (float): Maximum longitude
        **kwargs ():

    Returns: Stop data in JSON format
    """

    sql_query = """
    SELECT * FROM Stops
        WHERE Latitude BETWEEN {0} AND {1}
        AND Longitude BETWEEN {2} AND {3};
    """.format(min_lat, max_lat, min_long, max_long)

    df = pl.read_database(query=sql_query, connection=conn, infer_schema_length=None)

    return df.write_json()


def get_stops_code(conn: sqlite3.Connection, codes: list[str], **kwargs):
    """
    Return all stops in the requested area

    Args:
        conn (sqlite3.Connection): Connection to the database
        codes (list[str]): List of unique stop codes

    Returns: Stop data in JSON format
    """

    codes_str = "'" + "', '".join(codes) + "'"

    sql_query = """
    SELECT * 
    FROM Stops
    WHERE NaptanCode IN ({0})
    OR ATCOCode IN ({0});
    """.format(codes_str)

    df = pl.read_database(query=sql_query, connection=conn, infer_schema_length=None)

    return df.write_json()
