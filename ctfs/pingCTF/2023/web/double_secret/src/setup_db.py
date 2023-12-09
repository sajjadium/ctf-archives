
import mysql.connector
from secrets import token_hex 
import os

secret = token_hex(12)

mydb = mysql.connector.connect(
  host="db",
  user="root",
  password="password",
)
mycursor = mydb.cursor()


mycursor.execute("CREATE DATABASE chall")
mycursor.execute("USE chall")

mycursor.execute("CREATE TABLE secret (secret TEXT)")
mycursor.execute("INSERT INTO secret (secret) VALUES ( %s )", [secret])

mycursor.execute("CREATE TABLE users (id INT NOT NULL AUTO_INCREMENT, name TEXT, password TEXT, isAdmin BIT, PRIMARY KEY (id), UNIQUE (name(32)))")
mycursor.execute("INSERT INTO users (name, password, isAdmin) VALUES (%s, %s, %s)", ['admin', token_hex(8), True])


mydb.commit()
