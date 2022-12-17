const express = require("express");
const crypto = require("crypto");
const ADMIN_PASSWORD = crypto.randomBytes(16).toString("hex");
let app = new express();
let admin = require("./admin.js");
app.use(express.json({ limit: "1kb" }));
app.use(express.static("public"));

let noteDB = new Map();

noteDB.set("FLAG", {
	title: "FLAG",
	content: "ping{FAKE_FLAG}",
	owner: "admin",
});

let userDB = new Map();

userDB.set("admin", ADMIN_PASSWORD);

app.post("/api/create", (req, res) => {
	let auth = atob(req.headers.notcookie);
	let login = auth.split(":")[0];
	let password = auth.split(":")[1];

	console.log(login, password);
	if (!userDB.get(login)) {
		userDB.set(login, password);
	}

	if (userDB.get(login) !== password) {
		res.end("Unauthorized");
		return;
	}
	console.log(req.body);
	if (
		typeof req.body.title !== "string" ||
		typeof req.body.content !== "string"
	) {
		res.end("Invalid note");
		return;
	}

	let id = crypto.randomBytes(8).toString("hex");

	noteDB.set(id, {
		title: req.body.title,
		content: req.body.content,
		owner: login,
	});

	res.json({ id });
});

app.get("/api/notes/:id", (req, res) => {
	if (!noteDB.get(req.params.id)) {
		res.json("Not Found");
		return;
	}

	let auth = atob(req.headers.notcookie);
	let login = auth.split(":")[0];
	let password = auth.split(":")[1];
	if (!userDB.get(login) || userDB.get(login) !== password) {
		res.end("Unauthorized");
		return;
	}

	let note = noteDB.get(req.params.id);
	if (login !== "admin" && note.owner !== login) {
		res.end("Unauthorized");
		return;
	}

	res.json(note);
});

app.get("/api/report/:id", (req, res) => {
	if (!req.params.id.match(/^[a-f0-9]{16}$/) || !noteDB.get(req.params.id)) {
		res.end("Bad note Id");
	}
	admin.check(req.params.id, ADMIN_PASSWORD);
	res.end("Admin will visit your note soon");
});

app.listen(3000);
