import multiprocessing

import requests
import hashlib
import json


class RequestHandler(multiprocessing.Process):
    def __init__(self, queue):
        super().__init__()
        self.token = ''

        self.queue = queue
        self.server = "http://localhost:8000/"

    def run(self):
        while True:

            while not self.queue.Empty:
                task = self.queue.get()

                match task['type']:
                    case 'account':
                        self.doAccountRequest(task['command'], task['username'], task['password'])
                    case _:
                        print(f'request handler error on {task}')

    def doAccountRequest(self, command, username, password):
        hashobj = hashlib.sha256(str.encode(password))
        password = hashobj.hexdigest()

        sendData = {'command': command,
                    "args": {'username': username, 'password': password}}

        r = requests.post(self.server, json=sendData)

        response = json.loads(r.text)
        textResponse = response['writtenResponse']
        token = response['token']

        return textResponse, token

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