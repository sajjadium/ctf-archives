import json
from time import time
import tornado
import tornado.websocket
import tornado.ioloop
import random
import asyncio
import os
from datetime import timedelta

import tornado.web
import tornado.gen

PORT = 8000

NUM_RACCOONS = 8
FINISH_LINE = 1000
TARGET_BET = 1000
STEP_TIME = 0.25 # in seconds
BETTING_TIME = 15 # in seconds

FLAG = os.environ["GZCTF_FLAG"]

active_betters = {}
connections = {}
connection_count = 0
game = None

class RaccoonRun:
    def __init__(self):
        self.raccoons = [0] * 8
        self.finishers = []
        self.can_bet = True
        self.bet_end = 0

    def step(self):
        self.can_bet = False
        random_int = random.getrandbits(32)
        for i in range(NUM_RACCOONS):
            self.raccoons[i] += (random_int >> (i * 4)) % 16
        for (i, x) in enumerate(self.raccoons):
            if x >= FINISH_LINE and i not in self.finishers:
                self.finishers.append(i)
        return (self.raccoons, self.finishers)
    
    def game_over(self):
        return len(self.finishers) >= NUM_RACCOONS
    
class Gambler:
    def __init__(self, account=10):
        self.account = account
        self.guess = None
        self.bet_amount = 0
    
    def bet(self, guess, bet_amount):
        if self.validate_bet(guess, bet_amount):
            self.guess = guess
            self.bet_amount = bet_amount
            return True
        else:
            return False
    
    def validate_bet(self, guess, bet_amount):
        if (type(guess) is not list):
            return False
        if not all(type(x) is int for x in guess):
            return False
        if len(guess) != NUM_RACCOONS:
            return False
        if (type(bet_amount) is not int):
            return False
        if (bet_amount < 0 or bet_amount > self.account):
            return False
        return True

    # updates amount of money in account after game is over and bet comes through
    # and then return an boolean indicating whether you won/lost
    def check_bet(self, game_instance):
        if game_instance.finishers == self.guess:
            self.account += self.bet_amount
            return True
        else:
            self.account -= self.bet_amount
            return False
    
    def reset_bet(self):
        self.guess = None
        self.bet_amount = 0

def get_race_information(id):
    return json.dumps({"type": "race_information", "can_bet": "true" if game.can_bet else "false", "raccoons": game.raccoons, "finishers": game.finishers, "account": active_betters[id].account})

class RRWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        global game
        global active_betters
        global connections
        global connection_count
        
        self.better_id = connection_count
        active_betters[self.better_id] = Gambler()
        connections[self.better_id] = self
        connection_count += 1
        self.write_message(get_race_information(self.better_id))
        if game.can_bet:
            self.write_message(json.dumps({"type":"betting-starts","until":game.bet_end}))
    
    def on_message(self, message):
        try:
            data = json.loads(message)
            if "type" not in data:
                self.write_message(json.dumps({"type": "response", "value": "invalid WebSockets message"}))
            elif (data["type"] == "bet"):
                if (game.can_bet):
                    if active_betters[self.better_id].bet(data["order"], data["amount"]):
                        self.write_message(json.dumps({"type": "response", "value": "bet successfully placed!"}))
                    else:
                        self.write_message(json.dumps({"type": "response", "value": "bet is invalid, failed to be placed"}))
                else:
                    self.write_message(json.dumps({"type": "response", "value": "bet cannot be placed after the race starts, failed to be placed"}))
            elif (data["type"] == "buy_flag"):
                if (active_betters[self.better_id].account > TARGET_BET):
                    self.write_message(json.dumps({"type": "flag", "value": FLAG}))
            elif (data["type"] == "state"):
                self.write_message(json.dumps({"type": "response", "value": "bet" if game.can_bet else "race"}))
            elif (data["type"] == "account"):
                self.write_message(json.dumps({"type": "response", "value": active_betters[self.better_id].account}))
            else:
                self.write_message(json.dumps({"type": "response", "value": "invalid WebSockets message"}))
        except json.JSONDecodeError:
            self.write_message(json.dumps({"type": "response", "value": "invalid WebSockets message"}))

    def on_close(self):
        del active_betters[self.better_id]
        del connections[self.better_id]

def game_loop():
    global game
    print("Raccoons", game.raccoons)
    print("Finishers", game.finishers)
    for (id, connection) in connections.items():
        connection.write_message(get_race_information(id))
    game.step()
    if game.game_over():
        print("Raccoons", game.raccoons)
        print("Finishers", game.finishers)
        for (id, connection) in connections.items():
            connection.write_message(get_race_information(id))
            connection.write_message(json.dumps({"type":"result", "value": game.finishers}))
        for (id, x) in active_betters.items():
            if x.guess != None:
                win = x.check_bet(game)
                connections[id].write_message(json.dumps({"type": "bet_status", "value": f"you {'won' if win else 'lost'} the bet, your account now has ${x.account}"}))
                x.reset_bet()
            else:
                connections[id].write_message(json.dumps({"type": "bet_status", "value": f"you didn't place a bet, your account now has ${x.account}"}))
        print("Every raccoon has finished the race.")
        print(f"Starting new game! Leaving {BETTING_TIME} seconds for bets...")
        game = RaccoonRun()
        game.bet_end = time() + BETTING_TIME
        for (id, connection) in connections.items():
            connection.write_message(get_race_information(id))
            connection.write_message(json.dumps({"type":"betting-starts","until":game.bet_end}))
        tornado.ioloop.IOLoop.current().add_timeout(timedelta(seconds=BETTING_TIME), game_loop)
    else:
        tornado.ioloop.IOLoop.current().add_timeout(timedelta(seconds=STEP_TIME), game_loop)

if __name__ == "__main__":
    tornado.ioloop.IOLoop.configure("tornado.platform.asyncio.AsyncIOLoop")
    io_loop = tornado.ioloop.IOLoop.current()
    asyncio.set_event_loop(io_loop.asyncio_loop)
    game = RaccoonRun()
    print(f"Starting new game! Leaving {BETTING_TIME} seconds for bets...")
    game.bet_end = time() + BETTING_TIME
    tornado.ioloop.IOLoop.current().add_timeout(timedelta(seconds=BETTING_TIME), game_loop)
    application = tornado.web.Application([
        (r"/ws", RRWebSocketHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./static", "default_filename": "index.html"})
    ])
    application.listen(PORT)
    io_loop.start()