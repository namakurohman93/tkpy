from .connection import get_connection

def dict_parser(data):
    result = {}
    for key in data.keys():
        result[key] = data[key]

    return result

class Lobby:
    @staticmethod
    def find_all():
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM lobbies')

            results = cursor.fetchall()

            if results:
                return list(map(dict_parser, results))
            return None

    @staticmethod
    def find_by_pk(pk):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM lobbies WHERE id = ?', (pk, ))

            result = cursor.fetchone()

            if result:
                return dict_parser(result)
            return None

    @staticmethod
    def find_by_email(email):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM lobbies WHERE email = ?', (email, ))

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
                (email, password)
            )
            conn.commit()

            return cursor.lastrowid


class Gameworld:
    @staticmethod
    def find_by_lobby_id_and_gameworld_name(lobby_id, gameworld_name):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM gameworlds WHERE lobby_id = ? AND gameworld_name = ?',
                (lobby_id, gameworld_name)
            )

            result = cursor.fetchone()

            if result:
                return dict_parser(result)
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
