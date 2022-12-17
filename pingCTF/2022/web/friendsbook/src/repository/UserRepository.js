import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import { User } from "../domain/User.js";
import { Post } from "../domain/Post.js";
import { SECRET } from "../common.js";
import crypto from "crypto";
import { FLAG } from "../flag.js";

const MAX_POSTS_NUMBER = 5;

let users = [];
let posts = [];

let adminId;

export const init = async () => {
	const user = User.create({
		username: "Mark",
		password: await bcrypt.hash(
			crypto.randomBytes(128).toString("hex"),
			10
		),
	});

	adminId = user.id;

	const secretPost = Post.create({
		isPrivate: true,
		content: `My dirty secrets... ${FLAG}... I hope noone violates my privacy!`,
		author: user.username,
		authorId: user.id,
	});

	const publicPost = Post.create({
		isPrivate: false,
		content: `Hii friendsss! I'm new here! I hope you'll be my friend! I'm so lonely... 👀`,
		author: user.username,
		authorId: user.id,
	});

	posts = [...posts, secretPost, publicPost];
	users = [...users, user];
};

const getStrDate = (d) => {
	return `${d.getDate()}/${d.getMonth()}/${d.getFullYear()} ${d
		.getHours()
		.toString()
		.padStart(2, "0")}:${d.getMinutes().toString().padStart(2, "0")}`;
};

export const UserRepository = {
	async create(user) {
		const { username, password } = user;
		if (users.find((u) => u.username === username)) {
			throw new Error("Username already taken");
		}
		const hashedPassword = await bcrypt.hash(password, 10);
		const newUser = User.create({
			username,
			password: hashedPassword,
		});
		const token = jwt.sign({ id: newUser.id, username }, SECRET, {
			expiresIn: 86400,
		});
		users.push(newUser);

		newUser.addFriend(adminId);
		this.save(newUser);

		return { token };
	},

	async login({ username, password }) {
		const user = users.find((u) => u.username === username);
		if (!user) {
			throw new Error("User not found");
		}
		const validPassword = await bcrypt.compare(password, user.password);
		if (!validPassword) {
			throw new Error("Invalid password");
		}
		const token = jwt.sign({ id: user.id, username }, SECRET, {
			expiresIn: 86400,
		});
		return { token };
	},

	findById(id) {
		return users.find((u) => u.id === id);
	},

	save(user) {
		const index = users.findIndex((u) => u.id === user.id);
		users[index] = user;
	},

	getFriends(userId) {
		const user = users.find((u) => u.id === userId);
		return users.filter((u) => user.friends.includes(u.id));
	},

	getWall(userId, query) {
		const user = users.find((u) => u.id === userId);
		return posts
			.sort((a, b) => b.createdAt - a.createdAt)
			.map((p) => {
				if (
					(user.friends.includes(p.authorId) &&
						p.content.includes(query)) ||
					(p.authorId === userId && p.content.includes(query))
				) {
					return p.id;
				}
			})
			.filter((p) => p !== undefined);
	},

	getWallCount(userId, query) {
		const user = users.find((u) => u.id === userId);
		return posts.filter(
			(p) =>
				(user.friends.includes(p.authorId) &&
					p.content.includes(query)) ||
				(p.authorId === userId && p.content.includes(query))
		).length;
	},

	getPost(requester, postId) {
		const post = posts.find((p) => p.id === postId);

		// ! Privacy is VERY IMPORTANT to us, so we have a LOT of checks here. !
		if (!post) {
			throw new Error("Post not found");
		}
		if (requester.id === post.authorId) {
			return {
				...post,
				createdAt: getStrDate(post.createdAt),
			};
		}
		if (post.isPrivate && post.authorId !== requester.id) {
			throw new Error("Post not found");
		}
		if (requester.friends.includes(post.authorId) && post.isPrivate) {
			throw new Error("Post not found");
		}
		if (requester.friends.includes(post.authorId)) {
			return {
				...post,
				createdAt: getStrDate(post.createdAt),
			};
		}
		throw new Error("Post not found");
	},

	createPost(requester, content, isPublic) {
		let postsNumber = 0;
		posts.forEach((p) => {
			if (p.authorId === requester.id) postsNumber++;
		});

		if (postsNumber > MAX_POSTS_NUMBER) {
			throw new Error(
				`You have exceeded the maximum posts number: ${MAX_POSTS_NUMBER}!`
			);
		}

		const post = Post.create({
			content,
			isPrivate: !isPublic,
			author: requester.username,
			authorId: requester.id,
		});
		posts.push(post);
	},

	addFriend(requester, friendId) {
		const friend = users.find((u) => u.id === friendId);
		if (!friend) {
			throw new Error("Friend not found");
		}
		if (requester.id === friendId) {
			throw new Error("You can't add yourself as a friend");
		}
		if (requester.friends.includes(friendId)) {
			throw new Error("Friend already added");
		}
		requester.addFriend(friendId);
		this.save(requester);
	},

	findByUsername(username) {
		return users.find((u) => u.username === username);
	},
};
