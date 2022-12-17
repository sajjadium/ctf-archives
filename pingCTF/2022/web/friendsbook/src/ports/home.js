import express from "express";
import { verifyToken } from "./user.js";

const router = express.Router();

router.get("/", async (req, res) => {
	res.render("home", {
		user: req.user,
	});
});

router.get("/login", async (req, res) => {
	try {
		if (req.user.id) {
			return res.redirect("/");
		} else {
			res.render("login", {
				user: req.user,
			});
		}
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
});

router.get("/register", async (req, res) => {
	try {
		res.render("register", {
			user: req.user,
		});
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
});

router.get("/logout", async (req, res) => {
	try {
		res.clearCookie("token");
		res.redirect("/");
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
});

router.get("/error", async (req, res) => {
	try {
		res.render("error", {
			user: req.user,
			error: req.query.message,
		});
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
});

router.get("/wall", verifyToken, async (req, res) => {
	try {
		res.render("wall.pug", {
			user: req.user,
		});
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
});

router.get("/wall/new", verifyToken, async (req, res) => {
	try {
		res.render("new-post.pug", {
			user: req.user,
		});
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
});

export { router as home };
