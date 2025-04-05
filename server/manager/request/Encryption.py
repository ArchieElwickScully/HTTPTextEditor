from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode

from Crypto.Random import get_random_bytes


class Encryption:
    def __init__(self):
        pass

    @staticmethod
    def encryptData(sessionKey: bytes, data: str) -> (str, str, str):
        data: bytes = data.encode('utf-8')

        AESCipher = AES.new(sessionKey, AES.MODE_EAX)
        ciphertext, tag = AESCipher.encrypt_and_digest(data)

        return (
            Encryption.exportData(ciphertext),                        # export aes nonce, ciphertext and tag
            Encryption.exportData(AESCipher.nonce),                   # could look more prettier by having exp
            Encryption.exportData(tag)                                # take more optional args but its good
        )

    @staticmethod
    def decryptFromClient(userPrivateKey: str, data: str) -> str:
        key = Encryption.importKey(userPrivateKey)
        data: bytes = Encryption.importData(data)

        RSACypherObj = PKCS1_OAEP.new(key)
        decData = RSACypherObj.decrypt(data)
        return decData.decode('utf-8')

    @staticmethod
    def genSessionKeyAndEnc(clientpublicKey: str) -> (bytes, str):
        clientRSAKey = Encryption.importKey(clientpublicKey)    # import client rsa key
        AESKey: bytes = get_random_bytes(16)

        RSACypherObj = PKCS1_OAEP.new(clientRSAKey)             # new rsa obj to encrypt aes key
        encKey = RSACypherObj.encrypt(AESKey)                   # encrypting aes key so we can
        return AESKey, Encryption.exportData(encKey)            # returning both keys to add normal one to token class

    @staticmethod
    def importKey(s: str):
        decodedKey: bytes = Encryption.importData(s)
        return RSA.import_key(decodedKey)

    @staticmethod
    def importData(data: str) -> bytes:
        return b64decode(data.encode('utf-8'))

    @staticmethod
    def exportData(data: bytes) -> str:
        return b64encode(data).decode('utf-8')

    '''
    depreciated methods incase need for future ref
    
    @staticmethod
    def RSAencryptForClient(clientPubKey, data):
        key = Encryption.importKey(clientPubKey)
        data = data.encode('utf-8')

        RSACypherObj = PKCS1_OAEP.new(key)
        encData = RSACypherObj.encrypt(data)
        return Encryption.exportData(encData)

    '''

if __name__ == '__main__':
    e = Encryption()
    AESKey = get_random_bytes(16)

    dat = 'hello'

    print(e.encryptData(sessionKey = AESKey, data = dat))

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