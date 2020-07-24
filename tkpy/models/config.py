import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent
SCHEMA_NAME = "schema.sql"

SCHEMA_DIR = f"{BASE_DIR / SCHEMA_NAME}"


def create_table(conn):
    """ `create_table` is a function for create table based on `schema`.

    :param conn: - :class:`sqlite3.Connection`
    """
    with open(SCHEMA_DIR) as f:
        conn.executescript(f.read())
