import random
import json
import os
pid = os.getpid()

RAND = random.SystemRandom()

class InvalidInputException(Exception):
    pass

class AuthenticationException(Exception):
    pass


def get_inputs(cnt, lower_bound, upper_bound):
    try:
        data = json.loads(input())
    except json.JSONDecodeError as J:
        raise InvalidInputException("Invalid JSON") from J
    if not isinstance(data, list) or len(data) != cnt:
        raise InvalidInputException(f"Invalid response. Expected list of length {cnt}.")
    for item in data:
        if not isinstance(item,int):
            raise InvalidInputException(f"Invalid response: {item} is not an integer.")
        elif item < lower_bound or item > upper_bound:
            raise InvalidInputException(f"Invalid response: {item} is not in the interval [{lower_bound},{upper_bound}]")
    return data

def authenticate(rounds, ssq, e, p):
    squares = get_inputs(rounds,2,p-2)
    requests = RAND.choices(("r","rs"),k=rounds)
    print(json.dumps(requests))
    responses = get_inputs(rounds,2,p-2)
    for expected, response, rsq in zip(requests,responses,squares):
        if expected == "r" and pow(response,e,p) != rsq:
            raise AuthenticationException(f"{response}**{e} != {rsq}")
        elif expected == "rs" and pow(response,e,p) != ((rsq * ssq) % p):
            raise AuthenticationException(f"{response}**{e} != {rsq}*{ssq}")

if __name__ == "__main__":
    ROUNDS = 128
    
    with open("public_key.json",'r') as f:
        public_key=json.loads(f.read())

    with open("flag.txt",'r') as f:
        flag = f.read()

    p = public_key["p"]
    ssq = public_key["s^e"]
    e = public_key['e']
    
    authenticate(ROUNDS,ssq,e,p)
    print(flag)

    