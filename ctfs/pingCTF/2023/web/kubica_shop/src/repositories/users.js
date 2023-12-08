import { randomUUID } from "crypto";
import { db } from "./db.js";
import { resolve } from "path";

const findByUsername = async (username) => {
	return new Promise((resolve, reject) => {
		db.get(
			`SELECT * FROM users WHERE username = ?`,
			[username],
			(err, row) => {
				if (err) {
					return reject(new Error("Something went wrong"));
				}
				resolve(row);
			}
		);
	});
};

const findById = async (id) => {
	return new Promise((resolve, reject) => {
		db.get(`SELECT * FROM users WHERE id = ?`, [id], (err, row) => {
			if (err) {
				return reject(new Error("Something went wrong"));
			}
			resolve(row);
		});
	});
};

const createOne = async (username, password) => {
	return new Promise((resolve, reject) => {
		const id = randomUUID();
		const balance = 0;
		db.run(
			`INSERT INTO users (id, username, password, balance) VALUES (?, ?, ?, ?);`,
			[id, username, password, balance],
			(err) => {
				if (err) {
					return reject(new Error("Something went wrong"));
				}
				resolve({
					id,
					username,
					password,
					balance,
				});
			}
		);
	});
};

const addBalance = async (userId, value) => {
	return new Promise((resolve, reject) => {
		db.run(
			`UPDATE users SET balance = balance + ? WHERE id = ?`,
			[value, userId],
			(err) => {
				if (err) {
					return reject(new Error("Something went wrong"));
				}
				return resolve();
			}
		);
	});
};

export default {
	findByUsername,
	findById,
	createOne,
	addBalance,
};
