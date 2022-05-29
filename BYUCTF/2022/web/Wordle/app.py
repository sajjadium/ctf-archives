import json
import uuid

from flask import Flask, render_template, request, abort, make_response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

from utils import set_finished, word_is_valid, id_or_400, get_answer_info, getHashString, checkSolved
from sql import get_sql

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
CORS(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
)


def api_response(json_data):
    resp = make_response(json.dumps(json_data))
    resp.content_type = "application/json; charset=utf-8"
    return resp


@app.context_processor
def inject_debug():
    return dict(debug=app.debug)


# Frontend views
@app.route("/")
def index():
    return render_template("index.html")


# API endpoints
@app.route("/api/v1/start_game/", methods=["POST"])
#@limiter.limit("4/second;120/minute;600/hour;4000/day")
def start_game():
    """
    Starts a new game
    """
    word_id = None

    con, cur = get_sql()

    key = str(uuid.uuid4())

    word_id, word = get_answer_info(word_id)

    cur.execute("""INSERT INTO game (word, key) VALUES (?, ?)""", (word, key))
    con.commit()
    con.close()

    return api_response({"id": cur.lastrowid, "key": key, "wordID": word_id})


@app.route("/api/v1/guess/", methods=["POST"])
def guess_word():
    try:
        guess = request.get_json(force=True)["guess"]
        assert len(guess) == 5
        assert guess.isalpha()
        assert word_is_valid(guess)
    except AssertionError:
        return abort(400, "Invalid word")

    game_id = id_or_400(request)

    con, cur = get_sql()
    cur.execute(
        """SELECT word, guesses, finished FROM game WHERE id = (?)""", (game_id,)
    )
    answer, guesses, finished = cur.fetchone()

    guesses = guesses.split(",")

    if len(guesses) > 6 or finished:
        return abort(403)

    guesses.append(guess)
    guesses = ",".join(guesses)

    if guesses[0] == ",":
        guesses = guesses[1:]

    cur.execute("""UPDATE game SET guesses = (?) WHERE id = (?)""", (guesses, game_id))
    con.commit()
    con.close()

    guess_status = [{"letter": g_char, "state": 0} for g_char in guess]
    guessed_pos = set()

    for a_pos, a_char in enumerate(answer):
        if a_char == guess[a_pos]:
            guessed_pos.add(a_pos)
            guess_status[a_pos] = {
                "letter": guess[a_pos],
                "state": 2,
            }

    for g_pos, g_char in enumerate(guess):
        if g_char in answer and guess_status[g_pos]["state"] == 0:
            positions = []
            f_pos = answer.find(g_char)
            while f_pos != -1:
                positions.append(f_pos)
                f_pos = answer.find(g_char, f_pos + 1)

            for pos in positions:
                if pos not in guessed_pos:
                    guess_status[g_pos] = {
                        "letter": g_char,
                        "state": 1,
                    }
                    guessed_pos.add(pos)
                    break

    hashString = getHashString(guess_status)
    gameSolved = checkSolved(guess_status)
    respObj = {
        "gameSolved": gameSolved,
        "hashString": hashString,
    }
    return api_response(respObj)


@app.route("/api/v1/finish_game/", methods=["POST"])
def finish_game():
    game_id = id_or_400(request)
    set_finished(game_id)

    con, cur = get_sql()
    cur.execute(
        """SELECT word, guesses, finished FROM game WHERE id = (?)""", (game_id,)
    )
    answer, guesses, finished = cur.fetchone()
    guesses = guesses.split(",")

    if answer == guesses[-1]:
        answer = "Nice Job! byuctf{REDACTED}"
    else:
        answer = "Sorry! Try again."

    return api_response({"answer": answer})


if __name__ == "__main__":
    app.run()
