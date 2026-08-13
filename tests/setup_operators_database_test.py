import sqlite3
from io import StringIO

import polars as pl

from api_database.fetch_operators import fetch_operators_data, operators_info
from api_database.operators_database_setup import setup_operator_database
from tools import get_root


def test_operator_database_initialisation(tmp_path):
    db = tmp_path / "sample.db"

    conn = sqlite3.connect(db)

    operator_file = get_root() / "static" / "nocsample.xml"

    setup_operator_database(conn, operator_filepath=operator_file)

    op_data = fetch_operators_data(conn)

    out_df = pl.read_json(StringIO(op_data))

    print(out_df)

    assert out_df.shape == (2, 9)

    info = operators_info(conn)

    assert info == [
        "NOCCODE",
        "OperatorPublicName",
        "PubNmId",
        "Mode",
        "TTRteEnq",
        "FareEnq",
        "ComplEnq",
        "Twitter",
        "Website",
    ]
