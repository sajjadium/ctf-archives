from db import create_connection, insertRegistration, create_db, getRequests, validateSession, validateUser
from flask import Flask, request, send_file, render_template, make_response, redirect, url_for, abort
from marshmallow import Schema, fields
from flask_cors import CORS
import json, hashlib

app = Flask(__name__)
CORS(app)
database = r"sqlite.db"

class RegistrationInputSchema(Schema):
            rperiod = fields.Int(required=True)
            rtype = fields.Str(required=True)
            name = fields.Str(required=True)
            make = fields.Str(required=True)
            streetAddress = fields.Str(required=True)
            city = fields.Str(required=True)
            province = fields.Str(required=True)
            country = fields.Str(required=True)
            planet = fields.Str(required=False)
            year = fields.Int(required=True)
            make = fields.Str(required=True)
            model = fields.Str(required=True)
            color = fields.Str(required=True)

registrationSchema = RegistrationInputSchema()

@app.route('/index.js', methods=['GET'])
def indexjs():
    print("[+] index.js")
    return send_file('www/index.js', download_name='index.js')

@app.route('/', methods=['GET'])
def indexhtml():
    return send_file('www/index.html', download_name='index.html')

@app.route('/styles.css', methods=['GET'])
def stylecss():
    return send_file('www/styles.css', download_name='www/styles.css')



@app.route('/register', methods=['POST'])
def register():

    conn = create_connection(database)
    try:
        if(request.content_type.startswith('application/x-www-form-urlencoded')):
            errors = registrationSchema.validate(request.form)
            if errors:
                abort(400, str(errors))
            rperiod: int = request.form.get('rperiod')
            rtype: str = request.form.get('rtype')
            name: str = request.form.get('name')
            make: str = request.form.get('make')
            address = {}
            address['streetAddress']: str = request.form.get('streetAddress')
            address['city']:str = request.form.get('city')
            address['province']:str = request.form.get('province')
            address['country']:str = request.form.get('country')
            address['planet']:str = request.form.get('planet')
            year: int = request.form.get('year')
            make: str = request.form.get('make')
            model: str = request.form.get('model')
            color:str = request.form.get('color')
            insertRegistration(conn, (rperiod, 
                                  rtype,
                                  name,
                                  json.dumps(address),
                                  year,
                                  make,
                                  model,
                                  color))
            conn.commit()
        elif(request.content_type.startswith('application/json')):
            jsonData = json.loads(request.get_data().decode('utf-8'))
            insertRegistration(conn, (jsonData['rperiod'],
                                  jsonData['rtype'],
                                  jsonData['name'],
                                  json.dumps(jsonData['address']),
                                  jsonData['year'],
                                  jsonData['make'],
                                  jsonData['model'],
                                  jsonData['color']))
            conn.commit()
    finally:
        conn.close()
    return send_file('www/success.html', download_name='success.html')

@app.route('/node_modules/augmented-ui/aug-core.min.css', methods=['GET'])
def aug():
    return send_file('node_modules/augmented-ui/aug-core.min.css', download_name='aug-core.min.css')

@app.route('/admin', methods=['GET'])
def admin():
    conn = create_connection(database)
    if validateSession(conn, (request.cookies.get('session'),)):
        return send_file('www/admin.html', download_name='admin.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = create_connection(database)
    if request.method == 'GET':
        return send_file('www/login.html', download_name='login.html')
    else:
        sessionCookie = validateUser(conn, (request.form.get('username'), hashlib.md5(bytes(request.form.get('password'), "utf-8")).digest().hex()))

        conn.commit()
        if sessionCookie:
            resp = make_response(redirect(url_for('admin')))
            resp.set_cookie('session', sessionCookie)
            return resp
        else:
            return send_file('www/login.html', download_name='login.html')

@app.route('/requests', methods=['GET'])
def responses():
    conn = create_connection(database)
    if validateSession(conn, (request.cookies.get('session'),)):
        return json.dumps(getRequests(conn))
    else:
        return redirect(url_for('login'))

app.run(host='0.0.0.0', port=8000)

