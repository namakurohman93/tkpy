from .connection import get_connection

class Lobby:
    @staticmethod
    def dict_parser(data):
        result = {}
        for key in data.keys():
            result[key] = data[key]

        return result

    @staticmethod
    def find_all():
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM lobbies')

            results = cursor.fetchall()

            if results:
                return list(map(Lobby.dict_parser, results))
            return None

    @staticmethod
    def find_by_pk(pk):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM lobbies WHERE id = ?', (pk, ))

            result = cursor.fetchone()

            if result:
                return Lobby.dict_parser(result)
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
