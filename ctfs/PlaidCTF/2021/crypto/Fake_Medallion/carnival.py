from bank import Bank
import random
from os import urandom

FLAG = "PCTF{REDACTED}"

# Game of Razzle
class RazzleGame:
    def __init__(self):
        self.welcome_message = (
            "Welcome to our custom game of razzle! It takes one "
            "medallion for each game. You roll 8 dies and take the "
            "sum of the values rolled. If that sum is less than 12 or "
            "greater than 42, you get $2000! "
            "If you lose, you lose your medallion."
        )

    def play(self):
        # Well, razzle is supposed to be a scam
        while True:
            res = []
            for i in range(8):
                res.append(random.randint(1,6))
            s = sum(res)
            if s >= 12 and s <= 42:
                return (False, res)


# Carnival, where you use medallions as tokens of entry for our games.
class Carnival:
    def __init__(self, peername):
        self.bank = Bank()
        self.secret = FLAG
        self.user_money = 1024
        self.peername = peername

    def menu(self):
        return open('welcome.txt', 'rb').read()
    
    def help(self):
        return open('help.txt', 'r').read()

    # Call out the robber's IP address    
    def contact_police(self):
        peer = self.peername[0] + ":" + str(self.peername[1])
        return {'error': 
            f"{peer} is trying to rob our carnival with " +
            "fake medallions."}
    
    # Playing razzle
    def play_razzle(self, med_id):
        legit = self.bank.verify_medallion(med_id)
        if not legit:
            return self.contact_police()
        else:
            # Of course, you can't just use our services for free
            razzle = RazzleGame()
            win, res = razzle.play()
            if win:
                self.user_money += 2000
            return {
                'msg': razzle.welcome_message, 
                'rolls': res, 
                'win': win
            }

    # Clients can buy our carnival's medallion for $1000. If you already
    # have a medallion, please spend it before buying a new one.
    def money_for_medallion(self):
        if self.user_money < 1000:
            return {'error': "insufficient funds"}
        self.user_money -= 1000
        med_id = self.bank.new_medallion()
        return {'msg': f"Your new medallion {med_id} now stored at our bank."}

    # Clients can redeem their medallions for $999. The one dollar
    # difference is our competitive handling fee.
    def medallion_for_money(self, med_id):
        # Please also destroy the medallion in the process
        legit = self.bank.verify_medallion(med_id)
        if not legit:
            return self.contact_police()
        else:
            # Of course, you can't just use our services for free
            self.user_money += 999
            return {'msg': "Here you go. "}
    
    # Clients can refresh the system, void all previously
    # owned medallions, and gain a new medallion, for $1. Clients
    # must prove that they previously own at least 1 medallion, though.
    def medallion_for_medallion(self, med_id):
        if self.user_money < 1:
            return {'error': "insufficient funds"}
        self.user_money -= 1 
        # Please also destroy the medallion in the process
        legit = self.bank.verify_medallion(med_id)
        if not legit:
            return self.contact_police()
        else:
            old_medallion = self.bank.get_medallion(med_id)
            self.bank.refresh_bank()
            new_id = self.bank.new_medallion()
            return {'msg': f"New medallion {new_id} created. " +
                "Your old one was " +
                old_medallion +
                ". That one is now invalid."}
    
    # Our carnival bank offers free-of-charge computers for
    # each bit in the medallion. This is not necessary for
    # ordinary clients of the carnival.
    def play_with_medallion(self, data):
        return self.bank.operate_on_medallion(data)

    # Script for interacting with the user
    def interact(self, data):
        if 'option' not in data:
            return {'error': 'no option selected'}
        if data['option'] == 'help':
            res = {'help': self.help()}
        elif data['option'] == 'money_for_med':
            res = self.money_for_medallion()
        elif data['option'] == 'med_for_money':
            if 'med_id' not in data:
                return {'error': 'incomplete data'}
            res = self.medallion_for_money(int(data['med_id']))
        elif data['option'] == 'med_for_med':
            if 'med_id' not in data:
                return {'error': 'incomplete data'}
            res = self.medallion_for_medallion(int(data['med_id']))
        elif data['option'] == 'play_razzle':
            res = self.play_razzle(int(data['med_id']))
        elif data['option'] == 'op_on_med':
            res = self.play_with_medallion(data)
        else:
            return {'error': 'unrecognized option'}         

        if 'error' in res:
            return res
        if self.user_money > 15213:
            res['flag'] = ("We shan't begin to fathom how you " +
                "cheated at our raffle game. To attempt to appease "
                f"you, here is a flag: {self.secret}")
        res['curr_money'] = self.user_money
        return res
        
