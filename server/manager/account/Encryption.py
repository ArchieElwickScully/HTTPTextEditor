from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from base64 import b64encode, b64decode

class Encryption:
    def __init__(self):
        pass

    def encryptForClient(self, clientPubKey, data):
        key = self.returnKeyFromb64String(clientPubKey)

        RSACypherObj = PKCS1_OAEP.new(key)
        dataBytes = data.encode('utf-8')
        encData = RSACypherObj.encrypt(dataBytes)
        return encData

    def decryptFromClient(self, userPrivateKey ,data):
        key = self.returnKeyFromb64String(userPrivateKey)

        RSACypherObj = PKCS1_OAEP.new(key)
        decData = RSACypherObj.decrypt(data)
        return decData

    def returnKeyFromb64String(self, s):
        decodedKey = b64decode(s.encode('utf-8'))
        #bytesKey = k.encode('utf-8')
        return RSA.importKey(decodedKey)

    def returnDataFromb64String(self, dat):
        return b64decode(dat.encode('utf-8'))

    def exportForTransmission(self, key):
        return b64encode(key).decode('utf-8')

    def genUserKeys(self):
        k = RSA.generate(2048)
        public, private = (b64encode(k.export_key()).decode('utf-8'),
                           b64encode(k.public_key().export_key()).decode('utf-8'))
        return public, private


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