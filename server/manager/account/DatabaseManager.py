import sqlite3

class DatabaseManager:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cur = self.connection.cursor()

    def createTable(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS accounts(username text PRIMARY KEY, password text)""")

        self.connection.commit()

    def addAccount(self, username: str, password: str):
        entities = (username, password)

        self.cur.execute("INSERT INTO accounts(username, password) VALUES(?, ?)", entities)

        self.connection.commit()

    def nameExists(self, username: str) -> bool:
        self.cur.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE username=? LIMIT 1)", (username,))

        record = self.cur.fetchone()

        if record[0] == 1:
            return True
        else:
            return False

    def validateAccount(self, username: str, password: str) -> bool:
        self.cur.execute("SELECT password FROM accounts WHERE username = ?", (username,))

        record = self.cur.fetchall()

        if len(record) < 1:
            return False

        p = record[0][0]

        if password == p:
            return True
        else:
            return False

    def close(self):
        self.connection.close()
