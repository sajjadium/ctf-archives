from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from helpsort import helper
import random
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer, index=True)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    password=db.Column(db.String(20),index=True)

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'password':self.password
        }

db.create_all()


@app.route('/')
def index():
    return render_template('server_table.html', title='OUR VALUABLE EMPLOYEES')


@app.route('/api/data')
def data():
    query = User.query
    total_filtered = query.count()
    col_index = request.args.get('order[0][column]')
    flag=1
    if col_index is None:
        col_index=0
        flag=0
    col_name = request.args.get(f'columns[{col_index}][data]')
    users=[user.to_dict() for user in query]
    descending = request.args.get(f'order[0][dir]') == 'desc'
    try:
        if descending:
            users=sorted(users,key=lambda x:helper(x,col_name),reverse=True)
        else :
            users=sorted(users,key=lambda x:helper(x,col_name),reverse=False)
    except:
        pass
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    users=users[start:start+length]
    for user in users:
        del user['password']
    if flag==0:
        random.shuffle(users)
    return {
        'data': users,
        'recordsFiltered': total_filtered,
        'recordsTotal': 500,
        'draw': request.args.get('draw', type=int),
    }

if __name__ == '__main__':
    app.run('0.0.0.0', 16052)
