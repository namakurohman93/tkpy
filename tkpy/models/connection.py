import sqlite3
import pathlib
import contextlib
from .config import create_table

BASE_DIR = pathlib.Path(__file__).resolve().parent
DB_NAME = 'cred.sqlite'

DB_DIR = f'{BASE_DIR / DB_NAME}'

@contextlib.contextmanager
def get_connection():
    conn = sqlite3.connect(DB_DIR, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    try:
        create_table(conn)
        yield conn
    finally:
        conn.close()
