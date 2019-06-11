import os
import pickle
import sqlite3
from .exception import DriverNotFound

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class CredentialDb:
    def __init__(self, email, password, gameworld, avatar=None):
        self.path = os.path.join(BASE_DIR, 'credential.db')
        self.email = email
        self.password = password
        self.gameworld = gameworld
        self.avatar = avatar or 'empty'
        if not os.path.isfile(self.path):
            self._create_database()

    def _create_database(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute('''CREATE TABLE credential
            (email text, password text, gameworld text, driver BLOB, avatar text)'''
        )
        con.commit()
        con.close()

    def get(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute(
            '''SELECT driver FROM credential WHERE email=? AND password=? AND
            gameworld=? AND avatar=?''',
            (self.email, self.password, self.gameworld, self.avatar)
        )
        pickled = cur.fetchone()
        con.close()
        if pickled:
            return pickle.loads(*pickled)
        raise DriverNotFound()

    def update(self, driver):
        pickled = pickle.dumps(driver)
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute(
            '''UPDATE credential SET driver=?
            WHERE email=? AND password=? AND gameworld=? AND avatar=?''',
            (pickled, self.email, self.password, self.gameworld, self.avatar)
        )
        con.commit()
        con.close()

    def insert(self, driver):
        pickled = pickle.dumps(driver)
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute(
            '''INSERT INTO credential VALUES (?, ?, ?, ?, ?)''',
            (self.email, self.password, self.gameworld, pickled, self.avatar)
        )
        con.commit()
        con.close()
