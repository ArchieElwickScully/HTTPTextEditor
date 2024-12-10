from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
import json

class DatabaseManager:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cur = self.connection.cursor()


    def createTable(self):        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS accounts(username text PRIMARY KEY, password text)""")

        self.connection.commit()

    def addAccount(self, username, password):
        entities = (username, password)

        self.cur.execute("INSERT INTO accounts(username, password) VALUES(?, ?)", entities)

        self.connection.commit()

    def nameExists(self, username):
        self.cur.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE username=? LIMIT 1)", (username,))
        
        record = self.cur.fetchone()
        
        if record[0] == 1:
            return True
        else:
            return False

    def validateAccount(self, username, password):
        self.cur.execute("SELECT password FROM accounts WHERE username = ?", (username,))

        record = self.cur.fetchall()
        p = record[0][0]

        if password == p:
            return True
        else:
            return False

    def close(self):
        self.connection.close()
        

class RequestHandler:
    def __init__(self):
        self.dbm = DatabaseManager("accounts.db")
        self.dbm.createTable()
        
        self.commands = {"CreateAccount" : self.createAccount, "SignIn" : self.createAccount}
        """
        Create Account : [username, password]
        SignIn : [username, password]
        """


    def handlePost(self, data):
        d = json.loads(data)

        c = d['command']

        if c in self.commands:
            return self.commands[c](d['args'])
        exit()
        else:
            return 400, "Command does not exist"
        
    def createAccount(self, args):
        try:
            self.dbm.addAccount(args['username'], args['password'])
            print('created account:', args['username'])
            
            return 200, "Success. Account created"
        except:
            return 400, "Account creation error, username already taken?"

class HTTP(BaseHTTPRequestHandler):
    rh = RequestHandler()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        #self.wfile.write(bytes(""))

    def do_POST(self):
        length = int(self.headers['Content-length'])
        body = self.rfile.read(length)

        response, m = self.rh.handlePost(body.decode("UTF-8"))
                
        self.send_response(response)
        self.end_headers()

        self.wfile.write(bytes(m, encoding='utf-8'))


def main():
    PORT = 8000

    server = HTTPServer(("", PORT), HTTP)

    print("Server started on port", PORT)

    server.serve_forever()
    server.server_close()


if __name__ == "__main__":
    main()
