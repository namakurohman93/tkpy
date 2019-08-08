import os
import uuid
import pickle
import hashlib
import binascii
import argparse
from .driver import Lobby
from .database import get_db
from .exception import DriverNotFound
from .exception import NotAuthenticated


def credential():
    """ :func:`credential` is an argument parser for parsing credential.

    Usage::
        >>> email, password, gameworld, avatar = credential()
    """
    parser = argparse.ArgumentParser(usage='python3 %(prog)s <email> <password> <gameworld> [--avatar]')

    parser.add_argument('email', metavar='email', type=str, help='your email', nargs=1)
    parser.add_argument('password', metavar='password', type=str, help='your password', nargs=1)
    parser.add_argument('gameworld', metavar='gameworld', type=str, help='gameworld name', nargs=1)
    parser.add_argument('--avatar', help='your avatar', type=str, default=None, nargs='*')

    args = parser.parse_args()

    email = args.email[0]
    password = args.password[0]
    gameworld = args.gameworld[0]

    avatar = ' '.join(args.avatar) if args.avatar else None

    return email, password, gameworld, avatar


def login(email, password, gameworld, avatar):
    """ :func:`login` for login to gameworld and return
    :class:`Gameworld` object.
    """
    lobby = Lobby()
    lobby.authenticate(email, password)
    client = lobby.get_gameworld(gameworld, avatar)
    return client


def hash_password(password):
    """ Hashing a password. """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512',
        password.encode('utf-8'),
        salt,
        100000
    )
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """ Verify a stored password against one provided by user. """
    salt = stored_password[:64]
    stored_password = stored_password[64:]

    pwdhash = hashlib.pbkdf2_hmac(
        'sha512',
        provided_password.encode('utf-8'),
        salt.encode('ascii'),
        100000
    )
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')

    return pwdhash == stored_password


def get_data_from_db(query, params):
    with get_db() as db:
        return db.execute(query, params).fetchone()


def insert_data_to_db(query, params):
    with get_db() as db:
        db.execute(query, params)
        db.commit()


def get_user_id(email, password):
    user = get_data_from_db(
        'SELECT * FROM user WHERE email = ?',
        (email,)
    )

    if user is None:
        return user

    if not verify_password(user['password'], password):
        raise NotAuthenticated('wrong password.')

    return user['id']


def add_user(email, password):
    user_id = uuid.uuid4().hex

    insert_data_to_db(
        'INSERT INTO user (id, email, password) VALUES (?, ?, ?)',
        (user_id, email, hash_password(password))
    )

    return user_id


def get_driver_id(user_id, gameworld, avatar):
    driver = get_data_from_db(
        'SELECT g.id FROM gameworld g JOIN user u ON g.user_id = u.id WHERE user_id = ? AND avatar = ? AND game_world = ?',
        (user_id, avatar or '?', gameworld)
    )

    if driver is None:
        raise DriverNotFound()

    return driver['id']


def insert_driver(user_id, driver, gameworld, avatar):
    insert_data_to_db(
        'INSERT INTO gameworld (id, user_id, driver, avatar, game_world) VALUES (?, ?, ?, ?, ?)',
        (uuid.uuid4().hex, user_id, pickle.dumps(driver), avatar or '?', gameworld)
    )


def update_driver(driver_id, driver):
    insert_data_to_db(
        'UPDATE gameworld SET driver = ? WHERE id = ?',
        (pickle.dumps(driver), driver_id)
    )


def get_driver(driver_id):
    driver = get_data_from_db(
        'SELECT driver FROM gameworld WHERE id = ?',
        (driver_id,)
    )

    return pickle.loads(driver['driver'])


def _login(email, password, gameworld, avatar=None):
    user_id = get_user_id(email, password) or add_user(email, password)

    try:
        driver_id = get_driver_id(user_id, gameworld, avatar)

    except DriverNotFound:
        driver = login(email, password, gameworld, avatar)
        insert_driver(user_id, driver, gameworld, avatar)

    else:
        driver = get_driver(driver_id)

        try:
            driver.is_authenticated()

        except NotAuthenticated:
            driver = login(email, password, gameworld, avatar)
            update_driver(driver_id, driver)
            
        else:
            driver.update_account()

    return driver
