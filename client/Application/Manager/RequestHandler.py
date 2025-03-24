import requests
import hashlib
import json


class RequestHandler:
    def __init__(self):
        self.server = "http://localhost:8000/"

    def doAccountRequest(self, type, username, password):
        hashobj = hashlib.sha256(str.encode(password))
        password = hashobj.hexdigest()

        sendData = {'command': type,
                    "args": {'username': username, 'password': password}}

        r = requests.post(self.server, json=sendData)

        response = json.loads(r.text)
        textResponse = response['writtenResponse']
        token = response['token']

        return textResponse, token
