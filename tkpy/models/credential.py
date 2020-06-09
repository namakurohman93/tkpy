import os
import hashlib
import binascii
from .connection import get_connection

def dict_parser(data):
    result = {}
    for key in data.keys():
        result[key] = data[key]

    return result

def query_maker(data):
    temp = []
    for key in data.keys():
        temp.append(f'{key} = ?')

    return ' AND '.join(temp)

class Lobby:
    @staticmethod
    def hash_password(password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')

        pwdhash = hashlib.pbkdf2_hmac(
            'sha512',
            password.encode('utf-8'),
            salt,
            100000
        )
        pwdhash = binascii.hexlify(pwdhash)

        return (salt + pwdhash).decode('ascii')

    @staticmethod
    def verify_password(hashed_password, password):
        salt = hashed_password[:64]
        hashed_password = hashed_password[64:]

        pwdhash = hashlib.pbkdf2_hmac(
            'sha512',
            password.encode('utf-8'),
            salt.encode('ascii'),
            100000
        )
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')

        return pwdhash == hashed_password

    @staticmethod
    def find_one(**kwargs):
        query = 'SELECT * FROM lobbies'
        params = []

        if kwargs:
            query += ' WHERE ' + query_maker(kwargs)
            params = list(kwargs.values())

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            result = cursor.fetchone()

            if result:
                return dict_parser(result)
            return None

    @staticmethod
    def create(email, password):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO lobbies (email, password) VALUES (?, ?)',
                (email, Lobby.hash_password(password))
            )
            conn.commit()

            return cursor.lastrowid


class Gameworld:
    @staticmethod
    def find_one(**kwargs):
        query = 'SELECT * FROM gameworlds'
        params = []

        if kwargs:
            query += ' WHERE ' + query_maker(kwargs)
            params = list(kwargs.values())

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            result = cursor.fetchone()

            if result:
                return dict_parser(result)
            return None

    @staticmethod
    def update(updater, condition):
        query = 'UPDATE gameworlds SET '
        temp = []
        params = [*list(updater.values()), *list(condition.values())]

        for key in updater.keys():
            temp.append(f'{key} = ?')

        query += ', '.join(temp)

        query += ' WHERE ' + query_maker(condition)

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            return None

    @staticmethod
    def create(gameworld_name, driver, lobby_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO gameworlds (gameworld_name, driver, lobby_id) VALUES (?, ?, ?)',
                (gameworld_name, driver, lobby_id)
            )
            conn.commit()

            return cursor.lastrowid
