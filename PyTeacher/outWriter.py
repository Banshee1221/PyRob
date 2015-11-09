import json


def dictFormatter(dictionary):
    """Formats the provided dictionary and writes it to file.

    :param dictionary: The dictionary containing all the user code to write out.
    :type dictionary: dict
    :returns: True if successfully wrote the file, False otherwise.

    """
    try:
        fileTmp = open("codeList.out", "w")
        fileTmp.write(json.dumps(dictionary))
        fileTmp.close()
    except:
        return False
    return True


def dictReader():
    """Reads the list of user operations from a file.

    :returns: The dictionary containing the user actions if successful, -1 otherwise.

    """
    fileTmp = open("codeList.out", "r")
    try:
        return json.loads(fileTmp.read().strip("\n"))
    except:
        return -1
