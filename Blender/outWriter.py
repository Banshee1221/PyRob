import json

class FileWriter:

    def __init__(self):
        pass

    @staticmethod
    def dictFormatter(dictionary):
        return json.dumps(dictionary)

