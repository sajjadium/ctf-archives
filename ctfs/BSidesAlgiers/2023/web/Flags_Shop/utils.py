import hashlib
import json
import re


DEFAULT_BALANCE = 10


def getUsers():
    with open("users.json", "r") as file:
        return json.load(file)


def getBalance(username):
    usres = getUsers()
    try:
        return usres[username]["balance"]
    except:
        return 0

def addUser(username, password):
    users = getUsers()
    if username in users:
        return False
    
    users[username] = {"password":hash(password), "balance":DEFAULT_BALANCE, "redeemed":False}
    updateUsers(users)
    return True

def hash(password):
    return hashlib.sha1(password.encode()).hexdigest()

def generateTicket(username):
    return "%s-[0-9A-F]{4}$"%username

def checkTicket(regex, ticket):
    return re.match(regex, ticket)

def checkUser(username, password):
    users = getUsers()
    return username in users and users[username]["password"] == hash(password)

def checkBalance(username, price):
    users = getUsers()
    return username in users and users[username]["balance"] >= price

def updateBalance(username, amount):
    users = getUsers()
    users[username]["balance"]-=amount
    updateUsers(users)

def checkRedeem(username):
    users = getUsers()
    return username in users and not users[username]["redeemed"]

def userRedeem(username):
    users = getUsers()
    users[username]["redeemed"] = True
    users[username]["balance"] += 10
    updateUsers(users)

def updateUsers(users):
    with open("users.json", "w") as file:
        json.dump(users, file)