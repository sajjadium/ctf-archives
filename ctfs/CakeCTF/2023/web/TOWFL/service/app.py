#!/usr/bin/env python3
import flask
import json
import lorem
import os
import random
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/api/start", methods=['POST'])
def api_start():
    if 'eid' in flask.session:
        eid = flask.session['eid']
    else:
        eid = flask.session['eid'] = os.urandom(32).hex()

    # Create new challenge set
    db().set(eid, json.dumps([new_challenge() for _ in range(10)]))
    return {'status': 'ok'}

@app.route("/api/question/<int:qid>", methods=['GET'])
def api_get_question(qid: int):
    if qid <= 0 or qid > 10:
        return {'status': 'error', 'reason': 'Invalid parameter.'}
    elif 'eid' not in flask.session:
        return {'status': 'error', 'reason': 'Exam has not started yet.'}

    # Send challenge information without answers
    chall = json.loads(db().get(flask.session['eid']))[qid-1]
    del chall['answers']
    del chall['results']
    return {'status': 'ok', 'data': chall}

@app.route("/api/submit", methods=['POST'])
def api_submit():
    if 'eid' not in flask.session:
        return {'status': 'error', 'reason': 'Exam has not started yet.'}

    try:
        answers = flask.request.get_json()
    except:
        return {'status': 'error', 'reason': 'Invalid request.'}

    # Get answers
    eid = flask.session['eid']
    challs = json.loads(db().get(eid))
    if not isinstance(answers, list) \
       or len(answers) != len(challs):
        return {'status': 'error', 'reason': 'Invalid request.'}

    # Check answers
    for i in range(len(answers)):
        if not isinstance(answers[i], list) \
           or len(answers[i]) != len(challs[i]['answers']):
            return {'status': 'error', 'reason': 'Invalid request.'}

        for j in range(len(answers[i])):
            challs[i]['results'][j] = answers[i][j] == challs[i]['answers'][j]

    # Store information with results
    db().set(eid, json.dumps(challs))
    return {'status': 'ok'}

@app.route("/api/score", methods=['GET'])
def api_score():
    if 'eid' not in flask.session:
        return {'status': 'error', 'reason': 'Exam has not started yet.'}

    # Calculate score
    challs = json.loads(db().get(flask.session['eid']))
    score = 0
    for chall in challs:
        for result in chall['results']:
            if result is True:
                score += 1

    # Is he/she worth giving the flag?
    if score == 100:
        flag = os.getenv("FLAG")
    else:
        flag = "Get perfect score for flag"

    # Prevent reply attack
    flask.session.clear()

    return {'status': 'ok', 'data': {'score': score, 'flag': flag}}


def new_challenge():
    """Create new questions for a passage"""
    p = '\n'.join([lorem.paragraph() for _ in range(random.randint(5, 15))])
    qs, ans, res = [], [], []
    for _ in range(10):
        q = lorem.sentence().replace(".", "?")
        op = [lorem.sentence() for _ in range(4)]
        qs.append({'question': q, 'options': op})
        ans.append(random.randrange(0, 4))
        res.append(False)
    return {'passage': p, 'questions': qs, 'answers': ans, 'results': res}

def db():
    """Get connection to DB"""
    if getattr(flask.g, '_redis', None) is None:
        flask.g._redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    return flask.g._redis

if __name__ == '__main__':
    app.run()
