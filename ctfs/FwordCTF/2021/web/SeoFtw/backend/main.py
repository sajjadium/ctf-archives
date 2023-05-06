from flask import Flask, jsonify,Response, request,g
from neo4j import GraphDatabase, basic_auth
import os 
from flask_cors import CORS
import ipaddress

app = Flask(__name__, static_url_path='/static/')
CORS(app)

url = os.getenv("NEO4J_URI", "neo4j://neo4j")
username = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "fword")
database = os.getenv("NEO4J_DATABASE", "neo4j")
port = os.getenv("PORT", 8080)

driver = GraphDatabase.driver(url, auth=basic_auth(username, password),encrypted=False)

def get_db():
	neo4j_db = driver.session(database=database)
	return neo4j_db

@app.route("/secret")
def secret():
	ip=request.remote_addr
	an_address = ipaddress.ip_address(ip)
	a_network = ipaddress.ip_network('172.16.0.0/24')
	if(an_address in a_network):
		db=get_db()
		result = db.read_transaction(lambda tx: list(tx.run("MATCH (body:Anime) WHERE body.name=\""+request.args.get("name")+"\" RETURN body",{})))
		print(result)
		return jsonify({"result":result})
	else:
		return jsonify({"result":"No No little hacker"})
@app.route("/")
def animes():
	# implement retrieving best animes from neo4j but now let's just hardcode it x)
	return jsonify({"animes":["Naruto","HxH","Hyouka","All Isekai Animes :)"]})

if __name__ == '__main__':
	app.run()
