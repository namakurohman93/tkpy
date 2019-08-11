import sqlite3
import pathlib
import contextlib


BASE_DIR = pathlib.Path(__file__).resolve().parent


@contextlib.contextmanager
def get_db():
    db = sqlite3.connect(
        BASE_DIR / 'tkpy-credential.sqlite',
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()


def init_db():
    if not (BASE_DIR / 'tkpy-credential.sqlite').is_file():
        with get_db() as db:
            with open(BASE_DIR / 'schema.sql', 'r') as f:
                db.executescript(f.read())
