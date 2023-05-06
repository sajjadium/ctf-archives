import schedule, signal, queue, threading, time,sys, os, datetime, multiprocessing, requests, telegram, jsonify, threading, requests, re, hashlib, hmac, random, base64

from threading import Thread
import flask
from flask import Flask, request, render_template, json
from flask_bootstrap import Bootstrap
from flask_cors import CORS
import logging
import logging.config
from dotenv import load_dotenv

from datamodel import Database, Base, Subscriber
from coinapi import getCoinInfo
from rollback import RunRollbackDB, RunbackupDB

load_dotenv()

logging.config.fileConfig('./logging.conf', defaults={'logfilename1': './logs/KillCoinapi.log'})
logger = logging.getLogger('KillCoinapi')  

privateKey = b'let\'sbitcorinparty'

status = {
    'success' : {'message':'success'},
    'false' : {'message':'false'},
    'error' : {'message': 'error'},
    'key' : {'message': 'Key error'},
    'sign'  : {'message': 'Not Allowed'},
    'email' : {'message': 'Email invalid'},
    'admin' : {'message': 'Do you wanna admin cherry? You need to cool down bro! Your head is too heavy. Go outside. Your weight is '}
}

class Activity():
    def __init__(self):
        self.engine = Database.dbEngine
        Base.metadata.create_all(self.engine, Base.metadata.tables.values(), checkfirst=True)
        self.session = Database.session()
        self.dbHash = hashlib.md5(open(os.environ['DBFILE'],'rb').read()).hexdigest()
        self.integrityKey = hashlib.sha512((self.dbHash).encode('ascii')).hexdigest()
        self.subscriberObjs = self.session.query(Subscriber).all()
        self.backupedHash = ''
    
    def DbBackupRunner(self):
        self.dbHash = hashlib.md5(open(os.environ['DBFILE'],'rb').read()).hexdigest()
        self.backupedHash = RunbackupDB(self.backupedHash, self.dbHash)

    def Commit(self):
        try:
            self.session.commit()


        except Exception as e :
            err = 'Error On  {f} : {c}, Message, {m}, Error on line {l}'.format(f = sys._getframe().f_code.co_name ,c = type(e).__name__, m = str(e), l = sys.exc_info()[-1].tb_lineno)
            RunRollbackDB(self.dbHash)
            self.UpdateKey()
            self.Commit() 

    def UpdateKey(self):
        file = open(os.environ['DBFILE'],'rb').read()
        self.dbHash = hashlib.md5(file).hexdigest()
        self.integrityKey = hashlib.sha512((self.dbHash).encode('ascii')).hexdigest()
    
    def IntegrityCheckWorker(self):
        key = self.integrityKey
        dbHash = hashlib.md5(open(os.environ['DBFILE'],'rb').read()).hexdigest()

        self.IntegrityCheck(key, dbHash)
    

    def IntegrityCheck(self,key, dbHash): 

        if self.integrityKey == key:
            pass
        else:
            return json.dumps(status['key'])
        if self.dbHash != dbHash:
            flag = RunRollbackDB(dbHash)
            logger.debug('DB File changed!!'+dbHash)
            file = open(os.environ['DBFILE'],'rb').read()
            self.dbHash = hashlib.md5(file).hexdigest()
            self.integrityKey = hashlib.sha512((self.dbHash).encode('ascii')).hexdigest()
            return flag
        return "DB is safe!"

    def AddSubscriber(self, email):
        sub_time = time.strftime("%Y-%m-%d %H:%M:%S")
        subscriberObj = Subscriber(email, sub_time)
        self.session.add(subscriberObj)
        self.Commit()
        return json.dumps(status['success'])


    def ScheduleWorker(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run(self):
        threading.Thread(target=self.ScheduleWorker).start()
        schedule.every(int(os.environ['CHKTIME'])).seconds.do(self.IntegrityCheckWorker)
        # schedule.every(5).minutes.do(self.DbBackupRunner)
        schedule.every(2).seconds.do(self.UpdateKey)
        schedule.every(2).seconds.do(self.DbBackupRunner)

app = Flask(__name__)

Bootstrap(app) 
cors = CORS(app, resources={r"/*": {"origins": "*"}})


activity = Activity()
activity.run()


def valid_download(src):
    if( src != None ):
        return True
    else:
        return False

def WriteFile(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open('backup/'+local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)

def LanguageNomarize(request):
    if request.headers.get('Lang') is None:
        return "en"
    else:
        regex = '^[!@#$\\/.].*/.*' # Easy~~
        language = request.headers.get('Lang')
        language = re.sub(r'%00|%0d|%0a|[!@#$^]|\.\./', '', language)
        if re.search(regex,language):
            return request.headers.get('Lang')
        
        try:
            data = requests.get(request.host_url+language, headers=request.headers)
            if data.status_code == 200:
                return data.text
            else:
                return request.headers.get('Lang')
        except:
            return request.headers.get('Lang')

def list_routes():
    return ['%s' % rule for rule in app.url_map.iter_rules()]

def SignCheck(request):
    sigining = hmac.new( privateKey , request.query_string, hashlib.sha512 )

    if sigining.hexdigest() != request.headers.get('Sign'):
        return False
    else:
        return True

@app.route('/', methods=['GET'])
def index():
    # information call
    information = list_routes()
    information.append(request.host_url)
    return str(information)

@app.route('/en', methods=['GET'])
def en():
    return 'en'

@app.route('/jp', methods=['GET'])
def jp():
    return 'jp'

@app.route('/coin', methods=['GET'])
def coin():
    try:
        response = app.response_class()
        language = LanguageNomarize(request)
        response.headers["Lang"] =  language
        data = getCoinInfo()
        response.data = json.dumps(data)
        return response
    except Exception as e :
        err = 'Error On  {f} : {c}, Message, {m}, Error on line {l}'.format(f = sys._getframe().f_code.co_name ,c = type(e).__name__, m = str(e), l = sys.exc_info()[-1].tb_lineno)
        logger.error(err)


@app.route('/download', methods=['GET','POST'])
def download():
    try:
        if request.headers.get('Sign') == None:
            return json.dumps(status['sign'])
        else:
            if SignCheck(request):
                pass
            else:
                return json.dumps(status['sign'])

        if request.method == 'GET':
            src = request.args.get('src')

            if valid_download(src):
                pass
            else:
                return json.dumps(status.get('false'))
                
        elif request.method == 'POST':
            if valid_download(request.form['src']):
                pass
            else:
                return json.dumps(status.get('false'))

        WriteFile(src)
        return json.dumps(status.get('success'))
    except Exception as e :
        err = 'Error On  {f} : {c}, Message, {m}, Error on line {l}'.format(f = sys._getframe().f_code.co_name ,c = type(e).__name__, m = str(e), l = sys.exc_info()[-1].tb_lineno)
        logger.error(err)
        return json.dumps(status.get('false')), 404

@app.route('/addsub', methods=['GET'])
def addsub():
    try:
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        email = request.args.get('email')
        if (email is None) or (len(email)>100):
            return json.dumps(status['email'])

        if re.search(regex,email):
            return activity.AddSubscriber(email)
        else:
            return json.dumps(status['email'])
    except Exception as e :
        err = 'Error On  {f} : {c}, Message, {m}, Error on line {l}'.format(f = sys._getframe().f_code.co_name ,c = type(e).__name__, m = str(e), l = sys.exc_info()[-1].tb_lineno)
        logger.error(err)

@app.route('/integrityStatus', methods=['GET'])
def integritycheck():
    data = {'db':'database/master.db','dbhash':activity.dbHash}
    data = json.dumps(data)
    return data

@app.route('/rollback', methods=['GET'])
def rollback():
    try:
        if request.headers.get('Sign') == None:
            return json.dumps(status['sign'])
        else:
            if SignCheck(request):
                pass
            else:
                return json.dumps(status['sign'])

        if request.headers.get('Key') == None:
            return json.dumps(status['key'])
        result  = activity.IntegrityCheck(request.headers.get('Key'),request.args.get('dbhash'))
        return result
    except Exception as e :
        err = 'Error On  {f} : {c}, Message, {m}, Error on line {l}'.format(f = sys._getframe().f_code.co_name ,c = type(e).__name__, m = str(e), l = sys.exc_info()[-1].tb_lineno)
        logger.error(err)
        return json.dumps(status['error']), 404

@app.before_request
def before_request():
    if str(request.url_rule) not in list_routes():
        return json.dumps(status['error']), 404
    if request.headers.get('Sign') != None:
        if len(request.headers)>8:
            result = status['admin']
            result['message'] = result['message']+str(len(request.headers))
            return json.dumps(result), 404

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response

@app.errorhandler(404)
def page_not_found(e):
    return json.dumps(status['error']), 404

