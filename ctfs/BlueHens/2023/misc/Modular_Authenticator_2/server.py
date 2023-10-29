import random
import json
import logging
import os
pid = os.getpid()

logging.basicConfig(filename="auth.log",level=logging.INFO,format=f"{pid}:%(message)s")

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

def authenticate(rounds, ssq, e, N):
    logging.info("Client connected, beginning authentication.")
    squares = get_inputs(rounds,2,N-2)
    logging.info(f"got initial randoms")
    requests = RAND.choices(("r","rs"),k=rounds)
    logging.info(f"Sent challenges")
    print(json.dumps(requests))
    responses = get_inputs(rounds,2,N-2)
    for expected, response, rsq in zip(requests,responses,squares):
        logging.info(f"challenge: {expected}, response: {response}, initial: {rsq}")
        if expected == "r" and pow(response,e,N) != rsq:
            logging.warning(f"{response}**{e} != {rsq}")
            raise AuthenticationException(f"{response}**{e} != {rsq}")
        elif expected == "rs" and pow(response,e,N) != ((rsq * ssq) % N):
            logging.warning(f"{response}**{e} != {rsq}*{ssq}")
            raise AuthenticationException(f"{response}**{e} != {rsq}*{ssq}")
        logging.info("round passed.")
if __name__ == "__main__":
    ROUNDS = 128
    
    with open("public_key.json",'r') as f:
        public_key=json.loads(f.read())

    N = public_key["N"]
    ssq = public_key["s^2"]
    e = public_key['e']
    
    authenticate(ROUNDS,ssq,e,N)
    print("Authentication successful.")

    with open("flag.txt",'r') as f:
        print(f.read())

    