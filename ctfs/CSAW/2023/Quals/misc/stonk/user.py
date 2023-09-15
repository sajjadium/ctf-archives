import requests
import json

ADDRESS = "http://127.0.0.1"
PORT = 8000

print(\
"""Thank you for choosing City Subway Auction Website (CSAW)'s Trading Platform
As a thank you for using our platform, all new registrants will be granted $2000
and the flags are on sale for $9001 dollars. Have fun trading!

Here are the options:

Login and register with ID

1. List Account Status
2. Buy Stocks
3. Sell Stocks
4. Trade Stocks
5. Buy flags at $9001


""")

def inp() -> str:
    print(">", end="")
    return input()

def sendGET(subpath) -> str:
    try:
        response = requests.get(ADDRESS + ":" + str(PORT) + subpath)
        response.raise_for_status()  # Raises an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def sendPOST(subpath, data) -> str:
    url = ADDRESS + ":" + str(PORT) + subpath
    payload = data

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raises an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def buyStock(key, str):
    body = sendPOST("/buy", {"key":key, "stock": str})
    return body

def sellStock(key, str):
    body = sendPOST("/sell", {"key":key, "stock": str})
    return body

def tradeStock(key, str, str1):
    body = sendPOST("/trade", {"key":key, "stock": str, "stock1": str1})
    return body

def listCalls() -> str:
    body = sendGET("/listCalls")
    out = json.loads(body)
    return "\n".join((str(i["name"]) + " at " + str(i["price"]) for i in out.values()))

def flag(key) -> str:
    body = sendPOST("/flag", {"key":key})
    return body

def status(key) -> str:
    body = sendPOST("/login", {"key":key})
    return body

print(listCalls())

print()

print("Please login")
key = inp()

while True:
    stat = status(key)
    print(stat)
    stat = json.loads(stat)
    print("You have", stat['balance'], "dollars\n")
    print('''"1". List Account Status
"2 STOCKID". Buy Stocks
"3 STOCKID". Sell Stocks
"4 STOCKID STOCKID2". Trade Stocks
"5". Buy flags at $9001''')
    opt = inp().strip().split(" ")
    if not opt:
        continue
    if opt[0][0] == '1':
        continue
    elif opt[0][0] == '2' and len(opt) > 1:
        print(buyStock(key, opt[1]))
    elif opt[0][0] == '3' and len(opt) > 1:
        print(sellStock(key, opt[1]))
    elif opt[0][0] == '4' and len(opt) > 2:
        print(tradeStock(key, opt[1], opt[2]))
    elif opt[0][0] == '5':
        print(flag(key, ))



status(key)


