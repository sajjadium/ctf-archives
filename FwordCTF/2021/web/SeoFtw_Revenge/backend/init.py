import os
from neo4j import GraphDatabase, basic_auth

url = os.getenv("NEO4J_URI", "neo4j://neo4j")
username = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "fword")
database = os.getenv("NEO4J_DATABASE", "neo4j")

driver = GraphDatabase.driver(url, auth=basic_auth(username, password),encrypted=False)

def get_db():
        neo4j_db = driver.session(database=database)
        return neo4j_db

def init():
        db = get_db()
        result = db.write_transaction(lambda tx: list(tx.run("CREATE (body:Anime) SET body.name = $name RETURN body.name",{"name":"Naruto"})))
        print(result)
init()
