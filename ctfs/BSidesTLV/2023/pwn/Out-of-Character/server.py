#!/usr/bin/python3

from dataclasses import dataclass
from enum import Enum
import pathlib
import io
import sys
import random

DB_USERS = pathlib.Path(r"/tmp/users.db")
DB_SECRETS = pathlib.Path(r"/tmp/secrets.db")
MAX_SECRET_LEN = 128
MAX_USERNAME_LEN = 32


class UserType(Enum):
    MEMBER = "m"
    GUEST = "g"


MEMBERSHIP = None


def str_membership(membership: UserType):
    return "MEMBER" if membership == UserType.MEMBER else "GUEST"


def read(_io: io.StringIO, length: int):
    value = _io.read(length)
    return value


def eof(_io: io.StringIO):
    pos = _io.tell()
    is_eof = _io.read(1) == ""
    _io.seek(pos, io.SEEK_SET)
    return is_eof


@dataclass
class User:
    name: str
    type_: UserType

    def serialize(self, _io: io.StringIO):
        length = chr(len(self.name))
        name = self.name.lower()
        _type = self.type_.value

        return _io.write(length + name + _type)

    @classmethod
    def deserialize(cls, _io: io.StringIO):
        try:
            length = ord(read(_io, 1))
            name = read(_io, length)
            _type = UserType(read(_io, 1))
        except ValueError:
            print("ERROR: Could not read user values.")
            return

        return cls(name, _type)


@dataclass
class Secret:
    type_: UserType
    secret: str

    def serialize(self, _io: io.StringIO):
        _type = self.type_.value
        length = chr(len(self.secret))
        secret = self.secret

        return _io.write(_type + length + secret)

    @classmethod
    def deserialize(cls, _io: io.StringIO):
        try:
            _type = UserType(read(_io, 1))
            length = ord(read(_io, 1))
            secret = read(_io, length)
        except ValueError:
            print("ERROR: Could not read secret values.")
            return

        return cls(_type, secret)


def add_secret(secret: str):
    global MEMBERSHIP

    if not MEMBERSHIP:
        print("FAILED: Please login to read secrets.")
        return

    if len(secret) > MAX_SECRET_LEN:
        print("ERROR: Secret exceeds max length ({} characters).".format(MAX_SECRET_LEN))
        return

    try:
        with DB_SECRETS.open("a") as f:
            Secret(MEMBERSHIP, secret).serialize(f)
            print("Secret \"{}\" was successfully added.".format(secret))
    except FileNotFoundError:
        print("ERROR: Secrets database does not exist.")


def read_secret(idx: str):
    global MEMBERSHIP
    try:
        if not MEMBERSHIP:
            print("FAILED: Please login to read secrets.")
            return

        with DB_SECRETS.open("r") as f:
            idx = int(idx)
            i = 0
            while not eof(f) and i <= idx:
                sec = Secret.deserialize(f)
                i += 1
            if idx < 0 or idx >= i:
                print("ERROR: index out of bounds.")
            elif sec.type_ == UserType.MEMBER:
                if MEMBERSHIP == UserType.MEMBER:
                    print("Secret #{} is \"{}\"".format(idx, sec.secret))
                else:
                    print("FAILED: Only members allowed to read members' secrets!")
            elif sec.type_ == UserType.GUEST:
                print("Secret #{} is \"{}\"".format(idx, sec.secret))

    except FileNotFoundError:
        print("ERROR: Secrets database does not exist.")
    except ValueError:
        print("ERROR: Invalid secret index.")


def login(name: str):
    global MEMBERSHIP

    try:
        with DB_USERS.open("r") as f:
            while not eof(f):
                user = User.deserialize(f)
                if user.name == name.lower():
                    MEMBERSHIP = user.type_
                    print("{} logged in successfully as a {}.".format(user.name, str_membership(user.type_)))
                    return
    except FileNotFoundError:
        pass
    except AttributeError:
        print("ERROR: Failed to log in")

    print("FAILED: Member not found.")


def is_user_exists(name: str):
    try:
        with DB_USERS.open("r") as f:
            while not eof(f):
                user = User.deserialize(f)
                if user.name == name.lower():
                    return True
    except AttributeError:
        print("ERROR: Something went wrong...")
    except FileNotFoundError:
        pass

    return False


def add_member(name: str):
    if len(name) > MAX_USERNAME_LEN:
        print("ERROR: Username exceeds max length ({} characters).".format(MAX_USERNAME_LEN))
        return

    token = input("Enter a valid member token to get a membership: ")
    if token != random.getrandbits(256):
        print("ERROR: Invalid token.")
        return

    if is_user_exists(name):
        print("ERROR: User \"{}\" already exists.".format(name))
        return

    try:
        with DB_USERS.open("a") as f:
            User(name, UserType.MEMBER).serialize(f)
            print("Member \"{}\" was successfully added.".format(name))
    except FileNotFoundError:
        print("ERROR: Users database does not exist.")


def add_guest(name: str):
    if len(name) > MAX_USERNAME_LEN:
        print("ERROR: Username exceeds max length ({} characters).".format(MAX_USERNAME_LEN))
        return

    if is_user_exists(name):
        print("FAILED: User \"{}\" already exists.".format(name))
        return

    try:
        with DB_USERS.open("a") as f:
            User(name, UserType.GUEST).serialize(f)
            print("Guest \"{}\" was successfully added.".format(name))
    except FileNotFoundError:
        print("ERROR: Users database does not exist.")


def list_users():
    try:
        with DB_USERS.open("r") as f:
            while not eof(f):
                user = User.deserialize(f)
                print(user.name, str_membership(user.type_))
    except FileNotFoundError:
        print("ERROR: Users database does not exist.")
    except AttributeError:
        print("ERROR: Something went wrong...")


def main():
    print("Welcome to the secrets safe!")

    while True:
        print("\nSelect your choice:")
        print("1. Login")
        print("2. Add a member account")
        print("3. Add a guest account")
        print("4. Add a secret")
        print("5. Read a secret")
        print("6. Print users list")
        print("0. Exit")

        choice = input("\n>> ")

        if choice == "0":
            print("Good Bye!")
            exit(0)
        elif choice == "1":
            name = input("Enter your name: ")
            login(name)
        elif choice == "2":
            name = input("Enter your name: ")
            add_member(name)
        elif choice == "3":
            name = input("Enter your name: ")
            add_guest(name)
        elif choice == "4":
            secret = input("Enter a secret to store: ")
            add_secret(secret)
        elif choice == "5":
            secret = input("Select secret index: ")
            read_secret(secret)
        elif choice == "6":
            list_users()
        else:
            print("Invalid choice")


if __name__ == '__main__':
    main()
