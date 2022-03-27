import os
import hashlib
import shutil
import datetime
import uvicorn
import logging

from urllib.parse import unquote
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

templates = Jinja2Templates(directory='./')
templates.env.autoescape = False

def index(request):
    context = {}
    memoList = []
    
    try:
        clientId = getClientID(request.client.host)
        path = './memo/' + clientId
        
        if os.path.exists(path):
            memoList = os.listdir(path)
        
        context['request'] = request
        context['ip'] = request.client.host
        context['clientId'] = clientId
        context['memoList'] = memoList
        context['count'] = len(memoList)
    
    except:
        pass
    
    return templates.TemplateResponse('/view/index.html', context)

def save(request):
    context = {}
    memoList = []
    
    try:
        context['request'] = request
        context['ip'] = request.client.host
        
        contents = request.query_params['contents']
        path = './memo/' + getClientID(request.client.host) + '/'
        
        if os.path.exists(path) == False:
            os.makedirs(path, exist_ok=True)
        
        memoList = os.listdir(path)
        idx = len(memoList)
        
        if idx >= 3:
            return HTMLResponse('Memo Full')
        elif len(contents) > 100:
            return HTMLResponse('Contents Size Error (MAX:100)')
        
        filename = str(idx) + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            
        f = open(path + filename, 'w')
        f.write(contents)
        f.close()
    
    except:
        pass
    
    return HTMLResponse('Save Complete')

def reset(request):
    context = {}
    
    try:
        context['request'] = request
            
        clientId = getClientID(request.client.host)
        path = './memo/' + clientId
            
        if os.path.exists(path) == False:
            return HTMLResponse('Memo Null')
        
        shutil.rmtree(path)
            
    except:
        pass
    
    return HTMLResponse('Reset Complete')

def view(request):
    context = {}

    try:
        context['request'] = request
        clientId = getClientID(request.client.host)

        if '&' in request.url.query or '.' in request.url.query or '.' in unquote(request.query_params[clientId]):
            raise
        
        filename = request.query_params[clientId]
        path = './memo/' + "".join(request.query_params.keys()) + '/' + filename
        
        f = open(path, 'r')
        contents = f.readlines()
        f.close()
        
        context['filename'] = filename
        context['contents'] = contents
    
    except:
        pass
    
    return templates.TemplateResponse('/view/view.html', context)

def getClientID(ip):
    key = ip + '_' + os.getenv('SALT')
    
    return hashlib.md5(key.encode('utf-8')).hexdigest()

routes = [
    Route('/', endpoint=index),
    Route('/view', endpoint=view),
    Route('/reset', endpoint=reset),
    Route('/save', endpoint=save),
    Mount('/static', StaticFiles(directory='./static'), name='static')
]

app = Starlette(debug=False, routes=routes)

if __name__ == "__main__":
    logging.info("Starting Starlette Server")
    uvicorn.run(app, host="0.0.0.0", port=11000)