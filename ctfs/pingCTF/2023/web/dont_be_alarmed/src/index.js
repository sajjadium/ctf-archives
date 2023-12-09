import express from "express";
import { randomUUID } from "crypto";
// import DOMPurify from "isomorphic-dompurify";
import { readFileSync } from "fs";

import rl from "./ratelimit.js";
import { report, isValidUUID } from "./bot.js";

const app = express();
const port = 3000;

const scores = [];
const allowedChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

const addScore = (score, nickname) => {
	const scoreObj = {
		score,
		nickname,
		id: randomUUID(),
	};
	scores.push(scoreObj);
	try {
		scores.sort((a, b) => b.score - a.score);
		if (scores.length > 10) {
			scores.pop();
		}
	} catch (err) {
		// scores.pop();
	}
	return scoreObj;
};

app.set("trust proxy", 2);
app.use(express.static("static"));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.set("view engine", "ejs");

app.get("/", (req, res) => {
	res.render("index");
});

app.get("/result/:uuid", (req, res) => {
	const { uuid } = req.params;
	if (isValidUUID(uuid)) {
		const score = scores.find((s) => s.id === uuid);
		if (!score) {
			return res.status(404).send("Score not found");
		}
		res.render("result", { score });
	} else {
		res.status(400).send("Invalid UUID");
	}
});

app.get("/highscores", (req, res) => {
	res.render("highscores", { scores });
});

app.post("/highscores", (req, res) => {
	const { score, nickname } = req.body;
	if (
		typeof score !== "string" ||
		typeof nickname !== "string" ||
		nickname.length !== 4 ||
		nickname.split("").some((char) => !allowedChars.includes(char))
	) {
		return res.json({
			success: false,
			message:
				"Nickname must be 4 characters long and contain only letters",
		});
	}
	const s = addScore(score, nickname);
	return res.json({
		success: true,
		score: s,
	});
});

app.post("/report/:uuid", rl, async (req, res) => {
	try {
		const { uuid } = req.params;
		console.log(`Visiting http://localhost:3000/${uuid}`);
		await report(uuid);
		res.redirect("/");
	} catch (err) {
		console.log(err);
	}
});

app.listen(port, () => {
	console.log(`Server is running on http://localhost:${port}`);
});
