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
                (email, password)
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
    def create(gameworld_name, driver, lobby_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO gameworlds (gameworld_name, driver, lobby_id) VALUES (?, ?, ?)',
                (gameworld_name, driver, lobby_id)
            )
            conn.commit()

            return cursor.lastrowid
