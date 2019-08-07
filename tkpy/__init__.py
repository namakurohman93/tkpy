from .map import Map
from .utilities import login as _login
from .villages import Villages
from .notepads import Notepad
from .farmlist import Farmlist
from .database import DB_DIR
from .database import get_db
from .database import get_user_id
from .database import get_driver
from .database import update_driver
from .database import insert_driver


def login(email, password, gameworld, avatar=None):
    user_id = get_user_id(email, password)
    try:
        driver, driver_id = get_driver(user_id, gameworld, avatar)
        try:
            driver.is_authenticated()
            driver.update_account()
        except:
            # update
            driver = _login(email, password, gameworld, avatar)
            update_driver(driver, driver_id)
    except:
        driver = _login(email, password, gameworld, avatar)
        insert_driver(user_id, gameworld, avatar, driver)
    return driver

def create_db():
    db = get_db()
    with open('tkpy/schema.sql', 'r') as f:
        db.executescript(f.read())
    db.close()


if DB_DIR.is_file() is False:
    create_db()
