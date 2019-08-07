import os
import time
import uuid
import pickle
import sqlite3
import pathlib
import hashlib
import binascii

from .utilities import hash_password
from .utilities import verify_password
from .exception import DriverNotFound
from .exception import NotAuthenticated

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = pathlib.Path.home() / 'tkpy-credential.sqlite'


# def hash_password(password):
#     """ Hash a password for storing. """
#     salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
#     pwdhash = hashlib.pbkdf2_hmac(
#         'sha512',
#         password.encode('utf-8'),
#         salt,
#         100000
#     )
#     pwdhash = binascii.hexlify(pwdhash)
#     return (salt + pwdhash).decode('ascii')
#
#
# def verify_password(stored_password, provided_password):
#     """ Verify a stored password against one provided by user. """
#     salt = stored_password[:64]
#     stored_password = stored_password[64:]
#     pwdhash = hashlib.pbkdf2_hmac(
#         'sha512',
#         provided_password.encode('utf-8'),
#         salt.encode('ascii'),
#         100000
#     )
#     pwdhash = binascii.hexlify(pwdhash).decode('ascii')
#     return pwdhash == stored_password


# class CredentialDb:
#     def __init__(self, email, password, gameworld, avatar=None):
#         # self.path = os.path.join(BASE_DIR, 'credential.db')
#         # self.email = email
#         # self.password = hash_password(password)
#         # self.gameworld = gameworld
#         # self.avatar = avatar or 'empty'
#         # if not os.path.isfile(self.path):
#         #     self._create_database()
#         self.gameworld = gameworld
#         self.avatar = avatar
#         self.path = HOME_DIR / 'tkpy-credential.sqlite'
#         if not self.path.is_file():
#             self._create_database()
#         self.user_id = self._get_user_id(email, password)
#
#     def _get_user_id(self, email, password):
#         con = sqlite3.connect(self.path)
#         cur = con.cursor()
#         cur.execute(
#             'select * from credential where email=?', (email,)
#         )
#         credential = cur.fetchone()
#         con.close()
#         if credential is None:
#             return self._register_email(email, password)
#         if not verify_password(credential['password'], password):
#             raise NotAuthenticated('your password is wrong.')
#         return credential['id']
#
#     def _register_email(self, email, password):
#         user_id = int(time.time())
#         con = sqlite3.connect(self.path)
#         cur = con.cursor()
#         cur.execute(
#             'insert into credential (id, email, password) values (?, ?, ?)',
#             (user_id, email, hash_password(password))
#         )
#         con.commit()
#         con.close()
#         return user_id
#
#     def _create_database(self):
#         con = sqlite3.connect(self.path)
#         cur = con.cursor()
#         # cur.execute('''CREATE TABLE credential
#         #     (email text, password text, gameworld text, driver BLOB, avatar text)'''
#         # )
#         cur.execute("""
#             create table credential(
#                 id integer  primary key,
#                 email text unique not null,
#                 password text not null
#             )"""
#         )
#         cur.execute("""
#             create table gameworld(
#                 id integer primary key,
#                 credential_id text not null,
#                 gameworld_name text,
#                 driver blob,
#                 avatar text,
#                 foreign key (credential_id) references credential (id)
#             )"""
#         )
#         con.commit()
#         con.close()
#
#     def get(self):
#         con = sqlite3.connect(self.path)
#         cur = con.cursor()
#         # cur.execute(
#         #     '''SELECT driver FROM credential WHERE email=? AND password=? AND
#         #     gameworld=? AND avatar=?''',
#         #     (self.email, self.password, self.gameworld, self.avatar)
#         # )
#         cur.execute(
#             '''select g.id, credential_id, gameworld_name, driver,
#             avatar from gameworld g join credential c
#             on g.credential_id = c.id where credential_id = ? and
#             gameworld_name = ? and avatar = ?''',
#             (self.user_id, self.gameworld, self.avatar)
#         )
#         pickled = cur.fetchone()
#         con.close()
#         if pickled:
#             # return pickle.loads(*pickled)
#             return pickle.loads(pickled['driver'])
#         raise DriverNotFound()
#
#     def update(self, driver):
#         pickled = pickle.dumps(driver)
#         con = sqlite3.connect(self.path)
#         cur = con.cursor()
#         # cur.execute(
#         #     '''UPDATE credential SET driver=?
#         #     WHERE email=? AND password=? AND gameworld=? AND avatar=?''',
#         #     (pickled, self.email, self.password, self.gameworld, self.avatar)
#         # )
#         cur.execute(
#             '''update gameworld set driver=? where credential_id = ? and
#             gameworld_name = ? and avatar = ?''',
#             (self.user_id, self.gameworld, self.avatar)
#         )
#         con.commit()
#         con.close()
#
#     def insert(self, driver):
#         pickled = pickle.dumps(driver)
#         gameworld_id = int(time.time())
#         con = sqlite3.connect(self.path)
#         cur = con.cursor()
#         # cur.execute(
#         #     '''INSERT INTO credential VALUES (?, ?, ?, ?, ?)''',
#         #     (self.email, self.password, self.gameworld, pickled, self.avatar)
#         # )
#         cur.execute(
#             '''insert into gameworld (id, credential_id, gameworld_name,
#             driver, avatar) values (?, ?, ?, ?, ?)''',
#             (gameworld_id, self.user_id, self.gameworld, pickled,
#             self.avatar)
#         )
#         con.commit()
#         con.close()


def get_db():
    db = sqlite3.connect(DB_DIR, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db


def get_user_id(email, password):
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE email = ?', (email,)
    ).fetchone()
    if user is None:
        return add_user(email, password, db)
    db.close()
    if not verify_password(user['password'], password):
        raise NotAuthenticated('wrong password.')
    return user['id']


def add_user(email, password, db):
    user_id = uuid.uuid4().hex
    db.execute(
        'INSERT INTO user (id, email, password) VALUES (?, ? ,?)',
        (user_id, email, hash_password(password))
    )
    db.commit()
    db.close()
    return user_id


def get_driver(user_id, gameworld, avatar):
    db = get_db()
    gw = db.execute(
        '''SELECT g.id, user_id, driver, avatar, game_world FROM
        gameworld g JOIN user u on g.user_id = c.id WHERE user_id = ?
        AND avatar = ? AND game_world = ?''',
        (user_id, avatar, gameworld)
    ).fetchone()
    db.close()
    if gw is None:
        raise DriverNotFound()
    return pickle.loads(gw['driver']), gw['id']


def insert_driver(user_id, gameworld, avatar, driver):
    db = get_db()
    pickled = pickle.dumps(driver)
    gameworld_id = uuid.uuid4().hex
    db.execute(
        '''INSERT INTO gameworld (id, user_id, driver, avatar, game_world)
        VALUES (?, ?, ?, ?, ?)''',
        (gameworld_id, user_id, pickled, avatar, gameworld)
    )
    db.commit()
    db.close()


def update_driver(driver, driver_id):
    db = get_db()
    pickled = pickle.dumps(driver)
    db.execute(
        'UPDATE gameworld SET driver = ? WHERE id = ?',
        (pickled, driver_id)
    )
    db.commit()
    db.close()
