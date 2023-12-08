import { db } from "./db.js";

const findAll = async () => {
	return new Promise((resolve, reject) => {
		db.serialize(() => {
			db.all(`SELECT * FROM products`, (err, rows) => {
				if (err) {
					return reject(new Error("Something went wrong"));
				}
				resolve(rows);
			});
		});
	});
};

const findById = async (id) => {
	return new Promise((resolve, reject) => {
		db.get(`SELECT * FROM products WHERE id = ?`, [id], (err, row) => {
			if (err) {
				return reject(new Error("Something went wrong"));
			}
			resolve(row);
		});
	});
};

const findByUserId = async (userId) => {
	return new Promise((resolve, reject) => {
		db.all(
			`SELECT productId FROM users_products WHERE userId = ?`,
			[userId],
			async (err, rows) => {
				if (err) {
					return reject(new Error("Something went wrong"));
				}
				const products = await findAll();
				const filteredProducts = products.filter((product) =>
					rows.some((row) => row.productId === product.id)
				);
				return resolve(filteredProducts);
			}
		);
	});
};

const buy = (user, product) => {
	return new Promise((resolve, reject) => {
		const newBalance = user.balance - product.price;
		if (newBalance < 0) {
			return reject(new Error("Not enough money"));
		}

		db.run(
			`UPDATE users SET balance = ? WHERE id = ?`,
			[Math.round(newBalance * 100) / 100, user.id],
			(err) => {
				if (err) {
					return reject(new Error("Something went wrong"));
				}
				db.run(
					`INSERT INTO users_products (userId, productId) VALUES (?, ?);`,
					[user.id, product.id],
					(err) => {
						if (err) {
							return reject(new Error("Something went wrong"));
						}
						return resolve();
					}
				);
			}
		);
	});
};

export default {
	findAll,
	findById,
	findByUserId,
	buy,
};
