import os
import uuid
import json
import pickle
import hashlib
import argparse
import binascii

from primordial import Lobby

# from .driver import Lobby
from .database import get_db
from .exception import DriverNotFound
from .exception import NotAuthenticated
from .exception import AvatarNotFound


def credential():
    """ :func:`credential` is an argument parser for parsing credential.

    Usage:
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

    return: :class:`Gameworld`
    """
    lobby = Lobby()
    lobby.authenticate(email, password)
    client = lobby.get_gameworld(gameworld, avatar)
    return client


def hash_password(password):
    """ :func:`hash_password` hashing a password.

    :param password: - :class:`str` password that want to be hassed.

    return: :class:`str`
    """
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
    """ :func:`verify_password` verify a stored password against one
    provided by user.

    :param stored_password: - :class:`str` hashed password.
    :param provided_password: - :class:`str` password that want to be
                                compared with hashed password.

    return: :class:`boolean`
    """
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


def retrieve_data(query, params):
    """ :func:`retrieve_data` for retrieve data from database.

    :param query: - :class:`str` query for database.
    :param params: - :class:`tuple` parameters that will be used for
                     query.

    return: :class:`dict`
    """
    with get_db() as db:
        return db.execute(query, params).fetchone()


def commit_query(query, params):
    """ :func:`commit_query` for commit query to database.

    :param query: - :class:`str` query for database.
    :param params: - :class:`tuple` parameters that will be used for
                     query.
    """
    with get_db() as db:
        db.execute(query, params)
        db.commit()


def get_user_id(email, password):
    """ :func:`get_user_id` send query to database for retrieve user id
    based on email and password.

    :param email: - :class:`str` email of user.
    :param password: - :class:`str` password of user.

    return: :class:`str`
    """
    user = retrieve_data(
        'SELECT * FROM user WHERE email = ?',
        (email,)
    )

    if user is None:
        return user

    if not verify_password(user['password'], password):
        raise NotAuthenticated('wrong password.')

    return user['id']


def add_user(email, password):
    """ :func:`add_user` add user to database and return its user id.

    :param email: - :class:`str` email of user.
    :param password: - :class:`str` password of user.

    return: :class:`str`
    """
    user_id = uuid.uuid4().hex

    commit_query(
        'INSERT INTO user (id, email, password) VALUES (?, ?, ?)',
        (user_id, email, hash_password(password))
    )

    return user_id


def get_driver_id(user_id, gameworld, avatar):
    """ :func:`get_driver_id` get driver id from database. If driver
    id not found, it will raise :exception:`DriverNotFound`.

    :param user_id: - :class:`str` user id.
    :param gameworld: - :class:`str` gameworld name.
    :param avatar: - :class:`str` avatar name.

    return: :class:`str`
    """
    driver = retrieve_data(
        'SELECT g.id FROM gameworld g JOIN user u ON g.user_id = u.id WHERE user_id = ? AND avatar = ? AND game_world = ?',
        (user_id, avatar or '?', gameworld)
    )

    if driver is None:
        raise DriverNotFound()

    return driver['id']


def insert_driver(user_id, driver, gameworld, avatar):
    """ :func:`insert_driver` insert driver to database.

    :param user_id: - class:`str` user id.
    :param driver: - class:`Gameworld` gameworld that want to be stored
                     to database.
    :param gameworld: - :class:`str` gameworld name.
    :param avatar: - :class:`str` avatar name.
    """
    commit_query(
        'INSERT INTO gameworld (id, user_id, driver, avatar, game_world) VALUES (?, ?, ?, ?, ?)',
        (uuid.uuid4().hex, user_id, pickle.dumps(driver), avatar or '?', gameworld)
    )


def update_driver(driver_id, driver):
    """ :func:`update_driver` update driver from database.

    :param driver_id: - :class:`str` driver id.
    :param driver: - :class:`Gameworld` gameworld that want to be updated
                     to database.
    """
    commit_query(
        'UPDATE gameworld SET driver = ? WHERE id = ?',
        (pickle.dumps(driver), driver_id)
    )


def get_driver(driver_id):
    """ :func:`get_driver` get driver from database.

    :param driver_id: - :class:`str` driver id.

    return: :class:`Gameworld`
    """
    driver = retrieve_data(
        'SELECT driver FROM gameworld WHERE id = ?',
        (driver_id,)
    )

    return pickle.loads(driver['driver'])


def _login(email, password, gameworld, avatar=None):
    """ :func:`_login` is used for login to TK and return
    :class:`Gameworld` object.

    :param email: - :class:`str` email user.
    :param password: - :class:`str` password user.
    :param gameworld: - :class:`str` gameworld name.
    :param avatar: - :class:`str` (optional) avatar name. Default = None

    return: :class:`Gameworld`
    """
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


def pprint(data, indent=4):
    """ :func:`pprint` for print `dict` or `list` with indentation so
    it can be more read-able.

    :param data: - :class:`dict` data that want to be printed with indentation.
    :param indent: - :class:`int` spaces that used for indentation. Default = 4
    """
    print(json.dumps(data, indent=indent))


def relogin(email, password, gameworld, avatar=None, lobby=Lobby()):

    lobby.authenticate(email, password)

    if avatar:
        gameworld_id = None
        avatar_id = get_avatar_id(lobby, avatar, gameworld)
    else:
        gameworld_id = get_gameworld_id(lobby, gameworld)
        avatar_id = None

    driver = lobby.connect_to_gameworld(
        gameworld_name=gameworld,
        gameworld_id=gameworld_id,
        avatar_id=avatar_id,
    )

    return driver

def get_avatar_id(lobby, avatar, gameworld):
    for x in ('Collection:Sitter:1', 'Collection:Sitter:4'):
        r = lobby.cache.get({'names':[x]})

        for avatar in r['cache'][0]['data']['cache']:
            if (
                avatar['data']['avatarName'] == avatar
                and avatar['data']['worldName'].lower() == gameworld.lower()
            ):
                return avatar['data']['avatarIdentifier']

    raise AvatarNotFound(f'Avatar {avatar} on {gameworld} not found.')

def get_gameworld_id(lobby, gameworld):
    r = lobby.cache.get({'names':['Collection:Avatar']})

    for avatar in r['cache'][0]['data']['cache']:
        if gameworld.lower() == avatar['data']['worldName'].lower():
            gameworld_id = avatar['data']['consumersId']
            return gameworld_id

    raise AvatarNotFound(f'Avatar on {gameworld} not found')
