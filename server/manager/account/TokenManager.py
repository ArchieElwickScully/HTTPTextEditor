import math
import uuid

from server.manager.account.Token import Token
from time import time


class TokenManager:
    def __init__(self):
        self.activetokens: list[Token] = []

    def generateToken(self, username: str, SessionAESKey: bytes) -> uuid:
        uid: uuid = uuid.uuid4()
        currentTime = math.trunc(time())

        active: Token = self.findTokenByUsername(username)

        if active is not None:
            self.removeToken(active)

        token = Token(
            username = username,
            uid = uid,
            time = currentTime,
            SessionAESKey = SessionAESKey
        )

        self.addToken(token)

        return uid

    def validateToken(self, uid: uuid):
        token: Token = self.findTokenByUID(uid)

        if token is None:
            return False

        if token.isValid():
            return True
        else:
            self.removeToken(token)
            return False

    def findTokenByUsername(self, username: str) -> Token | None:
        for token in self.activetokens:
            if token.username == username:
                return token

        return None

    def findTokenByUID(self, uid: uuid) -> Token | None:
        for token in self.activetokens:
            if token.uid == uid:
                return token

        return None

    def addToken(self, token: Token):
        self.activetokens.append(token)

    def removeToken(self, token: Token):
        self.activetokens.remove(token)
