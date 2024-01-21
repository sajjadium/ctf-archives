from flask import *
from urllib.parse import unquote
import os

def readFile(path):
    f = open(path,'r')
    buf = f.read(0x1000)
    f.close()
    return buf

app = Flask(__name__,static_folder='./static')
app.secret_key = 'REDACTED'
indexFile = readFile('index.html')

@app.before_request
def init_session():
    if('credit' not in session):
        session['credit'] = 100
        session['words_balance'] = 1

@app.get('/')
def index():
    return indexFile

@app.get('/api/stats')
def getStats():
    return {'credit': session['credit'], 'words_balance': session['words_balance']}

@app.post('/api/charge')
def buyWord():
    nwords = request.args.get('nwords')
    if(nwords):
        nwords = int(nwords[:10])
        price = nwords * 10
        if(price <= session['credit']):
            session['credit'] -= price
            session['words_balance'] += nwords
            return {'success': True, 'msg': 'Added to your account!'}
        return {'success': False, 'msg': 'Not enough credit.'}, 402
    else:
        return {'success': False, 'msg': 'Missing parameteres.'}, 400

@app.get('/api/read/<path:name>')
def readNovel(name):
    name = unquote(name)
    if(not name.startswith('public/')):
        return {'success': False, 'msg': 'You can only read public novels!'}, 400
    buf = readFile(name).split(' ')
    buf = ' '.join(buf[0:session['words_balance']])+'... Charge your account to unlock more of the novel!'
    return {'success': True, 'msg': buf}

@app.get('/api/list-public-novels')
def listPublicNovels():
    return os.listdir('./public/')

@app.get('/api/list-private-novels')
def listPrivateNovels():
    return os.listdir('./private/')

if(__name__ == '__main__'):
    app.run('0.0.0.0',port=8000)
