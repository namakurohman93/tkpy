import os
import hashlib
import binascii
from .connection import get_connection


def repr(obj):
    """ :func:`repr` is a function for representing of object using object's name
    and object's properties
    """
    properties = {k: v for k, v in vars(obj).items()}
    return f"{type(obj).__name__}({properties})"


class Lobby:
    """ :class:`Lobby` is a model class for `lobbies` table."""

    def __init__(self, **kwargs):
        self.id = kwargs.pop("id", None)
        self.email = kwargs.pop("email", None)
        self.password = kwargs.pop("password", None)
        self.gameworlds = []

    def __repr__(self):
        return repr(self)

    def get_gameworlds(self):
        """ :method:`get_gameworlds` is a method for find gameworld data from
        table `gameworlds` that have association with this lobby.
        """
        self.gameworlds = Gameworld.find_all(lobby_id=self.id)

    def add_gameworld(self, gameworld_name, driver):
        """ :method:`add_gameworld` is a method for add new entry to `gameworlds` table
        that have association with this lobby.
        """
        self.gameworlds.append(
            Gameworld.create(
                driver=driver, lobby_id=self.id, gameworld_name=gameworld_name
            )
        )

    def find_gameworld(self, gameworld_name):
        """ :method:`find_gameworld` is a method for find gameworld that have
        association with this lobby based on gameworld name.
        """
        for gameworld in self.gameworlds:
            if gameworld.gameworld_name == gameworld_name:
                return gameworld

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
    def create(email, password):
        """ :staticmeth:`create` is for insert new entry to `lobbies` table's. 

        :param email: - :class:`str`
        :param password: - :class:`str`

        return: :class:`str`
        """
        query = "INSERT INTO lobbies (email, password) VALUES (?, ?)"
        params = (email, password)

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            lastId = cursor.lastrowid

            return Lobby(id=lastId, email=email, password=password)

    @staticmethod
    def find_one(include=False, **kwargs):
        """ :staticmeth:`find_one` for find single result from table `lobbies` based
        on `kwargs`.
        """
        query = "SELECT * FROM lobbies"
        params = [value for value in kwargs.values()]

        if kwargs:
            query += " WHERE " + " AND ".join([f"{key} = ?" for key in kwargs.keys()])

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            result = cursor.fetchone()

            if result:
                lobby = Lobby(**{k: result[k] for k in result.keys()})

                if include is True:
                    lobby.get_gameworlds()

                return lobby

    @staticmethod
    def find_all(include=False, **kwargs):
        """ :staticmeth:`find_all` for find all result from table `lobbies` based
        on `kwargs`.
        """
        query = "SELECT * FROM lobbies"
        params = [value for value in kwargs.values()]

        if kwargs:
            query += " WHERE " + " AND ".join([f"{key} = ?" for key in kwargs.keys()])

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

            if results:
                lobbies = [
                    Lobby(**{k: result[k] for k in result.keys}) for result in results
                ]

                if include is True:
                    for lobby in lobbies:
                        lobby.get_gameworlds()

                return lobbies

    @staticmethod
    def update(updater, condition):
        """ :staticmeth:`update` will update lobbies entry with `updater` based on `condition` """
        query = (
            "UPDATE lobbies SET "
            + ", ".join([f"{key} = ?" for key in updater.keys()])
            + " WHERE "
            + " AND ".join([f"{key} = ?" for key in condition.keys()])
        )
        params = [*list(updater.values()), *list(condition.values())]

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()


class Gameworld:
    """ :class:`Gameworld` is a model class for `gameworlds` table."""

    def __init__(self, **kwargs):
        self.id = kwargs.pop("id", None)
        self.gameworld_name = kwargs.pop("gameworld_name", None)
        self.driver = kwargs.pop("driver", None)
        self.lobby_id = kwargs.pop("lobby_id", None)

    def __repr__(self):
        return repr(self)

    def save(self):
        updater = {
            "gameworld_name": self.gameworld_name,
            "driver": self.driver,
            "lobby_id": self.lobby_id,
        }
        Gameworld.update(updater=updater, condition={"id": self.id})

    @staticmethod
    def create(gameworld_name, driver, lobby_id):
        """ :staticmeth:`create` is for insert new entry to `gameworlds` table's. 

        :param gameworld_name: - :class:`str`
        :param driver: - :class:`primordial.Gameworld`
        :param lobby_id: - :class:`str`

        return: :class:`str`
        """
        query = (
            "INSERT INTO gameworlds (gameworld_name, driver, lobby_id) VALUES(?, ?, ?)"
        )
        params = (gameworld_name, driver, lobby_id)

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            lastId = cursor.lastrowid

            return Gameworld(
                id=lastId,
                driver=driver,
                lobby_id=lobby_id,
                gameworld_name=gameworld_name,
            )

    @staticmethod
    def find_one(**kwargs):
        """ :staticmeth:`find_one` for find single result from table `gameworlds` based
        on `kwargs`.
        """
        query = "SELECT * FROM gameworlds"
        params = [value for value in kwargs.values()]

        if kwargs:
            query += " WHERE " + " AND ".join([f"{key} = ?" for key in kwargs.keys()])

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            result = cursor.fetchone()

            if result:
                return Gameworld(**{k: result[k] for k in result.keys()})

    @staticmethod
    def find_all(**kwargs):
        """ :staticmeth:`find_all` for find all result from table `gameworlds` based
        on `kwargs`.
        """
        query = "SELECT * FROM gameworlds"
        params = [value for value in kwargs.values()]

        if kwargs:
            query += " WHERE " + " AND ".join([f"{key} = ?" for key in kwargs.keys()])

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

            if results:
                return [
                    Gameworld(**{k: result[k] for k in result.keys()})
                    for result in results
                ]

            return []

    @staticmethod
    def update(updater, condition):
        """ :staticmeth:`update` is for update entry on `gameworlds` based on condition that
        provided by user.

        :param updater: - :class:`dict` is a property that want to be updated on table
        :param condition: - :class:`dict` is a condition for update
        """
        query = (
            "UPDATE gameworlds SET "
            + ", ".join([f"{key} = ?" for key in updater.keys()])
            + " WHERE "
            + " AND ".join([f"{key} = ?" for key in condition.keys()])
        )
        params = [*list(updater.values()), *list(condition.values())]

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
