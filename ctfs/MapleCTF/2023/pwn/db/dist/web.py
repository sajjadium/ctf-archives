import functools

import bottle
from bottle import abort, request, response, route, run, template, view

from db import Db

db = Db('film.db')

@route('/')
@view('index.html')
def index():
    offset = int(request.query.skip or 0)
    term = request.query.term or ''
    films = db.execute(
        b"select tconst, title, year from title\
        where title like '%"+term.encode('latin1')+b"%'\
        limit 50 offset "+str(offset).encode('latin1')+b";"
    )
    return dict(term=term, films=films)

@route('/film/<id:int>')
@view('film.html')
def film(id):
    results = db.execute(b"select title, year from title where tconst="+str(id).encode('latin1')+b";")
    if len(results) == 0:
        abort(404, 'Film not found')
    title, year = results[0]
    names = db.execute(
        b"select name.nconst, name.name, category.name from principal\
        join name on principal.nconst=name.nconst\
        join category on id=category\
        where tconst="+str(id).encode('latin1')+b";"
    )
    return dict(title=title, year=year, names=names)

@route('/person/<id:int>')
@view('person.html')
def film(id):
    results = db.execute(b"select name, birth_year from name where nconst="+str(id).encode('latin1')+b";")
    if len(results) == 0:
        abort(404, 'Person not found')
    name, birth_year = results[0]
    films = db.execute(
        b"select title.tconst, title, year from principal\
        join title on principal.tconst=title.tconst\
        where nconst="+str(id).encode('latin1')+b";"
    )
    return dict(name=name, birth_year=birth_year, films=films)

bottle.FormsDict.input_encoding = 'latin1'
run(host='0.0.0.0', port=8080)
