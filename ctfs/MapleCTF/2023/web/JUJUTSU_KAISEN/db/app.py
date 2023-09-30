from flask import Flask
from flask_graphql import GraphQLView as View
from schema import schema
from database import db
from configuration import PORT


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jjk_db.sqlite3'

app.add_url_rule("/", view_func=View.as_view("graphql", graphiql=False, schema=schema))

db.init_app(app)

with app.app_context():
    db.create_all()
    
    with open("init.sql", "r") as f:
        init_script = f.read()

    conn = db.engine
    statements = init_script.split(";")
    for statement in statements:
        conn.execute(statement)


@app.teardown_appcontext
def shutdown_session(Error=None):
    db.session.remove()


def main():
    app.run(port=PORT, debug=False, host='0.0.0.0')


if __name__ == "__main__":
    main()
