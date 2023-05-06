import re
import sqlite3
from flask import Flask, render_template, url_for, request, redirect, make_response

app = Flask(__name__)

blacklist = ["ABORT", "ACTION", "ADD", "AFTER", "ALL", "ALTER", "ALWAYS", "ANALYZE", "AND", "AS", "ASC", "ATTACH", "AUTOINCREMENT", "BEFORE", "BEGIN", "BETWEEN", "CASCADE", "CASE", "CAST", "CHECK", "COLLATE", "COLUMN", "COMMIT", "CONFLICT", "CONSTRAINT", "CREATE", "CROSS", "CURRENT", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "DATABASE", "DEFAULT", "DEFERRABLE", "DEFERRED", "DELETE", "DESC", "DETACH", "DISTINCT", "DO", "DROP", "EACH", "ELSE", "END", "ESCAPE", "EXCEPT", "EXCLUDE", "EXCLUSIVE", "EXISTS", "EXPLAIN", "FAIL", "FILTER", "FIRST", "FOLLOWING", "FOR", "FOREIGN", "FROM", "FULL", "GENERATED", "GLOB", "GROUP", "GROUPS", "HAVING", "IF", "IGNORE", "IMMEDIATE", "IN", "INDEX", "INDEXED", "INITIALLY", "INNER", "INSERT", "INSTEAD", "INTERSECT", "INTO", "IS", "ISNULL", "JOIN", "KEY", "LAST", "LEFT", "LIKE", "LIMIT", "MATCH", "MATERIALIZED", "NATURAL", "NO", "NOT", "NOTHING", "NOTNULL", "NULL", "NULLS", "OF", "OFFSET", "ON", "OR", "ORDER", "OTHERS", "OUTER", "OVER", "PARTITION", "PLAN", "PRAGMA", "PRECEDING", "PRIMARY", "QUERY", "RAISE", "RANGE", "RECURSIVE", "REFERENCES", "REGEXP", "REINDEX", "RELEASE", "RENAME", "REPLACE", "RESTRICT", "RETURNING", "RIGHT", "ROLLBACK", "ROW", "ROWS", "SAVEPOINT", "SELECT", "SET", "TABLE", "TEMP", "TEMPORARY", "THEN", "TIES", "TO", "TRANSACTION", "TRIGGER", "UNBOUNDED", "UNION", "UNIQUE", "UPDATE", "USING", "VACUUM", "VALUES", "VIEW", "VIRTUAL", "WHEN", "WHERE", "WINDOW", "WITH", "WITHOUT"] 

def checkCreds(username, password):
	con = sqlite3.connect('database.db')
	cur = con.cursor()
	for n in blacklist:
		regex = re.compile(n, re.IGNORECASE)
		username = regex.sub("", username)
	for n in blacklist:
		regex = re.compile(n, re.IGNORECASE)
		password = regex.sub("", password)
	print(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")		
	try:
		content = cur.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'").fetchall()
	except:
		return False
	cur.close()
	con.close()
	if content == []:
		return False
	else:
		return True

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/user', methods=['POST'])
def user():
	if request.method == 'POST': 
		username = request.values['username']
		password = request.values['password']
		if checkCreds(username, password) == True:
			return render_template("user.html")
		else:
			return "Error"
	else:
		return render_template("user.html")


