import json

class ResponseTemplate:
    def __init__(self):
        self.status = "Failed"
        self.code = 500
        self.data = {}
        self.message = ""
        self.pagination = {}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

class UserVerified:
    def __init__(self):
        self.permit = False
        self.id = ''
        self.email = ''
        self.nama = ''
        self.token = ''

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)



#Ini buat nampung respons nya Rest API agar message nya rapi.
