from collections import defaultdict
from enum import Enum
from collections import deque
from time import sleep

COMPANIES = {


    "AAPLISH": {
        "name": "AAPLISH Inc.",
        "price": 175.42
    },
    "AMAZING": {
        "name": "AMAZING Enterprises",
        "price": 194.87
    },
    "FACEFLOP": {
        "name": "FACEFLOP Innovations",
        "price": 132.15
    },
    "GOOBER": {
        "name": "GOOBER Technologies",
        "price": 119.63
    },
    "SPOTLITE": {
        "name": "SPOTLITE Systems",
        "price": 156.28
    },
    "ELONX": {
        "name": "ELONX Ventures",
        "price": 205.75
    },
    "CRUISEBOOK": {
        "name": "CRUISEBOOK Ltd.",
        "price": 186.94
    },
    "SNAPSTAR": {
        "name": "SNAPSTAR Innovations",
        "price": 142.09
    },
    "TWEETIFY": {
        "name": "TWEETIFY Solutions",
        "price": 121.36
    },
    "ZUCKTECH": {
        "name": "ZUCKTECH Industries",
        "price": 179.53
    },
    "BURPSHARKHAT": {
        "name": "BURPSHARKHAT Holdings",
        "price": 1723.44
    },
    "BROOKING": {
        "name": "BROOKING Holdings",
        "price": 1522.33
    }
}

QUEUE = deque()

TRADEPOST = deque()

class ACTION(Enum):
    BUY = 1
    SELL = 2
    TRADE = 3
    FLAG = 4

class Portfolio:
    def __init__(self, key) -> None:
        self.key = key
        self.balance = 2000.00
        self.portfolio = defaultdict(int)
        self.requests = 0

    def bkup(key, portfolio, balance, requests):
        ret = Portfolio(key)
        ret.key = key
        ret.balance = balance
        ret.requests = requests
        ret.portfolio = portfolio.copy()
        return ret

    def status(self) -> dict:
        return {
            "balance": self.balance,
            **self.portfolio
        }

class DB:
    def __init__(self) -> None:
        self.dict = dict()
        self.log = list()

    def getUser(self, key) -> Portfolio:
        if key not in self.dict:
            self.dict[key] = Portfolio(key)
        return self.dict[key]

    def getUsers(self):
        return self.dict.values()

    def getInstance():
        if not hasattr(DB, "instance"):
            DB.instance = DB()
        return DB.instance

    def logTransaction(self, key, option, action, hash) -> None:
        DB.getInstance().getUser(key).requests += 1
        self.log.append((key, option, action, hash))

def loginDB(key: str) -> dict:
    return DB.getInstance().getUser(key).status()

def buyDB(key: str, stock: str) -> bool:
    global COMPANIES
    p = DB.getInstance().getUser(key)
    DB.getInstance().logTransaction(key, stock, "buy", key + stock + "buy")
    if p.balance > COMPANIES[stock]["price"]:
        p.portfolio[stock] += 1
        p.balance -= COMPANIES[stock]["price"]
        return True
    return False

def sellDB(key: str, stock: str) -> bool:
    global COMPANIES
    p = DB.getInstance().getUser(key)
    DB.getInstance().logTransaction(key, stock, "sell", key + stock + "sell")
    if p.portfolio[stock] > 0:
        p.portfolio[stock] -= 1
        p.balance += COMPANIES[stock]["price"]
        return True
    return False

def buyFlagDB(key: str) -> str:
    p = DB.getInstance().getUser(key)
    if p.balance >= 9001:
        p.balance -= 9001
        return open("flag.txt", "r").read()
    return ""

def postTrade(key: str, stock: str) -> bool:
    p = DB.getInstance().getUser(key)
    if p.portfolio[stock] > 0:
        p.portfolio[stock] -= 1
        return True
    return False

def processTransaction(key: str, action: int, stock: str, stock1 = None) -> str:
    global COMPANIES, QUEUE
    #sanity check
    print(key, action, stock, stock1, stock in COMPANIES.keys(), stock1 in COMPANIES.keys())
    if (stock != "flag" and stock not in COMPANIES.keys()) or (stock1 != None and stock1 not in COMPANIES.keys()):
        print("BAD")
        return "BAD REQUEST"
    if action == ACTION.BUY.value:
        QUEUE.append((key, 1, stock, stock1))
        return "SUCCESS"
    elif action == ACTION.SELL.value:
        QUEUE.append((key, 2, stock, stock1))
        return "SUCCESS"
    elif action == ACTION.TRADE.value:
        QUEUE.append((key, 3, stock, stock1))
        return "SUCCESS"
    elif action == ACTION.FLAG.value:
        return buyFlagDB(key)

    print("BAD")
    return "BAD REQUEST"

def threadTransact():
    global QUEUE
    global TRADEPOST
    bkup = dict()
    while True:
        if QUEUE:
            key, action, s1, s2 = QUEUE.popleft()
            p = DB.getInstance().getUser(key)
            #process trading by posting trade request
            #onto the classified
            if action == 3:
                if(postTrade(key, s1)):
                    TRADEPOST.append((key, s1, s2))
            #money related actions is very costly to the server,
            #throttle if the user has more than 1 requests per second
            #over 10 second survey period
            if p.requests > 10:
                #Throttling, ignore request and attempts to restore
                if key in bkup:
                    p = DB.getInstance().getUser(key)
                    p.balance = bkup[key].balance
                    p.requests = bkup[key].requests
                    p.portfolio = bkup[key].portfolio
                continue
            bkup[key] = Portfolio.bkup(key, p.portfolio, p.balance, p.requests)
            if action == 1:
                buyDB(key, s1)
            elif action == 2:
                sellDB(key, s1)

#since we control the platform
#we can make a bot to automatically scrape good trades
#and reject ones that is not good trade
def market_scrape():
    while True:
        if TRADEPOST:
            key, s1, s2 = TRADEPOST.popleft()
            if COMPANIES[s1]['price'] > COMPANIES[s2]['price']:
                #this is a good trade, yoink
                DB.getInstance().getUser(key).portfolio[s2] += 1
            else:
                #not a good trade
                DB.getInstance().getUser(key).portfolio[s1] += 1

def Throttle_Splash():
    while True:
        sleep(10)
        for i in DB.getInstance().getUsers():
            i.requests = 0
        print(len(QUEUE))


