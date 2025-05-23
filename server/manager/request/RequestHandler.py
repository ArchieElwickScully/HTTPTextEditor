import json
import uuid

from server.manager.account.DatabaseManager import DatabaseManager
from server.manager.request.Encryption import Encryption
from server.manager.account.TokenManager import TokenManager
from server.manager.request.ResponseBuilder import Response


class RequestHandler:
    def __init__(self):
        self.dbm = DatabaseManager("accounts.db")
        self.tm = TokenManager()
        self.encryption = Encryption()

        self.dbm.createTable()

        self.commands = {
            "CreateAccount": self.createAccount,
            "SignIn": self.signIn
        }

        """
        Create Account : [username, password]
        SignIn : [username, password, clientPubKey] -> clientPubKey encoded with b64 then decoded to utf-8
        """

    def handlePost(self, data: str) -> (int, str):
        d: dict = json.loads(data)
        command = d['command']

        if command not in self.commands:
            print("returned command does not exist")
            return 400, str(Response("Command does not exist"))

        return self.commands[command](d['args'])

    def createAccount(self, args: dict) -> (int, str):
        try:
            if self.dbm.nameExists(args['username']):
                return 400, str(Response("Account creation error, Username already taken"))

            self.dbm.addAccount(args['username'], args['password'])
            print(f'created accouznt: {args["username"]}')

            return 200, str(Response("Success. Account created"))

        except Exception as e: # exception too broad but i will fix later
            #print(e)
            return 400, str(Response("Account creation error"))

    def signIn(self, args: dict) -> (int, str):
        try:
            if not self.dbm.validateAccount(args['username'], args['password']):
                print(f'Account sign in failure on: {args["username"]}')
                return 400, str(Response('Sign In error')) # make more specific later, username does not exist,
                                                           # password incorrect etc
            clientPubKey: str = args['clientPubKey']

            sessionAESKey: bytes
            encSessionAESKey: str
            sessionAESKey, encSessionAESKey = self.encryption.genSessionKeyAndEnc(clientPubKey)

            token: uuid = self.tm.generateToken(args['username'], sessionAESKey)
            cipher = self.encryption.encryptData(sessionAESKey, str(token))

            writtenResponse = 'Succes. Sign In complete'

            response = str(Response(writtenResponse=writtenResponse, token=cipher, sessionKey=encSessionAESKey))

            print(f'successful sign into {args["username"]}')
            return 200, response

        except Exception as e:
            #print(e)
            return 400, str(Response('Sign In error'))

"""
        response, m, uuid = self.rh.handlePost(body.decode("UTF-8"))
        resp = '{' + f'"writtenResponse": "{m}", "token": "{uuid}"' + '}' # bit of a hacky way to do this but running



change requesth handler todo

instead of returning the stuff we want to be formatted we do all formatting here so we can encrypt easier and only
have to return the string and can send direcrly from main

we want a response builder that has optional args and builds a decent response without needing loads of random stuff

"""
