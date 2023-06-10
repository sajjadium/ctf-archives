import mysql.connector
import utils
import hashlib
import os


class DBException(Exception):
    pass


class DB:
    hostname = os.environ.get('DBHOST', '127.0.0.1')
    dbname = os.environ.get('MYSQL_DATABASE', 'bank_db')
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
                INSERT INTO user(id, username, password_hash, salt, credit, totp_secret)
                VALUES (DEFAULT, %s, %s, %s, 10, NULL); 
                """, (username, password_hash, salt))

            self.commit()
            cursor.close()

            return True
        except mysql.connector.Error as err:
            raise DBException("Error in insert in register")

    # -> User dictionary if logged in
    # -> None if wrong credentials or user doesn't exists
    def login(self, username, password):
        cursor = self.get_cursor()

        try:
            cursor.execute(
                "SELECT id, username, password_hash, salt, credit, totp_secret FROM user WHERE username = %s;", (username,))
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

    def disable_totp(self, user_id):
        cursor = self.get_cursor()

        try:
            cursor.execute(
                "UPDATE user SET totp_secret = NULL WHERE id = %s;", (user_id,))

            self.commit()
            cursor.close()
        except mysql.connector.Error as err:
            cursor.close()
            raise DBException("Error in update in disable_totp")          

    def enable_totp(self, user_id, totp_secret):
        cursor = self.get_cursor()

        try:
            cursor.execute(
                "UPDATE user SET totp_secret = %s WHERE id = %s;", (totp_secret, user_id,))

            self.commit()
            cursor.close()
        except mysql.connector.Error as err:
            cursor.close()
            raise DBException("Error in update in disable_totp")


    def decrement_user_credit(self, user_id, amount):
        cursor = self.get_cursor()

        try:
            cursor.execute("UPDATE user SET credit = credit - %s WHERE id = %s;", (amount, user_id))

            self.commit()
            cursor.close()

            return True

        except mysql.connector.Error as err:
            cursor.close()
            raise DBException("Error in update in update_user_credit")


    def get_user_from_id(self, user_id):
        cursor = self.get_cursor()

        try:
            cursor.execute(
                "SELECT id, username, password_hash, salt, credit, totp_secret FROM user WHERE id = %s;", (user_id,))
        except mysql.connector.Error as err:
            raise DBException("Error in select in get_user_from_id")

        users = cursor.fetchall()
        cursor.close()

        return User(users[0])


class User:
    def __init__(self, user_dict):
        self.id = user_dict['id']
        self.username = user_dict['username']
        self.password_hash = user_dict['password_hash']
        self.salt = user_dict['salt']
        self.credit = user_dict['credit']
        self.totp_secret = user_dict['totp_secret']

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
