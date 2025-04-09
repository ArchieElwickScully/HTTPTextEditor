import requests
import hashlib
import json

from multiprocessing import Process, Queue

from client.Application.Manager.Encryption import Encryption


class RequestHandler(Process):
    def __init__(self, queue: Queue, outQueue: Queue):
        super().__init__()

        self.SERVER = "http://localhost:8000/"

        self.encryption = None # fixes pickling error
        self.token = ''

        self.queue = queue
        self.outQueue = outQueue


    def run(self):                          # this is called when the class is instantiated and started as new process
        self.encryption = Encryption()      # instantiating the Encryption class to handle encryption of data
                                            # it is only instantiated here insteaf of in the init method as having it
        while True:                         # defined there was creating a pickling error which im still not sure why
            self.checkQueue()               # but i assume it has something to do with certain classes or objects not
                                            # being hashable?
    def checkQueue(self):
        if self.queue.empty():
            return

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

        r = requests.post(self.SERVER, json=sendData)

        response: dict = json.loads(r.text)
        textResponse: str = response['writtenResponse']

        if 'encrypted' in response.keys():
            tokenCipher: tuple[str, str, str] = response['encrypted']['token']      # currently no handling for tokens
            sessionKey: str = response['encrypted']['sessionKey']                   # as ran out of time but they are
                                                                                    # received perfectly fine
            self.encryption.importSessionKey(sessionKey)
            print(self.encryption.decrypt(tokenCipher))

        self.outQueue.put((textResponse, False))                                    # just sending to output queue to
                                                                                    # be displayed

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