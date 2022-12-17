const express = require("express");
const fetch = (...args) =>
	import("node-fetch").then(({ default: fetch }) => fetch(...args));
const crypto = require("crypto");
const session = require("express-session");
const urlencoded = require("body-parser");

const admin = require("./admin.js");
const DB = require("./db.js");

const PASSWORD = DB.PASSWORD;
const ADMIN_PASSWORD = crypto.randomBytes(16).toString("hex");

const userDB = new Map();

userDB.set("admin", ADMIN_PASSWORD);

const app = new express();

app.use(
	session({
		secret: "secret",
		cookie: { secure: false },
	})
);

app.use(express.json());
app.use(urlencoded());

app.use((req, res, next) => {
	res.setHeader(
		"Content-Security-Policy",
		"default-src 'self'" // NO HACKING!
	);
	next();
});

app.post("/api/auth", async (req, res) => {
	if (
		typeof req.body.login !== "string" ||
		typeof req.body.password !== "string"
	)
		return res.status(503).send("Bad parameters");

	if (!userDB.has(req.body.login)) {
		userDB.set(req.body.login, req.body.password);
	}

	let password = userDB.get(req.body.login);
	if (req.body.password !== password)
		return res
			.status(200)
			.send(
				"<h1>Wrong username/password!</h1> <a href='/auth.html'>Try again</a>"
			);

	req.session.user = req.body.login;

	res.status(200).send(
		"<h1>Registered/Logged in successfully redirecting...!</h1><meta http-equiv='refresh' content='3;url=/' />"
	);
});

app.get("/report", async (req, res) => {
	if (!req.query.url) return res.status(503).send("Bad parameters");
	let url = req.query.url.toString();
	if (url.match(/^https?:\/\//)) {
		admin.check(url, ADMIN_PASSWORD, PASSWORD);
		return res.end("Admin whill check your url soon");
	}
	res.end("Invalid url");
});

app.post("/api/set", async (req, res) => {
	if (!req.session.user || req.session.user == "admin")
		return res.status(403).send("Unauthorized");

	if (!req.body.password || !req.body.content)
		return res.status(503).send("Bad parameters");

	let body = req.body;

	body.password = body.password.toString();
	body.content = body.content.toString().replace(/[<>'"]/g, ""); // NO HACKING!

	let response = await fetch(
		`http://localhost:3001/api/db/set?${new URLSearchParams(body)}`,
		{
			headers: {
				user: req.session.user,
			},
		}
	);
	res.end(await response.text());
});

app.get("/api/get", async (req, res) => {
	let query = req.query;
	if (!query.password) return res.status(503).send("Bad parameters");

	query.password = query.password.toString();

	let response = await fetch(
		`http://localhost:3001/api/db/get?${new URLSearchParams(query)}`,
		{
			headers: {
				user: req.session.user,
			},
		}
	);

	res.end(await response.text());
});

app.get("/", (req, res, next) => {
	if (!req.session.user) {
		return res.redirect("/auth.html");
	}
	next();
});

app.use(express.static("public"));

app.listen(3000);
