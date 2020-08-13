from .connection import get_connection


def flush_tables():
    """ `flush_tables` if a function for flushing data from tables. """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gameworlds")
        cursor.execute("DELETE FROM lobbies")
        conn.commit()

        return None
