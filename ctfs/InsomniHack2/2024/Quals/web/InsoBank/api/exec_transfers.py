#!/usr/local/bin/python

import psycopg2
import mysql.connector
import sqlite3
import os

MYSQL_DB_HOST = os.getenv("MYSQL_HOST") or 'mysql'
MYSQL_DB_USER = os.getenv("MYSQL_USER") or 'user'
MYSQL_DB_PASSWORD = os.getenv("MYSQL_PASSWORD") or 'password'
MYSQL_DB_DATABASE = os.getenv("MYSQL_DB") or 'inso24'

PG_DB_HOST = os.getenv("PG_HOST") or 'pg'
PG_DB_USER = os.getenv("PG_USER") or 'postgres'
PG_DB_PASSWORD = os.getenv("PG_PASSWORD") or 'postgres'
PG_DB_DATABASE = os.getenv("PG_DB") or 'inso24'


def get_db(type='mysql'):
    if type == 'mysql':
        conn = mysql.connector.connect(
            host=MYSQL_DB_HOST,
            user=MYSQL_DB_USER,
            password=MYSQL_DB_PASSWORD,
            database=MYSQL_DB_DATABASE
        )
    elif type == 'sqlite':
        conn = sqlite3.connect("/app/db/db.sqlite")
    elif type == 'pg':
        conn = psycopg2.connect(
            host=PG_DB_HOST,
            database=PG_DB_DATABASE,
            user=PG_DB_USER,
            password=PG_DB_PASSWORD)
    return conn

conn = get_db()
cursor = conn.cursor()
connpg = get_db(type='pg')
cursorpg = connpg.cursor()

cursorpg.execute('''
    SELECT DISTINCT batchid FROM batch_transactions WHERE verified = true and executed = false 
    ''')
for (batchid,) in cursorpg.fetchall():
    TRANSFERS = {}
    cursorpg.execute('''
    SELECT id,sender,recipient,amount FROM batch_transactions WHERE batchid = %s AND verified = true AND executed = false 
    ''',(batchid,))
    transactions = cursorpg.fetchall()
    for (txid,sender,recipient,amount) in transactions:
        cursor.execute('''
            UPDATE batch_transactions SET executed = true WHERE id = %s
            ''',(txid,))
        cursorpg.execute('''
            UPDATE batch_transactions SET executed = true WHERE id = %s
            ''',(txid,))
        TRANSFERS[recipient] = amount if recipient not in TRANSFERS.keys() else TRANSFERS[recipient] + amount
    for recipient in TRANSFERS:
        cursor.execute('''
            UPDATE accounts SET balance = balance + %s WHERE id = %s
            ''', (TRANSFERS[recipient], recipient))
    cursor.execute('''
            UPDATE batches SET executed = true WHERE id = %s
            ''',(batchid,))
    connpg.commit()
    conn.commit()
    connpg.close()
    conn.close()
