from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
import os
import time
import re
import argparse
import tempfile
import PyPDF2
import string
import random
import datetime
from subprocess import PIPE, Popen
from reportlab.pdfgen import canvas

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = './static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY']='censored'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite://///app/library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
reg=re.compile('[0-9a_f]{32}\Z', re.I)
db = SQLAlchemy(app)
class Users(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     public_id = db.Column(db.Integer)
     name = db.Column(db.String(50))
     password = db.Column(db.String(50))
     admin = db.Column(db.Boolean)
class Tokens(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     token = db.Column(db.String(32))
db.create_all()
def check_valid_token(intoken):
  if bool(reg.match(intoken)):
    rez=Tokens.query.filter(Tokens.token.ilike(intoken)).first()
    print(rez)
    if rez:
      return True
    else:
      return False
  else:
    return False
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
def _get_tmp_filename(suffix=".pdf"):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as fh:
        return fh.name
coords='1x100x100x150x40'
path='./static/'
date=False
output=None
pdf='pf.pdf'
signature='3k.png'

def sign_pdf(inputfile):
    infile=path+inputfile
    pdf=path+get_random_string(8)+'.pdf'
    cmd='unoconv -v -o '+pdf+' -f pdf '+infile
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    page_num, x1, y1, width, height = [int(a) for a in coords.split("x")]
    page_num -= 1

    output_filename = output or "{}_signed{}".format(
        *os.path.splitext(pdf)
    )

    pdf_fh = open(pdf, 'rb')
    sig_tmp_fh = None

    pdf = PyPDF2.PdfFileReader(pdf_fh)
    writer = PyPDF2.PdfFileWriter()
    sig_tmp_filename = None

    for i in range(0, pdf.getNumPages()):
        page = pdf.getPage(i)

        if i == page_num:
            sig_tmp_filename = _get_tmp_filename()
            c = canvas.Canvas(sig_tmp_filename, pagesize=page.cropBox)
            c.drawImage(signature, x1, y1, width, height, mask='auto')
            if date:
                c.drawString(x1 + width, y1, datetime.datetime.now().strftime("%Y-%m-%d"))
            c.showPage()
            c.save()

            sig_tmp_fh = open(sig_tmp_filename, 'rb')
            sig_tmp_pdf = PyPDF2.PdfFileReader(sig_tmp_fh)
            sig_page = sig_tmp_pdf.getPage(0)
            sig_page.mediaBox = page.mediaBox
            page.mergePage(sig_page)

        writer.addPage(page)

    with open(output_filename, 'wb') as fh:
        writer.write(fh)

    for handle in [pdf_fh, sig_tmp_fh]:
        if handle:
            handle.close()
    if sig_tmp_filename:
        os.remove(sig_tmp_filename)
    return output_filename
def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      token = None
      if 'x-access-tokens' in request.headers:
         token = request.headers['x-access-tokens']

      if not token:
         return jsonify({'message': 'a valid token is missing'})

      try:
         data = jwt.decode(token, app.config['SECRET_KEY'])
         current_user = Users.query.filter_by(public_id=data['public_id']).first()
      except:
         return jsonify({'message': 'token is invalid'})

      return f(current_user, *args, **kwargs)
   return decorator
@app.route('/', methods=['GET', 'POST'])
def home():
  return jsonify({'message': 'Welcome \O// '})

@app.route('/register', methods=['GET', 'POST'])
def signup_user():  
 data = request.get_json()  

 hashed_password = generate_password_hash(data['password'], method='sha256')
 
 new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False) 
 db.session.add(new_user)  
 db.session.commit()    

 return jsonify({'message': 'registered successfully'})
@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
 
  auth = request.authorization   

  if not auth or not auth.username or not auth.password:  
     return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

  user = Users.query.filter_by(name=auth.username).first()   
     
  if check_password_hash(user.password, auth.password):  
     token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
     return jsonify({'token' : token.decode('UTF-8')}) 

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
   if current_user.admin:
   
       users = Users.query.all() 

       result = []   

       for user in users:   
           user_data = {}   
           user_data['public_id'] = user.public_id
           user_data['name'] = user.name 
           user_data['admin'] = user.admin 
           
           result.append(user_data)   
   else:
      return jsonify({'error': "not admin"})

   return jsonify({'users': result})
@app.route('/role_user', methods=['GET'])
@token_required
def role(current_user):
    if not(current_user.admin):
        return jsonify({'role': "ROLE_USER"})
    else:
       return jsonify({'role': "ROLE_ADMIN"})
@app.route('/share_file', methods=['GET', 'POST'])
@token_required
def upload_file(current_user):
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': "upload file..."})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': "no filename !!"})
        if file and allowed_file(file.filename):
            ext=file.filename.rsplit('.', 1)[1]
            relfile=get_random_string(8)+'.'+ext
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], relfile))
            if not(request.args.get('sign_token')) or (not(check_valid_token(request.args.get('sign_token')))):
              return jsonify({'file': "/static/"+relfile})
            else:
              signed_file=sign_pdf(relfile)
              return jsonify({'signed_file':signed_file})
        else:
          return jsonify({'error': "go away!!"})
@app.route('/sign_tokens', methods=['GET'])
@token_required
def sign_tokens(current_user):
  if current_user.admin:
   
       tokens = Tokens.query.all() 

       result = []   

       for tok in tokens:   
           token_data = {}   
           token_data['id'] = tok.id
           token_data['token'] = tok.token 
           
           result.append(token_data)
  else:
      return jsonify({'error': "not admin"})

  return jsonify({'users': result})
@app.route('/add_tokens', methods=['PUT'])
@token_required
def add_tok(current_user):
  if current_user.admin:
    try:
      data = request.get_json() 
      new_token = Tokens(token=data['token']) 
      db.session.add(new_token)  
      db.session.commit()
    except:
      return jsonify({'error': "//"})
    return jsonify({'message': "Added successfully"})
  else:
    return jsonify({'error': "not admin"})
if __name__ == '__main__':
   app.run(host="0.0.0.0")