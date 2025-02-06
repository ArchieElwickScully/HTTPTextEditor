import json

from server.manager.account.DatabaseManager import DatabaseManager
from server.manager.account.TokenManager import TokenManager


class RequestHandler:
    def __init__(self):
        self.dbm = DatabaseManager("accounts.db")
        self.tm = TokenManager()

        self.dbm.createTable()

        self.commands = {"CreateAccount": self.createAccount, "SignIn": self.signIn}
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
            print("returned command does not exist")
            return 400, "Command does not exist", None

    def createAccount(self, args):
        try:
            self.dbm.addAccount(args['username'], args['password'])
            print(f'created account: {args['username']}')

            return 200, "Success. Account created", None
        except: # exception too broad but i will fix later
            return 400, "Account creation error, username already taken?", None

    def signIn(self, args):
        try:
            if self.dbm.validateAccount(args['username'], args['password']):

                token = self.tm.generateToken(args['username'])

                print(f'successful sign into {args['username']}')
                return 200, "Succes. Sign In complete", token
            else:
                print(f'Account sign in failure on: {args['username']}')
                return 400, "Sign In error", None # make more specific later, username does not exist, password incorrect etc

        except:
            print('unknown error')
            return 400, "Unknown Sign In error", None
