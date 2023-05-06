import { v4 } from "uuid";

export class Post {
	id;
	isPrivate = false;
	content;
	createdAt;
	author;
	authorId;

	constructor({ id, isPrivate, content, createdAt, author, authorId }) {
		this.id = id;
		this.isPrivate = isPrivate;
		this.content = content;
		this.createdAt = createdAt;
		this.author = author;
		this.authorId = authorId;
	}

	static create({ isPrivate, content, author, authorId }) {
		const newPost = new Post({
			id: v4(),
			isPrivate,
			content,
			createdAt: new Date(),
			author,
			authorId,
		});

		return newPost;
	}

	switchVisibility() {
		this.isPrivate = !this.isPrivate;
	}

	updateContent(content) {
		this.content = content;
	}
}
