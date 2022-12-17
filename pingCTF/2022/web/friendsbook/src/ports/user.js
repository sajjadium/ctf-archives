import express from "express";
import jwt from "jsonwebtoken";
import { UserRepository } from "../repository/UserRepository.js";
import { SECRET } from "../common.js";

const router = express.Router();

export const verifyToken = (req, res, next) => {
	try {
		const token = req.cookies.token;
		if (!token) {
			throw new Error("Please login first");
		}
		const verified = jwt.verify(token, SECRET);
		req.user = UserRepository.findById(verified.id);
		return next();
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
};

router.post("/register", async (req, res) => {
	try {
		const { username, password, password2 } = req.body;
		if (!username || !password || !password2) {
			throw new Error("Invalid data");
		}
		if (password !== password2) {
			throw new Error("Passwords do not match");
		}
		const user = await UserRepository.create({ username, password });
		res.cookie("token", user.token, { httpOnly: true });
		res.redirect("/");
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
});

router.post("/login", async (req, res) => {
	try {
		const { username, password } = req.body;
		const user = await UserRepository.login({ username, password });
		res.cookie("token", user.token, { httpOnly: true });
		res.redirect("/");
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
});

router.get("/friends", verifyToken, async (req, res) => {
	try {
		const friends = UserRepository.getFriends(req.user.id);
		const friendNames = friends.map((friend) => friend.username);
		res.json(friendNames);
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
});

router.post("/friends", verifyToken, async (req, res) => {
	try {
		const { username } = req.body;
		const friend = UserRepository.findByUsername(username);
		if (!friend) {
			throw new Error("User not found");
		}
		UserRepository.addFriend(req.user, friend.id);
		res.status(200).end();
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
});

export { router as user };
