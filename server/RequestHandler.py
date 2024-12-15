import json

from server.DatabaseManager import DatabaseManager


class RequestHandler:
    def __init__(self):
        self.dbm = DatabaseManager("accounts.db")
        self.dbm.createTable()

        self.commands = {"CreateAccount": self.createAccount, "SignIn": self.createAccount}
        """
        Create Account : [username, password]
        SignIn : [username, password]
        """

    def handlePost(self, data):
        d = json.loads(data)

        c = d['command']

        if c in self.commands:
            return self.commands[c](d['args'])
        else:
            return 400, "Command does not exist"

    def createAccount(self, args):
        try:
            self.dbm.addAccount(args['username'], args['password'])
            print('created account:', args['username'])

            return 200, "Success. Account created"
        except:
            return 400, "Account creation error, username already taken?"
