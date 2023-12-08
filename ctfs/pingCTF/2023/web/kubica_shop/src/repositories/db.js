import sqlite3 from "sqlite3";
import products from "./seed/products.js";

export const db = new sqlite3.Database(":memory:");

export const init = () => {
	db.serialize(() => {
		db.run(`CREATE TABLE products (
			id TEXT PRIMARY KEY,
			name TEXT NOT NULL,
			description TEXT NOT NULL,
			price REAL NOT NULL,
			imageUrl TEXT NOT NULL
		);`);
		db.run(`CREATE TABLE users (
			id TEXT PRIMARY KEY,
			username TEXT NOT NULL,
			password TEXT NOT NULL,
			balance REAL NOT NULL
		);`);
		db.run(`CREATE TABLE coupons (
			id TEXT PRIMARY KEY,
			userId TEXT NOT NULL,
			code TEXT NOT NULL,
			value REAL NOT NULL,
			valid INTEGER NOT NULL
		);`);
		db.run(`CREATE TABLE users_products (
			userId TEXT NOT NULL,
			productId TEXT NOT NULL,
			PRIMARY KEY (userId, productId)
		);`);
		const statement = db.prepare(
			`INSERT INTO products (id, name, description, price, imageUrl) VALUES (?, ?, ?, ?, ?);`
		);
		products.forEach((product) => {
			statement.run(
				product.id,
				product.name,
				product.description,
				product.price,
				product.imageUrl
			);
		});
		statement.finalize();
	});
};
