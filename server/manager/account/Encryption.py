from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode

class Encryption:
    def __init__(self):
        pass

    @staticmethod
    def encryptForClient(clientPubKey, data):
        key = Encryption.importKey(clientPubKey)
        data = Encryption.importData(data)

        RSACypherObj = PKCS1_OAEP.new(key)
        encData = RSACypherObj.encrypt(data)
        return Encryption.exportData(encData)

    @staticmethod
    def decryptFromClient(userPrivateKey ,data):
        key = Encryption.importKey(userPrivateKey)
        data = Encryption.importData(data)

        RSACypherObj = PKCS1_OAEP.new(key)
        decData = RSACypherObj.decrypt(data)
        return decData.decode('utf-8')

    @staticmethod
    def genUserKeys():
        k = RSA.generate(2048)
        public, private = (Encryption.exportData(k.export_key()),
                           Encryption.exportData(k.public_key().export_key()))
        return public, private

    @staticmethod
    def importKey(s):
        decodedKey = Encryption.importData(s)
        return RSA.importKey(decodedKey)

    @staticmethod
    def importData(data):
        return b64decode(data.encode('utf-8'))

    @staticmethod
    def exportData(data):
        return b64encode(data).decode('utf-8')


"""
e = Encryption()

enc = e.encryptForClient('LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF6UTdQUFdNeWZUUVVOMU1JaE14awpjK1BRQ1Vwem9RajVFUlQvb2ZoUlZOTW1QaTdtWkdaNGVnR3UrRW9uSjZaVi9jelFIQWhoeHZ2dmVOK1JEVUwzCjBvMFg5V0xiZ29NeDJWUXNsTHFJTG9ZTWpwaGVNWWN2TXBoa2Z1U050MElHeDV1YkoxOXZNK3p5STJrbFhHM1EKOFBZeXVFWUJNbElOMEVlVVgwaHZKRVdnN05USlh5OUxISzFyME1VSzBuVk1jYms0aGgyTzVYQXhPbW1hKzFyKwpzemFBcmRqOHRnbTZocm1ja05DWDJUc2lQL3VSaXc3MmgydTVjcVg5c04yTFRkZkRIVHhncGZKSjIwQWd2ZEpQCmFyemUvNXJFNjNmUkhSNFp2SVd3STBKdjFpVGdKTGUwb0ZSZTVmMXZnSkJ3Y2JFbE9FdWRJTHNIYzlrSG44UUgKUHdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t',
                   'hi')
print(enc)
enc = e.exportForTransmission(enc)
print(enc)

dec = e.returnDataFromb64String(enc)
print(dec)
"""

"""
each user will have an rsa private and public key in their class
stored as base64 encoded to utf-8
"""