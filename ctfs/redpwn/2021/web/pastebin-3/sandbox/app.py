import sqlite3
from flask import (
    Flask,
    render_template_string,
    request,
)

app = Flask(__name__)


def execute(query, params=()):
    con = sqlite3.connect('../db/db.sqlite3')
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    return cur.fetchall()


def get_paste(paste_id):
    results = execute(
        'SELECT paste FROM pastes WHERE id = ?',
        params=(paste_id,)
    )
    if len(results) < 1:
        return 'Paste not found!'
    return results[0][0]


@app.route('/')
def index():
    paste_id = request.args.get('id')
    return render_template_string(
        '''
        <script src="/static/purify.min.js"></script>
        <script>
            (async() => {
                await new Promise(
                    (resolve) => window.addEventListener('load', resolve)
                );
                document.body.innerHTML = DOMPurify.sanitize(
                    `{{ paste | tojson }}`.slice(1, -1)
                );
            })()
        </script>
        ''',
        paste=get_paste(paste_id)
    )
