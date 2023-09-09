#!/usr/bin/env python3
from mlmodel import endpoint

WARNING = '\033[93m'
ERROR = '\033[91m'
END = '\033[0m'

if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        classification = endpoint.classify_local(user_input)
        if len(classification) == 0:
            print(f"{WARNING}Cannot verify...{END}")
            continue
        intent = dict(classification[0]).get('intent')
        if intent == None: continue
        try:
            if intent == 'good_code':
                exec(user_input)
            else:
                print(f"{ERROR}Bad Code Detected...{END}")
        except Exception as e:
            print(f"Oops, something broke: \n{ERROR}{e}{END}")
            pass
