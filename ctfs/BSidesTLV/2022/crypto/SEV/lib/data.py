from base64 import b64encode, b64decode

def JoinData(*data : bytes):
    return b'|'.join(b64encode(d) for d in data)


def SplitData(data : bytes):
    return tuple(b64decode(x) for x in data.split(b'|'))
