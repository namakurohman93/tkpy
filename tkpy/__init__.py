"""
  /^^   /^^
  /^^   /^^
/^/^ /^ /^^  /^^ /^ /^^  /^^   /^^
  /^^   /^^ /^^  /^  /^^  /^^ /^^
  /^^   /^/^^    /^   /^^   /^^^
  /^^   /^^ /^^  /^^ /^^     /^^
   /^^  /^^  /^^ /^^        /^^
                 /^^      /^^

Travian: Kingdom utilities for your need.
"""


from .map import Map
from .villages import Villages
from .notepads import Notepad
from .farmlist import Farmlist
from .database import DB_DIR
from .database import get_db
from .utilities import _login as login


def _create_db():
    with get_db() as db:
        with open('tkpy/schema.sql', 'r') as f:
            db.executescript(f.read())


if not DB_DIR.is_file():
    _create_db()
