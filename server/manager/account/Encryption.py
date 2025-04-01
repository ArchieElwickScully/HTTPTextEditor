from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode

class Encryption:
    def __init__(self):
        pass

    @staticmethod
    def encryptForClient(self, clientPubKey, data):
        RSACypherObj = PKCS1_OAEP.new(self.serverPublicKey)
        dataBytes = data.encode('utf-8')
        encData = RSACypherObj.encrypt(dataBytes)
        return encData

    @staticmethod
    def decryptFromClient(self, data):
        RSACypherObj = PKCS1_OAEP.new(self.key)
        decData = RSACypherObj.decrypt(data)
        return decData

    @staticmethod
    def returnClientPublicKeyFromB64String(s):
        decodedKey = b64decode(s.encode('utf-8'))
        #bytesKey = k.encode('utf-8')
        return RSA.importKey(decodedKey)

    @staticmethod
    def exportClientPublicKeyForServer(self):
        return b64encode(self.clientPublicKey).decode('utf-8')

    @staticmethod
    def genUserKeys():
        k = RSA.generate(2048)
        public, private = (b64encode(k.export_key()).decode('utf-8'),
                           b64encode(k.public_key().export_key()).decode('utf-8'))
        return public, private


"""
each user will have an rsa private and public key in their class
stored as base64 encoded to utf-8
"""