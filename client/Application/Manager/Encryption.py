from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey.RSA import RsaKey
from Crypto.PublicKey import RSA

from base64 import b64encode, b64decode



class Encryption:
    def __init__(self):
        self.RSAkey: RsaKey = RSA.generate(2048)                                 # our key for decrypting data from server
        self.clientPublicKey: bytes = self.RSAkey.publickey().export_key()      # our key to send to server to encrypt requests
        self.sessionKey = None                                           # AES session key from server

    def decrypt(self, cipher: tuple[str, str, str]) -> str:
        ciphertext, nonce, tag = cipher
        ciphertext, nonce, tag = (
            Encryption.importData(ciphertext),
            Encryption.importData(nonce),
            Encryption.importData(tag)
        )

        cipher_aes = AES.new(self.sessionKey, AES.MODE_EAX, nonce)
        decData: bytes = cipher_aes.decrypt_and_verify(ciphertext, tag)

        return decData.decode('utf-8')

    def importSessionKey(self, k: str):
        k: bytes = Encryption.importData(k)

        RSACypherObj = PKCS1_OAEP.new(self.RSAkey)                     # new RSA obj to decrypt the AES session key
        decKey: bytes = RSACypherObj.decrypt(k)
        self.sessionKey = decKey                                       # im actually not sure if i should be storing
                                                                       # this as bytes or storing an aes cipher obj
    def exportClientPublicKeyForServer(self) -> str:
        return Encryption.exportData(self.clientPublicKey)

    @staticmethod
    def exportData(data: bytes) -> str:
        return b64encode(data).decode('utf-8')

    @staticmethod
    def importData(data: str) -> bytes:
        return b64decode(data.encode('utf-8'))

    '''
    depreciated functions incase future ref needed
    
    def encryptForServer(self, data):
        if self.serverPublicKey is None:
            print('Cannot encrypt -> not yet recieved public key from server (this should never happen)')
            return

        dataBytes = data.encode('utf-8')

        RSACypherObj = PKCS1_OAEP.new(self.serverPublicKey)
        encData = RSACypherObj.encrypt(dataBytes)
        return Encryption.exportData(encData)
        
    def decryptFromServer(self, data):
        data = Encryption.importData(data)

        RSACypherObj = PKCS1_OAEP.new(self.RSAkey)
        decData = RSACypherObj.decrypt(data)
        return decData

'''

# we could be validating encrypted data but sending across aes keys and nonce etc will just take too much
# bandwidth and is ever so slightly overkill for the time being due to time constraints


if __name__ == '__main__':
    # test
    key = RSA.generate(2048)
    pubKey = b64encode(key.publickey().export_key()).decode('utf-8') #needed for sending w http requests

    encryp = Encryption()
    encryp.key = key
    encryp.importSeverPublicKey(pubKey)
    encrypted = encryp.encryptForServer('hi')
    print(encrypted)

    decrypted = encryp.decryptFromServer(encrypted)
    print(decrypted)

"""
this works now so we essentially need the same in server

when we send login req we send the client pub key with it
once validated and have status code 200 we now decode every request with out priv key


this now works but rsa sucks for taking large amount of time so is best to create an aes key, encrypt that both ways
with rsa, send it over and use that for encryption

firstly

clientside
    create public rsa key
    send it over to server
    simple hopefully
    
serverside
    recieve client public rsa key
    create aes key
        store in token
    encrypt aes key
    send back to client and client will register it to the encryption class for future use
    

"""