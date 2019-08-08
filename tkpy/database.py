import sqlite3
import pathlib
import contextlib


DB_DIR = pathlib.Path.home() / 'tkpy-credential.sqlite'


@contextlib.contextmanager
def get_db():
    db = sqlite3.connect(DB_DIR, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()
