import pathlib
import sqlite3
import contextlib

BASE_DIR = pathlib.Path(__file__).resolve().parent


@contextlib.contextmanager
def get_db():
    """ Context function for get connection to 'tkpy-credential.sqlite'
    database.

    Usage:
        >>> with get_db() as db:
        >>>    user = db.execute('select * from user').fetchall()
        >>>
    """
    db = sqlite3.connect(
        BASE_DIR / "tkpy-credential.sqlite",
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()


def init_db():
    """ Initialize database for tkpy use. It will overwrite old
    'tkpy-credential.sqlite' file.
    """
    with get_db() as db:
        with open(BASE_DIR / "schema.sql", "r") as f:
            db.executescript(f.read())
