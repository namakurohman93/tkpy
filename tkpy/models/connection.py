import sqlite3
import pathlib
import contextlib
from .config import create_table

BASE_DIR = pathlib.Path(__file__).resolve().parent
DB_NAME = "cred.sqlite"

DB_DIR = f"{BASE_DIR / DB_NAME}"


@contextlib.contextmanager
def get_connection():
    """ `get_connection` is a function for create connection to sqlite database and maintain
    connectionn as context management.

    :yield: :class:`sqlite3.Connection`
    """
    conn = sqlite3.connect(DB_DIR, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    try:
        create_table(conn)
        yield conn
    finally:
        conn.close()
