import json


def dictFormatter(dictionary):
        fileTmp = open("codeList.out", "w")
        fileTmp.write(json.dumps(dictionary))
        fileTmp.close()

def dictReader():
    fileTmp = open("codeList.out", "r")
    try:
        return json.loads(fileTmp.read().strip("\n"))
    except:
        return -1

