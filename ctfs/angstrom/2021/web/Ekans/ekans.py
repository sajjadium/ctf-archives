from flask import Flask, request, redirect, make_response
import importlib
import pickle
import base64

app = Flask(__name__)

header = """<title>POKEDEX</title>
<style>
* { font-family: sans-serif }
ul {
	padding: 0;
	display: flex;
	flex-wrap: wrap;
	list-style: none;
	justify-content: center;
}
li {
	height: 5em;
	width: 5em;
	text-align: center;
	line-height: 5em;
	background-image: url(https://cdn.bulbagarden.net/upload/thumb/b/b3/Vermilion_Forest_Ekans.png/250px-Vermilion_Forest_Ekans.png);
	background-size: cover;
	background-repeat: no-repeat;
	background-position: center;
	margin: 1em;
	border: 2px solid black;
}
html {
	background: url(https://wallpaperaccess.com/full/45634.png);
	background-size: cover;
	background-position: center;
	background-attachment: fixed;
}
body {
	text-align: center;
}
h1 {
	text-align: center;
	margin-top: 1em;
}
form {
	text-align: center;
}
</style>"""

@app.route('/', methods=['GET', 'POST'])
def pokedex():
	db = importlib.util.find_spec('db').loader.load_module('db')

	if request.method == "POST":
		response = make_response(redirect('/'))
		response.set_cookie('user', base64.b64encode(pickle.dumps(db.User(request.form.get('username'), request.form.get('password')))))
		return response

	if 'user' not in request.cookies:
		return header+'<h1>Log in to access your pokedex: </h1><form method="POST"><input type="text" name="username" placeholder="Username"> <input type="text" name="password" placeholder="Password"> <button>Log In</button></form>'

	if db.load_user(request).is_admin(): return header+'<h1>ADMINISTRATOR PANEL</h1><img src="https://thumbs.gfycat.com/CarefulConcreteAsianwaterbuffalo-max-1mb.gif">'

	if not db.load_user(request).authenticated(): return header+'<h1>INVALID CREDENTIALS</h1><img src="https://thumbs.gfycat.com/DefiantTanImago-small.gif">'

	return header+'<h1>POKEDEX</h1><ul><li>'+'<li>'.join(p[1] for p in db.POKEMON.items() if p[0] != 1337 or db.load_user(request).is_admin())+'</ul>'

if __name__ == '__main__': app.run(threaded=True)
