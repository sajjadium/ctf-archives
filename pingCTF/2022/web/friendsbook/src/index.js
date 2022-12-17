import express from "express";
import cookieParser from "cookie-parser";
import jwt from "jsonwebtoken";
import { config } from "dotenv";
import { user } from "./ports/user.js";
import { post } from "./ports/post.js";
import { home } from "./ports/home.js";
import { SECRET } from "./common.js";
import {
	UserRepository,
	init as userInit,
} from "./repository/UserRepository.js";
config();

const PORT = process.env.PORT || 3000;
const app = express();
app.set("view engine", "pug");
app.set("views", "./views");

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

const extractUser = (req, res, next) => {
	req.user = {
		id: null,
		username: null,
	};
	if (req.cookies && req.cookies.token) {
		const token = req.cookies.token;
		if (!token) {
			return next();
		}
		try {
			const user = jwt.verify(token, SECRET);
			req.user = UserRepository.findById(user.id);
			return next();
		} catch (err) {
			return next();
		}
	} else {
		return next();
	}
};

app.use(extractUser);

app.use("/api/post", post);
app.use("/api/user", user);
app.use("/", home);
app.all("*", (req, res) => {
	res.render("error", { error: "Page not found", user: req.user });
});

app.listen(PORT, async () => {
	await userInit();
	console.log(`listening on port http://127.0.0.1:${PORT}`);
});
