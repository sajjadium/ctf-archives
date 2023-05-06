import { v4 } from "uuid";

export class User {
	id;
	username;
	password;
	createdAt;
	friends;

	constructor({ id, username, password, createdAt, friends }) {
		this.id = id;
		this.username = username;
		this.password = password;
		this.createdAt = createdAt;
		this.friends = friends;
	}

	static create({ username, password }) {
		const newUser = new User({
			id: v4(),
			username,
			password,
			createdAt: new Date(),
			friends: [],
		});

		return newUser;
	}

	addFriend(friendId) {
		this.friends.push(friendId);
	}
}
