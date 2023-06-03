import mysql.connector
import os
import bcrypt
import hashlib
import secrets

class Connector(object):

    def __init__(self):
        self.host = os.getenv('MYSQL_DATABASE_HOST')
        self.user = os.getenv('MYSQL_DATABASE_USER')
        self.password = os.getenv('MYSQL_DATABASE_PASSWORD')
        self.db = os.getenv('MYSQL_DATABASE_DB')
        self.connection = None

    def initMySQL(self):
        self.connection = mysql.connector.connect(host=self.host,
                             database=self.db,
                             user=self.user,
                             password=self.password)

        return self.connection.cursor(prepared=True, dictionary=True)


    def loginUserCheck(self, username, password, identifier, cursor):
        query = "SELECT id,password FROM user WHERE username = %s AND identifier = %s"

        user_to_retrivie = (username, identifier)
        cursor.execute(query, user_to_retrivie)

        rows = cursor.fetchall()

        return str(rows[0]['id']) if len(rows) > 0 and\
                              bcrypt.checkpw(password.encode(), rows[0]['password'].encode())\
                        else False

    def getProductsFromDb(self, cursor):
        query = "SELECT * FROM products"
        cursor.execute(query)

        rows = cursor.fetchall()
        return rows

    def addProductToCart(self, cursor, productid, userid):
        query = """INSERT INTO cart (productid,userid) VALUES (%s,%s)"""
        to_parameterize = (int(productid), int(userid))

        thrownEx = False

        try:
            cursor.execute(query, to_parameterize)
            self.connection.commit()
        except Exception:
            thrownEx = True

        return not thrownEx

    def getProductFromCart(self, cursor, userid):
        rows = []

        query = """SELECT name,price FROM products AS P JOIN cart
                       as C ON P.id = C.productid WHERE C.userid = %s"""
        useridBind = (userid,)
        cursor.execute(query, useridBind)

        rows = cursor.fetchall()

        return rows

    def registerUser(self, username, password, cursor):
        sql_insert_query = """ INSERT INTO user
                       (username, password, identifier) VALUES (%s,%s,%s)"""

        identifier = hashlib.sha256(secrets.token_bytes(64)).hexdigest()

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user_to_inser = (username, hashed, identifier)
        thrownEx = False

        try:
            cursor.execute(sql_insert_query, user_to_inser)
            self.connection.commit()
        except Exception:
            thrownEx = True

        return identifier if not thrownEx else False
