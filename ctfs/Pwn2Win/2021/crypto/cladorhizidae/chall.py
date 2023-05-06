#!/usr/bin/python3

from uuid import uuid4
from cladorhizidae import hmac


def main():
    k = uuid4().bytes
    user_ID = uuid4().bytes

    token = hmac(k, user_ID)
    flag = open('flag.txt').read()
    print("This is a valid user_ID: ", user_ID.hex())
    print("This is the corresponding access token: ", token.hex())
    print("You can make up to 2^16 queries to forge a new token")

    i = 0

    while i<=2**16:
        u_ = bytes.fromhex(input())
        if len(u_) in range(4, 34, 2):
            t_ = hmac(k, u_)
            i+=1
            print(t_.hex())
        else:
            extra = uuid4().bytes + uuid4().bytes
            u_ = user_ID + extra
            t_ = hmac(k, u_)
            print("ok, now give'me the access token for: ", u_.hex())
            t_user = bytes.fromhex(input())
            if t_user == t_:
                print(flag)
                return()
            else:
                print('not quite right')
                return()

main()
