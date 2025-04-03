from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode

class Encryption:
    def __init__(self):
        self.key = RSA.generate(2048)                                 # our key for decrypting data from server
        self.clientPublicKey = self.key.publickey().export_key()      # our key to send to server to encrypt requests
        self.serverPublicKey = None                                   # our key for encrypting data for server

    def encryptForServer(self, data):
        if self.serverPublicKey is None:
            print('Cannot encrypt -> not yet recieved public key from server (this should never happen)')
            return

        RSACypherObj = PKCS1_OAEP.new(self.serverPublicKey)
        dataBytes = data.encode('utf-8')
        encData = RSACypherObj.encrypt(dataBytes)
        return encData

    def decryptFromServer(self, data):
        RSACypherObj = PKCS1_OAEP.new(self.key)
        decData = RSACypherObj.decrypt(data)
        return decData

    def exportData(self, data):
        b64encode(data).decode('utf-8')

    def registerServerPublicKeyFromB64String(self, s):
        decodedKey = b64decode(s.encode('utf-8'))
        #bytesKey = k.encode('utf-8')
        self.serverPublicKey = RSA.importKey(decodedKey)

    def exportClientPublicKeyForServer(self):
        return b64encode(self.clientPublicKey).decode('utf-8')

# we could be validating encrypted data but sending across aes keys and nonce etc will just take too much
# bandwidth and is ever so slightly overkill for the time being due to time constraints


if __name__ == '__main__':
    key = RSA.generate(2048)
    pubKey = b64encode(key.publickey().export_key()).decode('utf-8') #needed for sending w http requests

    encryp = Encryption()
    encryp.key = key
    encryp.registerServerPublicKeyFromB64String(pubKey)
    encrypted = encryp.encryptForServer('hi')
    print(b64encode(encrypted))

    decrypted = encryp.decryptFromServer(encrypted)
    print(decrypted)

"""
this works now so we essentially need the same in server

when we send login req we send the client pub key with it
once validated and have status code 200 we now decode every request with out priv key

"""