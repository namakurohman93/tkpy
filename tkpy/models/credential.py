import os
import hashlib
import binascii
from .connection import get_connection


def dict_parser(data):
    """ `dict_parser` is a function for parsing :class:`sqlite3.Row` into `dict`.

    :param data: - :class:`sqlite3.Row`

    :return: :class:`dict`
    """
    result = {}
    for key in data.keys():
        result[key] = data[key]

    return result


def query_maker(data):
    """ `query_maker` is a function for parsing :class:`dict` into query for querying.

    :param data: - :class:`dict`

    :return: :class:`str`
    """
    temp = []
    for key in data.keys():
        temp.append(f"{key} = ?")

    return " AND ".join(temp)


class Lobby:
    """ :class:`Lobby` is a model class for `lobbies` table."""

    @staticmethod
    def hash_password(password):
        """ :staticmeth:`hash_password` for hashing string. 

        :param password: - :class:`str`

        return: :class:`str`
        """
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")

        pwdhash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)

        return (salt + pwdhash).decode("ascii")

    @staticmethod
    def verify_password(hashed_password, password):
        """ :staticmeth:`verivy_password` for comparing hashed password with provided password.

        :param hashed_password: - :class:`str`
        :param password: - :class:`str`

        return: :class:`bool`
        """
        salt = hashed_password[:64]
        hashed_password = hashed_password[64:]

        pwdhash = hashlib.pbkdf2_hmac(
            "sha512", password.encode("utf-8"), salt.encode("ascii"), 100000
        )
        pwdhash = binascii.hexlify(pwdhash).decode("ascii")

        return pwdhash == hashed_password

    @staticmethod
    def find_one(**kwargs):
        """ :staticmeth:`find_one` for find single result from table `lobbies` based
        on `kwargs`.
        """
        query = "SELECT * FROM lobbies"
        params = []

        if kwargs:
            query += " WHERE " + query_maker(kwargs)
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
        """ :staticmeth:`create` is for insert new entry to `lobbies` table's. 

        :param email: - :class:`str`
        :param password: - :class:`str`

        return: :class:`str`
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO lobbies (email, password) VALUES (?, ?)",
                (email, Lobby.hash_password(password)),
            )
            conn.commit()

            return cursor.lastrowid


class Gameworld:
    """ :class:`Gameworld` is a model class for `gameworlds` table."""

    @staticmethod
    def find_one(**kwargs):
        """ :staticmeth:`find_one` for find single result from table `gameworlds` based
        on `kwargs`.
        """
        query = "SELECT * FROM gameworlds"
        params = []

        if kwargs:
            query += " WHERE " + query_maker(kwargs)
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
        """ :staticmeth:`update` is for update entry on `gameworlds` based on condition that
        provided by user.

        :param updater: - :class:`dict` is a property that want to be updated on table
        :param condition: - :class:`dict` is a condition for update
        """
        query = "UPDATE gameworlds SET "
        temp = []
        params = [*list(updater.values()), *list(condition.values())]

        for key in updater.keys():
            temp.append(f"{key} = ?")

        query += ", ".join(temp)

        query += " WHERE " + query_maker(condition)

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            return None

    @staticmethod
    def create(gameworld_name, driver, lobby_id):
        """ :staticmeth:`create` is for insert new entry to `gameworlds` table's. 

        :param gameworld_name: - :class:`str`
        :param driver: - :class:`primordial.Gameworld`
        :param lobby_id: - :class:`str`

        return: :class:`str`
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gameworlds (gameworld_name, driver, lobby_id) VALUES (?, ?, ?)",
                (gameworld_name, driver, lobby_id),
            )
            conn.commit()

            return cursor.lastrowid
