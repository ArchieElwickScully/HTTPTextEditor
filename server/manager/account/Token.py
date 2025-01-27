from time import time

class Token:
    def __init__(self, username, uid, t):
        self.username = username
        self.uid = uid
        self.time = t

    def isValid(self):
        elapsed = self.time - time()

        if elapsed > 86400:
            return False
        else:
            return True