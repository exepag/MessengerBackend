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


class AnnotationModel:
    def __init__(self):
        self.name = ""
        self.xmin = 0
        self.ymin = 0
        self.xmax = 0
        self.ymax = 0

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

class nasabahVerified:
    def __init__(self):
        self.permit = False
        self.email = ''
        self.nama = ''
        self.token = ''

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
