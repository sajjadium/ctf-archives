from flask import Flask, request
from flask_caching import Cache
from redis import Redis

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'redis','CACHE_REDIS_HOST':'redis'})

redis = Redis('redis')

@app.route('/',methods=["GET"])
def index():
    return "Welcome to ctf-cdn"


@app.route('/api/upload',methods=["POST"])
def upload():
    name, contents = (request.form.get('name'),request.form.get('contents'))
    redis.set(f"uploads_{name}",contents)
    return "OK"

@app.route('/uploads/<path:name>',methods=["GET"])
@cache.cached(timeout=30)
def uploads(name):
    d = redis.get(f"uploads_{name}")
    if d != None:
        return d
    else:
        return "Nothing with the name " + name
