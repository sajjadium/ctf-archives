from werkzeug.exceptions import abort

from sql import get_sql

import hashlib

def checkSolved(guess_status):
    # guess_status[g_pos] = {"letter":g_char, "state":1}
    isSolved = True
    for i in guess_status:
        if i["state"] != 2:
            isSolved = False

    return isSolved

def getHashString(guess_status):
    # guess_status[g_pos] = {"letter":g_char, "state":1}
    passString = ''
    for i in guess_status:
        if i["state"] == 0:
            passString += '⬛'
        elif i["state"] == 1:
            passString += '🟨'
        elif i["state"] == 2:
            passString += '🟩'
        else:
            passString += '?'

        hashString = hashlib.md5(passString.encode('utf-8')).hexdigest()
    return hashString


def get_answer_info(word_id=None):
    con, cur = get_sql()

    if word_id:
        word = cur.execute(
            """SELECT word FROM answerList WHERE id = (?)""", (word_id,)
        ).fetchone()[0]
    else:
        word_id, word = cur.execute(
            """SELECT id, word FROM answerList ORDER BY RANDOM() LIMIT 1"""
        ).fetchone()

    return word_id, word


def word_is_valid(word):
    con, cur = get_sql()
    cur.execute("""SELECT word FROM wordList WHERE word = (?)""", (word,))
    return bool(cur.fetchone())


def id_or_400(request):
    try:
        game_id = request.get_json(force=True)["id"]
        key = request.get_json(force=True)["key"]

        con, cur = get_sql()
        cur.execute("""SELECT key FROM game WHERE key = (?)""", (key,))
        assert cur.fetchone()[0] == key
        con.close()

        return game_id
    except (AssertionError, KeyError, TypeError):
        abort(400)


def set_finished(game_id):
    con, cur = get_sql()
    cur.execute("""UPDATE game SET finished = true WHERE id = (?) """, (game_id,))
    con.commit()
    con.close()
