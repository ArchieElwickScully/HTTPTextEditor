from server.manager.account.Token import Token

from uuid import uuid4
from time import time


class TokenManager:
    def __init__(self):
        self.activetokens = []

    def generateToken(self, username):
        uid = uuid4()
        t = time()

        active = self.findTokenByUsername(username)

        if active is not None:
            self.removeToken(active)

        token = Token(username, uid, t)
        self.addToken(token)

        return uid

    def validateToken(self, uid):
        token = self.findTokenByUID(uid)

        if token is None:
            return False

        if token.isValid():
            return True
        else:
            self.removeToken(token)
            return False

    def findTokenByUsername(self, username):
        for t in self.activetokens:
            if t.username == username:
                return t

        return None

    def findTokenByUID(self, uid):
        for t in self.activetokens:
            if t.uid == uid:
                return t
        return None

    def addToken(self, token):
        self.activetokens.append(token)

    def removeToken(self, token):
        self.activetokens.remove(token)
