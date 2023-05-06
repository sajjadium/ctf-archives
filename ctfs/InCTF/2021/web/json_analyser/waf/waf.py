from flask import Flask, request
from flask_cors import CORS
import ujson
import json
import re
import os

os.environ['subscription_code'] = '[REDACTED]'
app=Flask(__name__)
cors = CORS(app)
CORS(app)
cors = CORS(app, resources={
    r"/verify_roles": {
       "origins": "*"
    }
})

@app.route('/verify_roles',methods=['GET','POST'])
def verify_roles():
    no_hecking=None
    role=request.args.get('role')
    if "superuser" in role:
        role=role.replace("superuser",'')
    if " " in role:
        return "n0 H3ck1ng"
    if len(role)>30:
        return "invalid role"
    data='"name":"user","role":"{0}"'.format(role)
    no_hecking=re.search(r'"role":"(.*?)"',data).group(1)
    if(no_hecking)==None:
        return "bad data :("
    if no_hecking == "superuser":
        return "n0 H3ck1ng"
    data='{'+data+'}'
    try:
        user_data=ujson.loads(data)
    except:
        return "bad format" 
    role=user_data['role']
    user=user_data['name']
    if (user == "admin" and role == "superuser"):
        return os.getenv('subscription_code')
    else:
        return "no subscription for you"

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5555)
