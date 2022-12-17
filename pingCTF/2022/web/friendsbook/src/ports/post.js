import { verifyToken } from "./user.js";
import { UserRepository } from "../repository/UserRepository.js";
import express from "express";

const router = express.Router();

router.get("/wall", verifyToken, async (req, res) => {
	try {
		const { q } = req.query;
		const posts = UserRepository.getWall(req.user.id, q);
		const count = UserRepository.getWallCount(req.user.id, q);
		res.json({ data: posts, count });
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
});

router.get("/:id", verifyToken, async (req, res) => {
	try {
		const { id } = req.params;
		const post = UserRepository.getPost(req.user, id);
		res.render("post.pug", {
			user: req.user,
			post,
		});
	} catch (err) {
		res.status(404).render("post.pug", {
			user: req.user,
			post: null,
		});
	}
});

router.post("/", verifyToken, async (req, res) => {
	try {
		const { content, isPublic } = req.body;
		UserRepository.createPost(req.user, content, isPublic === "on");
		res.redirect("/wall");
	} catch (err) {
		res.redirect(`/error?message=${err.message}`);
	}
});

export { router as post };
