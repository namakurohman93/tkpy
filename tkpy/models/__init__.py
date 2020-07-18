from .connection import get_connection


def flush_tables():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gameworlds")
        conn.commit()
        cursor.execute("DELETE FROM lobbies")
        conn.commit()

        return None
