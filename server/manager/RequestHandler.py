import json

from server.manager.account.DatabaseManager import DatabaseManager
from server.manager.account.Encryption import Encryption
from server.manager.account.TokenManager import TokenManager


class RequestHandler:
    def __init__(self):
        self.dbm = DatabaseManager("accounts.db")
        self.tm = TokenManager()
        self.encryption = Encryption()

        self.dbm.createTable()

        self.commands = {"CreateAccount": self.createAccount, "SignIn": self.signIn}
        """
        Create Account : [username, password]
        SignIn : [username, password, clientPubKey] -> clientPubKey encoded with b64 then decoded to utf-8
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
            if self.dbm.nameExists(args['username']):
                return 400, "Account creation error, Username already taken", None

            self.dbm.addAccount(args['username'], args['password'])
            print(f'created account: {args["username"]}')

            return 200, "Success. Account created", None

        except: # exception too broad but i will fix later
            return 400, "Account creation error", None

    def signIn(self, args):
        try:
            if self.dbm.validateAccount(args['username'], args['password']):
                userPublicKey, userPrivateKey = self.encryption.genUserKeys()
                token = self.tm.generateToken(args['username'], args['clientPubKey'], userPrivateKey)

                writtenResponse = 'Succes. Sign In complete'

                response = '{' + f'"writtenResponse": {self.enc}, "token": {token}, "userPublicKey": {userPublicKey}' + '}'

                print(f'successful sign into {args["username"]}')
                return 200, "Succes. Sign In complete", token, userPublicKey

            else:
                print(f'Account sign in failure on: {args["username"]}')
                return 400, "Sign In error", None # make more specific later, username does not exist, password incorrect etc

        except:
            print('unknown error')
            return 400, "Unknown Sign In error", None

"""
        response, m, uuid = self.rh.handlePost(body.decode("UTF-8"))
        resp = '{' + f'"writtenResponse": "{m}", "token": "{uuid}"' + '}' # bit of a hacky way to do this but running


"""