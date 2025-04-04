import requests
import hashlib
import json

import multiprocessing

from client.Application.Manager.Encryption import Encryption


class RequestHandler(multiprocessing.Process):
    def __init__(self, queue, outQueue):
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
                task = self.queue.get()
                match task['type']:
                    case 'account':
                        self.doAccountRequest(task['data']['command'], task['data']['username'], task['data']['password'])
                    case _:
                        print(f'request handler error on {task}')

    def doAccountRequest(self, command, username, password):
        hashobj = hashlib.sha256(str.encode(password))
        password = hashobj.hexdigest()

        sendData = {'command': command,
                    "args": {'username': username, 'password': password,
                             'clientPubKey': self.encryption.exportClientPublicKeyForServer()}}

        r = requests.post(self.server, json=sendData)

        response = json.loads(r.text)
        textResponse = response['writtenResponse']

        if 'encrypted' in response.keys():
            encToken = response['encrypted']['token']
            serverPubKey = response['encrypted']['serverPublicKey']

            self.encryption.importSeverPublicKey(serverPubKey)
            print(self.encryption.decryptFromServer(encToken))

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