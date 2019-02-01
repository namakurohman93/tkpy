import os
import pickle
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Database:
    def __init__(self, email, password, gameworld):
        self.path = os.path.join(BASE_DIR, 'credential.db')
        self.email = email
        self.password = password
        self.gameworld = gameworld
        if not os.path.isfile(self.path):
            self._create_database()

    def _create_database(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute('''CREATE TABLE credential
            (email text, password text, gameworld text, driver BLOB)'''
        )
        con.commit()
        con.close()

    def get_driver(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute(
            '''SELECT driver FROM credential WHERE email=? AND password=? AND
            gameworld=?''',
            (self.email, self.password, self.gameworld)
        )
        pickled = cur.fetchone()
        con.close()
        if pickled:
            client = pickle.loads(*pickled)
        else:
            client = None
        return client

    def update_data(self, driver):
        pickled = pickle.dumps(driver)
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute(
            '''UPDATE credential SET driver=?
            WHERE email=? AND password=? AND gameworld=?''',
            (pickled, self.email, self.password, self.gameworld)
        )
        con.commit()
        con.close()

    def insert_data(self, driver):
        pickled = pickle.dumps(driver)
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute(
            '''INSERT INTO credential VALUES (?, ?, ?, ?)''',
            (self.email, self.password, self.gameworld, pickled)
        )
        con.commit()
        con.close()
