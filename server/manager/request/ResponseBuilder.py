import json


class Response:
    def __init__(self, writtenResponse, token=None, serverPubKey=None):
        self.template = {
            'token': token,
            'serverPublicKey': serverPubKey
        }

        self.response = {
            'writtenResponse': writtenResponse,
        }

        self.encrypted = self.getDict()
        if len(self.encrypted) > 0:
            self.response['encrypted'] = self.encrypted


    def getDict(self):
        d = {}

        for key in self.template:
            if self.template[key] is not None:
                d[key] = self.template[key]

        return d

    def __str__(self):
        return json.dumps(self.response)

"""

request structure:

data = {
    'writtenResponse': writtenResponse,
        'encrypted': {
            'token': encToken,
            'serverPublicKey': encPubKey
        }
    }

is it better to create skeleton sort of dictionary then purge keys with non values
or loop params and add if not none

"""