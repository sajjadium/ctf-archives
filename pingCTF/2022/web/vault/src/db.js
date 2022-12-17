const express = require("express");
const crypto = require("crypto");
const PASSWORD = crypto.randomBytes(16).toString("hex");
require("dotenv").config();
const DB = new Map();

DB.set("admin", {
	password: PASSWORD,
	content: process.env.FLAG,
});

const app = new express();

app.get("/api/db/set", (req, res) => {
	if (
		typeof req.query.content != "string" ||
		typeof req.query.password != "string" ||
		typeof req.headers.user != "string"
	)
		return res.status(200).send("Bad parameters");

	DB.set(req.headers.user, req.query);
	res.end("success");
});

app.get("/api/db/get", (req, res) => {
	if (
		typeof req.query.password != "string" ||
		typeof req.headers.user != "string"
	)
		return res.end("Bad parameters");

	if (!DB.has(req.headers.user)) return res.end("No secret set");

	let record = DB.get(req.headers.user);

	if (req.query.password !== record.password)
		return res.end("Wrong Password");

	res.end(record.content);
});

app.listen(3001);

module.exports = { PASSWORD };
