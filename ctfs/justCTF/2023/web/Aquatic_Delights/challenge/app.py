#!/usr/bin/env python
import flask
import json
import sqlite3
from os import getenv

app = flask.Flask(__name__, static_url_path='/static')
DATABASE = None

def database_connection(func):
    def wrapper(self, *args, **kwargs):
        with sqlite3.connect('/tmp/shop.db') as con:
            if hasattr(self, 'locked') and self.locked:
                return flask.jsonify({'result': 'NG', 'reason': 'Database is locked!'}), 500
            try:
                return func(self, con.cursor(), *args, **kwargs)
            except Database.Error as ex:
                return flask.jsonify({'result': 'NG', 'reason': str(ex)}), 500
            except:
                return flask.abort(500, 'Something went wrong')
            
    return wrapper

def database_lock(func):
    def wrapper(self, *args, **kwargs):
        try:
            self.locked = True
            result = func(self, *args, **kwargs)
        except:
            raise
        finally:
            self.locked = False

        return result
    return wrapper

class Database(object):
    @database_connection
    def __init__(self, cur):
        self.just_coins = 10

        cur.execute("DROP TABLE IF EXISTS shop")
        cur.execute("CREATE TABLE shop(name, price, available)")
        shop_data = [
            ('Catfish', 1, 10),
            ('Rainbow Guppy', 5, 5),
            ('Koi Carp', 20, 3),
            ('Royal Angelfish', 100, 1),
            ('Flagfish', 1337, 1)
        ]
        cur.executemany("INSERT INTO shop(name, price, available) VALUES(?, ?, ?)", shop_data)
        
        cur.execute("DROP TABLE IF EXISTS inventory")
        cur.execute("CREATE TABLE inventory(name, available)")
        cur.executemany("INSERT INTO inventory(name, available) VALUES(?, ?)", 
            [
                (name, 0) for name, _, _ in shop_data
            ]
        )

    def _get_shop(self, cur, name=None):
        if name is None:
            return {x[0]: x[1:] for x in cur.execute("SELECT * FROM shop")}
        else:
            cur.execute("SELECT price, available FROM shop WHERE name = ?", (name,))
            return cur.fetchone()
    
    def _get_inventory(self, cur, name=None):
        if name is None:
            return {x[0]: x[1] for x in cur.execute("SELECT * FROM inventory")}
        else:
            cur.execute("SELECT available FROM inventory WHERE name = ?", (name,))
            return cur.fetchone()[0]
    
    def _update_shop(self, cur, name, available):
        cur.execute("UPDATE shop SET available = ? WHERE name = ?", (available, name))

    def _update_inventory(self, cur, name, available):
        cur.execute("UPDATE inventory SET available = ? WHERE name = ?", (available, name))
    
    def _get_shop_data(self, cur):
        data = {}
        shop = self._get_shop(cur)
        inventory = self._get_inventory(cur)
        for name, item in shop.items():
            data[name.replace(' ', '_')] = {
                'price': item[0],
                'available': item[1],
                'eat': inventory.get(name)
            }
        
        return data

    class Error(Exception):
        pass

    @database_connection
    @database_lock
    def buy(self, cur, name, amount):
        shop_price, shop_available = self._get_shop(cur, name)
        inv_available = self._get_inventory(cur, name)

        if shop_available == 0:                    raise Database.Error('There is no more item of this type in shop')
        if amount <= 0 or amount > 0xffffffff:     raise Database.Error('Invalid amount')
        if shop_available < amount:                raise Database.Error('Not enough items in shop')

        total_price = shop_price * amount
        if total_price > self.just_coins:          raise Database.Error('Not enough justCoins')

        self.just_coins -= total_price
        self._update_inventory(cur, name, inv_available + amount)
        self._update_shop(cur, name, shop_available - amount)

        return flask.jsonify({'result': 'OK', 'response': f'Successfully bought {amount} {name}', 
                              'justCoins': DATABASE.just_coins, 'data': self._get_shop_data(cur)})
        
    @database_connection
    @database_lock
    def sell(self, cur, name, amount):
        inv_available = self._get_inventory(cur, name)

        if inv_available < amount:                 raise Database.Error('Not enough items in inventory')
        if amount <= 0 or amount > 0xffffffff:     raise Database.Error('Invalid amount')

        shop_price, shop_available = self._get_shop(cur, name)
        total_price = shop_price * amount

        self.just_coins += total_price
        self._update_inventory(cur, name, inv_available - amount)
        self._update_shop(cur, name, shop_available + amount)

        return flask.jsonify({'result': 'OK', 'response': f'Successfully sold {amount} {name}', 
                              'justCoins': DATABASE.just_coins, 'data': self._get_shop_data(cur)})
    
    @database_connection
    def eat(self, cur, name):
        inv_available =  self._get_inventory(cur, name)

        if inv_available <= 0:                     raise Database.Error('Not enough items in inventory')
        self._update_inventory(cur, name, inv_available - 1)

        if name == 'Flagfish':
            response = getenv("FLAG")
        else:
            response = 'Nothing happened'
        
        return flask.jsonify({'result': 'OK', 'response': response, 'justCoins': DATABASE.just_coins,
                              'data': self._get_shop_data(cur)})
    
    @database_connection
    def get_table(self, cur):
        return flask.render_template('table.html', inv=DATABASE._get_inventory(cur), shop=DATABASE._get_shop(cur))
    
    @database_connection
    def get_inventory(self, cur=None):
        return self._get_inventory(cur)

    @database_connection
    def get_shop(self, cur=None):
        return self._get_shop(cur)
    
@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html', just_coins=DATABASE.just_coins,  inv=DATABASE.get_inventory(), shop=DATABASE.get_shop())

@app.route('/api/buy', methods=['POST'])
def api_buy():
    try:
        data = json.loads(flask.request.data)
        assert isinstance(data['name'], str)
        assert isinstance(data['amount'], int)
    except:
        return flask.abort(400, 'Invalid request')

    return DATABASE.buy(data['name'], data['amount'])

@app.route('/api/sell', methods=['POST'])
def api_sell():
    try:
        data = json.loads(flask.request.data)
        assert isinstance(data['name'], str)
        assert isinstance(data['amount'], int)
    except:
        return flask.abort(400, 'Invalid request')

    return DATABASE.sell(data['name'], data['amount'])

@app.route('/api/eat', methods=['POST'])
def api_eat():
    try:
        data = json.loads(flask.request.data)
        assert isinstance(data['name'], str)
    except:
        return flask.abort(400, 'Invalid request')

    return DATABASE.eat(data['name'])

@app.route('/reset', methods=['GET'])
def reset():
    DATABASE.__init__()
    
    return flask.redirect("/")

if __name__ == '__main__':
    DATABASE = Database()
    app.run(host="0.0.0.0", port=8080)
