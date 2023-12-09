const express = require("express");
const rateLimit = require("express-rate-limit");
const report = require("./adminbot.js");

var app = express();

app.set("trust proxy", 2);

app.use(express.static("public"));

app.post(
	"/report",
	rateLimit({
		windowMs: 60 * 1000,
		limit: 2,
		standardHeaders: "draft-7",
		legacyHeaders: false,
	}),
	(req, res) => {
		const { url } = req.query ?? "";

		if (!url.match(/^http\:\/\/localhost:3000\/\?code=/)) {
			res.end("Invalid url!");
			return;
		}
		report(url);
		res.end(`Visiting url ${url}!`);
		return;
	}
);

app.listen(3000);
