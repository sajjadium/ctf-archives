import threading


class Wallet():
    def __init__(self) -> None:
        self.balances = {
            "cashout": 1000,
            "glaciercoin": 0,
            "ascoin": 0,
            "doge": 0,
            "gamestock": 0,
            "ycmi": 0,
            "smtl": 0
        }
        self.lock = threading.Lock();


    def getBalances(self):
        return self.balances
    
    def transaction(self, source, dest, amount):
        if source in self.balances and dest in self.balances:
            with self.lock:
                if self.balances[source] >= amount:
                    self.balances[source] -= amount
                    self.balances[dest] += amount
                    return 1
        return 0
    
    def inGlacierClub(self):
        with self.lock:
            for balance_name in self.balances:
                if balance_name == "cashout":
                    if self.balances[balance_name] < 1000000000:
                        return False
                else:
                    if self.balances[balance_name] != 0.0:
                        return False
            return True
