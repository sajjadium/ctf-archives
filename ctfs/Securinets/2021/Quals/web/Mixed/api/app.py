from flask import Flask, render_template, request
import random
import sqlite3 as sql
import binascii
import json
import base64
from Crypto.Cipher import AES
import config
def my_decrypt(data, passphrase):
    try:
        unpad = lambda s : s[:-s[-1]]
        key = binascii.unhexlify(passphrase)
        encrypted = json.loads(base64.b64decode(data).decode('ascii'))
        encrypted_data = base64.b64decode(encrypted['data'])
        iv = base64.b64decode(encrypted['iv'])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_data)
        clean = unpad(decrypted).decode('ascii').rstrip()
    except Exception as e:
        print("Cannot decrypt datas...")
        print(e)
        exit(1)
    return clean
app = Flask(__name__)



@app.route('/add_note',methods = ['POST', 'GET'])
def add_note():
   if request.method == 'GET':
      try:
         msg=""
         username = request.args.get('username')
         cmt = request.args.get('comment')
         cook = request.cookies.get('cook')
         username1=my_decrypt(cook,config.key)
         if (username!=username1):
            msg='unauthorized'
         else:
         
             with sql.connect("db/db_notes.sqlite3") as con:
                cur = con.cursor()
                id = random.randint(154877,404842)
                
                cur.execute("INSERT INTO notes (note_id,username,note) VALUES (?,?,?)",(id,username,cmt) )
                
                con.commit()
                msg = "Record successfully added / note id -> "+str(id)
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return msg
         con.close()

@app.route('/get_note',methods = ['POST', 'GET'])
def get_note():
   if request.method == 'GET':
    try:
       con = sql.connect("db/db_notes.sqlite3")
       con.row_factory = sql.Row
       username = request.args.get('username')
       id = request.args.get('id')
       cook = request.cookies.get('cook')
       username1=my_decrypt(cook,config.key)
       if (username!=username1):
        msg='unauthorized'
       else:

       
           cur = con.cursor()
           cur.execute("select note from notes where note_id=?",(id,))
           
           rows = cur.fetchone()[0]
           msg=rows
    except:
         con.rollback()
         msg = "error "
    finally:
        return msg
        con.close()

if __name__ == '__main__':
   app.run(debug = True)
