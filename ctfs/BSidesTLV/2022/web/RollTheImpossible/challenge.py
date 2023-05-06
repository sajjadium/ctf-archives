from flask import session
import flag
import random

CTX_FIELDS = ["question", "num"]
NUM_DIGITS = 10
FISH_IN_SEA = 3500000000000 # thanks wikipedia

QUESTIONS_LIST = {"roll a negative number": lambda num: int(num) < 0,
        "roll a number that is divisable by 10": lambda num: int(num) % 10 == 0,
        "roll a number that contains only ones": lambda num: all(x == "1" for x in num),
        "roll the number of fish in the sea": lambda num: int(num) == random.randrange(FISH_IN_SEA),
        "misdirection": lambda num: True}

def is_context_exist():
    return all(key in session for key in CTX_FIELDS)

def init():
    question = random.choice(list(QUESTIONS_LIST.keys())[:-1])

    # init context, must contain all the fields in CTX_FIELDS
    session["question"] = question
    session["num"] = ""

def step():
    if not is_context_exist():
        return {"num": "", "new_digit": "", "flag": "invalid session data"}
    # load data from the session
    question = session["question"]
    num = session["num"]

    _flag = ""
    new_digit = ""
    if len(num) < NUM_DIGITS:
        # roll a new digit and update the number
        new_digit = str(random.randrange(9)+1)
        num += new_digit
    if len(num) == NUM_DIGITS:
        if QUESTIONS_LIST[question](num):
            _flag = flag.FLAG
        else:
            _flag = "wrong :("

    # store the changed data to the session
    session["num"] = num
    return {"num": num,
            "new_digit": new_digit,
            "flag": _flag}
