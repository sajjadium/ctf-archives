from flask import Flask, render_template, url_for, redirect, request
from neo4j import GraphDatabase

app = Flask(__name__)

URI = "bolt://localhost:7687"
AUTH = ("", "")


def query(input_query):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        session = driver.session()
        tx = session.begin_transaction()
        records = [t for t in tx.run(input_query)]
        tx.rollback()
        return records


@app.route("/")
def index():
    distance = request.args.get('distance')
    stations = query('MATCH (n:Station) RETURN n.id, n.name ORDER BY n.id DESC;')
    return render_template('index.html', stations=stations, distance=distance)


@app.route("/search", methods=['POST'])
def search():
    start = request.form["startStation"]
    end = request.form['endStation']
    distance_query = f'MATCH (n {{id: {start}}})-[p *bfs]-(m {{id: {end}}}) RETURN size(p) AS distance;'
    distance = query(distance_query)
    if len(distance) == 0:
        distance = 'unknown'
    else:
        distance = int(distance[0]['distance'])
    return redirect(url_for('.index', distance=distance))
