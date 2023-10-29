import sqlite3
from flask import Flask, request, g

DATABASE = './database.db'
app = Flask(__name__)

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
@app.route('/')
def index():
    return "This is for admins only!"

@app.get('/secret')
def secret():
    cur = get_db().execute("SELECT details FROM illegalrecipes WHERE name='casu marzu'")
    recipe = cur.fetchone()
    cur.close()
    return str(recipe)

@app.get('/recipe')
def getRecipe():
    name = request.args.get('name')
    cur = get_db().execute("SELECT details FROM recipes WHERE name=?", (name,))
    recipe = cur.fetchone()
    cur.close()
    return str(recipe)
    
if __name__ == "__main__":
    init_db()
    app.run("0.0.0.0")
