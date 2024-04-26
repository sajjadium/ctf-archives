import os
import shutil
import mysql.connector
from flask import Flask, request, jsonify, send_from_directory, redirect
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt, create_access_token
from flask_cors import CORS
import base64
import time
import psycopg2
from time import sleep
import uuid
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["JWT_SECRET_KEY"] = os.urandom(64)
jwt = JWTManager(app)

MYSQL_DB_HOST = os.getenv("MYSQL_HOST") or 'mysql'
MYSQL_DB_USER = os.getenv("MYSQL_USER") or 'root'
MYSQL_DB_PASSWORD = os.getenv("MYSQL_PASSWORD") or 'password'
MYSQL_DB_DATABASE = os.getenv("MYSQL_DB") or 'inso24'

PG_DB_HOST = os.getenv("PG_HOST") or 'pg'
PG_DB_USER = os.getenv("PG_USER") or 'postgres'
PG_DB_PASSWORD = os.getenv("PG_PASSWORD") or 'postgres'
PG_DB_DATABASE = os.getenv("PG_DB") or 'inso24'

FLAG = os.getenv("FLAG") or 'INS{fake-flag}'

def get_db(type='mysql'):
    if type == 'mysql':
        conn = mysql.connector.connect(
            host=MYSQL_DB_HOST,
            user=MYSQL_DB_USER,
            password=MYSQL_DB_PASSWORD,
            database=MYSQL_DB_DATABASE
        )
    elif type == 'pg':
        conn = psycopg2.connect(
            host=PG_DB_HOST,
            database=PG_DB_DATABASE,
            user=PG_DB_USER,
            password=PG_DB_PASSWORD)
    return conn



@app.route("/accounts", methods=['GET','PUT'])
@jwt_required()
def accounts():
    results = {}
    userid = get_jwt_identity()
    conn = get_db()
    cursor = conn.cursor()
    if request.method == "PUT":
        for accid in request.json:
            cursor.execute("UPDATE accounts SET name = %s WHERE id = %s AND userid = %s",(request.json[accid]["name"],accid,userid))
        conn.commit()
    cursor.execute('''
        SELECT id,name,balance FROM accounts WHERE userid = %s
        ''', (userid,))
    for (accountid,name,balance) in cursor.fetchall():
        if balance > 13.37:
            results[accountid] = {'name': name, 'balance': balance, 'flag': FLAG}
        else:
            results[accountid] = {'name': name, 'balance': balance}
    conn.close()
    return jsonify(results)

@app.route("/profile", methods=['GET','PUT'])
@jwt_required()
def profile():
    userid = get_jwt_identity()
    conn = get_db()
    cursor = conn.cursor()
    if request.method == "PUT":
        cursor.execute('''
            UPDATE users SET firstname = %s, lastname = %s, email = %s WHERE id = %s
            ''', (request.json.get("firstname"),request.json.get("lastname"),request.json.get("email"),userid))
        conn.commit()

    cursor.execute('''
        SELECT id,firstname,lastname,email FROM users WHERE id = %s
        ''', (userid,))
    (userid,firstname,lastname,email) = cursor.fetchone()
    conn.close()
    return jsonify({'id': userid, 'firstname': firstname, 'lastname': lastname, 'email': email})
    
@app.route("/transactions", methods=['GET','DELETE'])
@jwt_required()
def transactions():
    userid = get_jwt_identity()
    conn = get_db()
    cursor = conn.cursor()
    batchid = request.args.get("batchid")
    if request.method == "DELETE":
        connpg = get_db(type='pg')
        cursorpg = connpg.cursor()
        cursorpg.execute("DELETE FROM batch_transactions WHERE batchid = %s AND id = %s", (batchid,request.json.get("txid")))
        connpg.commit()
        connpg.close()
        cursor.execute("DELETE FROM batch_transactions WHERE batchid = %s and id = %s", (batchid,request.json.get("txid")))
        conn.commit()
    
    cursor.execute('''
        SELECT bt.id, bt.batchid, bt.recipient, a.name, bt.amount, bt.verified, bt.executed FROM batch_transactions bt LEFT OUTER JOIN accounts a ON a.id = bt.recipient WHERE bt.batchid = %s
        ''', (batchid,))
    results = []
    try:
        for (txid,batchid,recipient,recipientname,amount,verified,executed) in cursor.fetchall():
            results.append({'txid':txid,'batchid':batchid,'recipient':recipient,'recipientname':recipientname,'amount':amount,'verified':verified,'executed':executed})
    except:
        pass
    conn.close()
    return jsonify(results)

@app.route("/batch/new", methods=['POST'])
@jwt_required()
def newbatch():
    userid = get_jwt_identity()
    batchid = str(uuid.uuid4())
    senderid = request.json.get("senderid")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT userid FROM accounts WHERE id = %s
        ''',(senderid,))
    data = cursor.fetchone()
    if data == None or data[0]!=userid:
        return jsonify({"error":"Invalid account"})
    cursor.execute('''
        INSERT INTO batches(id,senderid,userid) VALUES (%s,%s,%s) 
        ''', (batchid,senderid,userid))
    conn.commit()
    conn.close()
    return redirect("/batches")


@app.route("/batches", methods=['GET','DELETE'])
@jwt_required()
def batches():
    userid = get_jwt_identity()
    conn = get_db()
    cursor = conn.cursor()
    if request.method == "DELETE":
        cursor.execute('''
        SELECT userid,executed,verified FROM batches WHERE id = %s
            ''', (request.json.get("batchid"),))

        (buserid,verified,executed) = cursor.fetchone()
        if verified or executed:
            return jsonify({"error":"Cannot delete a verified or executed batch"})
        if buserid != userid:
            return jsonify({"error":"Cannot delete batch"})
        connpg = get_db(type='pg')
        cursorpg = connpg.cursor()
        cursorpg.execute("DELETE FROM batch_transactions WHERE batchid = %s",(request.json.get("batchid"),))
        connpg.commit()
        connpg.close()
        cursor.execute('''
            DELETE FROM batch_transactions WHERE batchid = %s
            ''', (request.json.get("batchid"),))
        cursor.execute('''
            DELETE FROM batches WHERE id = %s
            ''', (request.json.get("batchid"),))
        conn.commit()

    cursor.execute('''
        SELECT b.id,b.senderid,a.name,b.executed,b.verified FROM batches b LEFT OUTER JOIN accounts a ON a.id = b.senderid WHERE b.userid = %s
        ''',(userid,))
    batches = []
    for (batchid,senderid,sendername,executed,verified) in cursor.fetchall():
        batches.append({'batchid':batchid,'senderid':senderid,'sendername':sendername,'executed':executed,'verified':verified})
    return jsonify(batches)

@app.route("/login", methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM users WHERE username = %s AND password = %s
        ''', (username,password))
    data = cursor.fetchone()
    conn.close()
    if data == None:
        return jsonify({"error":"Login failed"})
    access_token = create_access_token(identity=data[0])
    return jsonify({"userid":data[0],"jwt":access_token})

@app.route("/register", methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if len(password) < 15:
        return jsonify({"error":"Strong password required for security reasons"})
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT count(*) FROM users WHERE username = %s
        ''', (username,))
    data = cursor.fetchone()
    if data[0] != 0:
        return jsonify({"error":"User already exists"})

    cursor.execute('''
        INSERT INTO users (username,password) VALUES (%s,%s)
        ''',(username,password))
    userid = cursor.lastrowid
    cursor.execute('''
        INSERT INTO accounts(id, userid, name, balance) VALUES (%s,%s,%s,%s)
        ''',(str(uuid.uuid4()),userid,'Savings account',0))
    cursor.execute('''
        INSERT INTO accounts(id, userid, name, balance) VALUES (%s,%s,%s,%s)
        ''',(str(uuid.uuid4()),userid,'Current account',10))
    cursor.execute('''
        INSERT INTO accounts(id, userid, name, balance) VALUES (%s,%s,%s,%s)
        ''',(str(uuid.uuid4()),userid,'Checkings account',0))
    conn.commit()
    conn.close()
    access_token = create_access_token(identity=userid)
    return jsonify({"userid":userid,"jwt":access_token})

@app.route("/logout", methods=['GET'])
@jwt_required()
def logout():
    return jsonify({"message":"Logged out"})


@app.route("/validate", methods=['POST'])
@jwt_required()
def validate():
    userid = get_jwt_identity()
    batchid = request.json.get("batchid")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id,senderid FROM batches WHERE id = %s AND userid = %s", (batchid,userid))
    data = cursor.fetchone()
    if data == None or data[0] != batchid:
        return jsonify({"error":"Invalid batchid"})
    senderid = data[1]

    cursor.execute("LOCK TABLES batch_transactions WRITE, accounts WRITE, batches WRITE")
    cursor.execute("SELECT sum(amount) FROM batch_transactions WHERE batchid = %s", (batchid,))
    data = cursor.fetchone()

    if data == None or data[0] == None:
        cursor.execute("UNLOCK TABLES")
        conn.close()
        return jsonify({"error":"Invalid batch"})
    total = data[0]
    cursor.execute('''
        SELECT balance FROM accounts WHERE id = %s
        ''', (senderid,))
    data = cursor.fetchone()
    balance = data[0] if data else 0
    if total > balance:
        cursor.execute("UNLOCK TABLES")
        conn.close()
        return jsonify({"error":"Insufficient balance ("+str(total)+" > " + str(balance) +")"})
    cursor.execute('''
        UPDATE accounts SET balance = (balance - %s) WHERE id = %s
    ''',(total,senderid))

    cursor.execute('''
        UPDATE batch_transactions SET verified = true WHERE batchid = %s;
        ''',(batchid,))
    connpg = get_db(type='pg')
    cursorpg = connpg.cursor()
    cursorpg.execute('''
        UPDATE batch_transactions SET verified = true WHERE batchid = %s
        ''',(batchid,))
    connpg.commit()
    connpg.close()
    cursor.execute('''
            UPDATE batches SET verified = true WHERE id = %s;
            ''',(batchid,))
    cursor.execute('''
        UNLOCK TABLES;
    ''')
    conn.close()
    return redirect("/batches")



@app.route("/transfer", methods=['POST'])
@jwt_required()
def transfer():
    userid = get_jwt_identity()
    txid = str(uuid.uuid4())
    amount = request.json.get('amount')
    recipient = request.json.get('recipient')
    batchid = request.json.get('batchid')
    if not float(amount) > 0:
        return jsonify({"error":"Invalid amount"})
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT count(*) FROM batches WHERE id = %s AND userid = %s AND verified = false
        ''',(batchid,userid))
    data = cursor.fetchone()
    if data[0] != 1:
        conn.close()
        return jsonify({"error":"Invalid batchid"})

    cursor.execute('''
        SELECT userid FROM accounts WHERE id = %s
        ''', (recipient,))
    data = cursor.fetchone()
    if data == None or data[0] != userid:
        conn.close()
        return jsonify({"error": "Recipient account does not belong to you"})

    cursor.execute('''
        SELECT count(*) FROM batch_transactions WHERE batchid = %s AND recipient = %s
        ''',(batchid,recipient))
    data = cursor.fetchone()

    if data[0] > 0:
        conn.close()
        return jsonify({"error":"You can only have one transfer per recipient in a batch"})

    cursor.execute('''
        SELECT balance FROM accounts WHERE id = (SELECT senderid FROM batches WHERE id = %s)
            ''', (batchid,))
    data = cursor.fetchone()
    balance = data[0]

    connpg = get_db(type='pg')

    cursorpg = connpg.cursor()
    cursorpg.execute('''
        LOCK TABLE batch_transactions;
        INSERT INTO batch_transactions (id,batchid,recipient,amount) SELECT %s,%s,%s,%s WHERE (SELECT coalesce(sum(amount),0)+%s FROM batch_transactions WHERE batchid = %s) <= %s
        ''', (txid,batchid,recipient,amount,amount,batchid,balance))
    connpg.commit()
    connpg.close()
    cursor.execute('''
        INSERT INTO batch_transactions (id,batchid,recipient,amount) SELECT %s,%s,%s,%s WHERE (SELECT coalesce(sum(amount),0)+%s FROM batch_transactions WHERE batchid = %s) <= %s
        ''', (txid,batchid,recipient,amount,amount,batchid,balance))
    conn.commit()
    conn.close()

    return redirect("/transactions?batchid="+batchid)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
