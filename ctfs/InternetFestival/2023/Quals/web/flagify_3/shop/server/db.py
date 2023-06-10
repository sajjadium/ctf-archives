import mysql.connector
import utils
import hashlib
import os


class DBException(Exception):
    pass


class DB:
    hostname = os.environ.get('DBHOST', '127.0.0.1')
    dbname = os.environ.get('MYSQL_DATABASE', 'shop_db')
    username = 'root'
    password = os.environ.get('MYSQL_ROOT_PASSWORD', 'password')

    def __init__(self):
        data = {
            "user": DB.username,
            "password": DB.password,
            "host": DB.hostname,
            "database": DB.dbname
        }

        try:
            self.connection = mysql.connector.connect(**data)
        except mysql.connector.Error as err:
            raise DBException("Error on database connection")

    def __del__(self):
        self.connection.close()

    def get_cursor(self):
        return self.connection.cursor(dictionary=True, prepared=True)

    def commit(self):
        try:
            return self.connection.commit()
        except mysql.connector.Error as err:
            raise DBException("Error on commit")

    # str, str -> str
    def compute_hash(self, password, salt):
        h = hashlib.sha256()
        h.update(password.encode())
        h.update(salt.encode())
        return h.hexdigest()

    # -> True if registed
    # -> False if can't register
    def register(self, username, password):
        cursor = self.get_cursor()

        try:
            cursor.execute(
                "SELECT id FROM user WHERE username = %s", (username,))
        except mysql.connector.Error as err:
            cursor.close()
            raise DBException("Error in select in register")

        users = cursor.fetchall()
        if len(users) == 1:
            cursor.close()
            return False

        salt = utils.random_string(10)
        password_hash = self.compute_hash(password, salt)

        try:
            cursor.execute("""
                INSERT INTO user(id, username, password_hash, salt)
                VALUES (DEFAULT, %s, %s, %s); 
                """, (username, password_hash, salt))

            self.commit()
            cursor.close()

            return True
        except mysql.connector.Error as err:
            raise DBException("Error in insert in register")

    def login(self, username, password):
        cursor = self.get_cursor()

        try:
            cursor.execute(
                "SELECT id, username, password_hash, salt FROM user WHERE username = %s;", (username,))
        except mysql.connector.Error as err:
            raise DBException("Error in select in login")

        users = cursor.fetchall()
        cursor.close()

        if len(users) == 0:
            return None

        user = users[0]

        if self.compute_hash(password, user['salt']) != user['password_hash']:
            return None

        return User(user)

    def get_user_from_id(self, user_id):
        cursor = self.get_cursor()

        try:
            cursor.execute(
                "SELECT id, username, password_hash, salt FROM user WHERE id = %s;", (user_id,))
        except mysql.connector.Error as err:
            raise DBException("Error in select in get_user_from_id")

        users = cursor.fetchall()
        cursor.close()

        return User(users[0])

    def get_all_items(self):
        cursor = self.get_cursor()

        try:
            cursor.execute("SELECT id, name, content, cost FROM item;")
        except mysql.connector.Error as err:
            raise DBException("Error in select in get_all_items")

        items = cursor.fetchall()
        cursor.close()

        return [Item(x) for x in items]

    def get_item_from_id(self, item_id):
        cursor = self.get_cursor()

        try:
            cursor.execute("SELECT id, name, content, cost FROM item where id = %s;", (item_id,))
        except mysql.connector.Error as err:
            raise DBException("Error in select in get_item_from_id")

        items = cursor.fetchall()

        if len(items) == 0:
            return None
        
        return Item(items[0])

    def make_transaction(self, user_id, item_id):
        cursor = self.get_cursor()

        tx_id = utils.random_string(10)

        try:
            cursor.execute("""
                INSERT INTO transaction VALUES
                    (%s, %s, %s, FALSE);
            """, (tx_id, user_id, item_id))

            self.commit()
        except mysql.connector.Error as err:
            raise DBException("Error in insert in make_transaction")

        return Transaction(tx_id, user_id, item_id, False)


    def get_owned_items(self, user_id):
        cursor = self.get_cursor()

        try:
            cursor.execute("""
            SELECT i.id, i.name, i.content, i.cost 
            FROM transaction t
            INNER JOIN item i
                ON t.item_id = i.id
            WHERE t.status = TRUE AND user_id = %s
            """, (user_id,))
        except mysql.connector.Error as err:
            raise DBException("Error in select in get_owned_items")
        
        items = cursor.fetchall()

        return [Item(x) for x in items]


    def checkout_transaction(self, transaction_id):
        cursor = self.get_cursor()

        try:
            cursor.execute("UPDATE transaction SET status = TRUE WHERE id = %s", (transaction_id,))
            self.commit()
            cursor.close()
        except mysql.connector.Error as err:
            raise DBException("Error in update in checkout_transaction")


class User:
    def __init__(self, user_dict):
        self.id = user_dict['id']
        self.username = user_dict['username']
        self.password_hash = user_dict['password_hash']
        self.salt = user_dict['salt']

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Item:
    def __init__(self, item_dict):
        self.id = item_dict['id']
        self.name = item_dict['name']
        self.content = item_dict['content']
        self.cost = item_dict['cost']

    def __repr__(self):
        return f'{self.id} - {self.name} - {self.cost}'


class Transaction:
    def __init__(self, tx_id, user_id, item_id, status):
        self.id = tx_id
        self.user_id = user_id
        self.item_id = item_id
        self.status = status

    def from_dict(tx_dict):
        return Transaction(tx_dict['id'], tx_dict['user_id'], tx_dict['item_id'], tx_dict['status'])
