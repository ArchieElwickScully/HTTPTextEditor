import requests
import hashlib
import json

from multiprocessing import Process, Queue

from client.Application.Manager.Encryption import Encryption


class RequestHandler(Process):
    def __init__(self, queue: Queue, outQueue: Queue):
        super().__init__()

        self.encryption = None # fixes pickling error
        self.token = ''

        self.queue = queue
        self.outQueue = outQueue
        self.server = "http://localhost:8000/"


    def run(self):
        self.encryption = Encryption()

        while True:
            while not self.queue.empty():
                task: dict = self.queue.get()

                match task['type']:
                    case 'account':
                        self.doAccountRequest(
                            task['data']['command'],
                            task['data']['username'], task['data']['password']
                        )

                    case _:
                        print(f'request handler error on {task}')

    def doAccountRequest(self, command: str, username: str, password: str):
        hashobj: hash = hashlib.sha256(str.encode(password))
        password = hashobj.hexdigest()

        sendData = {
            'command': command,
            "args": {
                'username': username, 'password': password,
                'clientPubKey': self.encryption.exportClientPublicKeyForServer()
            }
        }

        r = requests.post(self.server, json=sendData)

        response: dict = json.loads(r.text)
        textResponse: str = response['writtenResponse']

        if 'encrypted' in response.keys():
            tokenCipher: tuple[str, str, str] = response['encrypted']['token']
            sessionKey: str = response['encrypted']['sessionKey']

            self.encryption.importSessionKey(sessionKey)
            print(self.encryption.decrypt(tokenCipher))

        self.outQueue.put((textResponse, False))

'''
each task will have a command

account or something else

example
{
type: account,
    data: {
        command: create,
        username: uname,
        password: pword
    }
}

{
type: loadToken,
token: token
}

'''