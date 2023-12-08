import { randomUUID } from "crypto";
import { db } from "./db.js";
import users from "./users.js";

const saveOne = async (coupon) => {
	return new Promise((resolve, reject) => {
		db.run(
			`UPDATE coupons SET valid = ? WHERE id = ?`,
			[coupon.valid, coupon.id],
			(err) => {
				if (err) {
					return reject(new Error("Something went wrong"));
				}
				return resolve(coupon);
			}
		);
	});
};

const findByUserId = async (userId) => {
	return new Promise((resolve, reject) => {
		db.all(
			`SELECT * FROM coupons WHERE userId = ?`,
			[userId],
			(err, rows) => {
				if (err) {
					return reject(new Error("Something went wrong"));
				}
				return resolve(rows);
			}
		);
	});
};

const findByUserIdAndCode = async (userId, couponCode) => {
	return new Promise((resolve, reject) => {
		db.get(
			`SELECT * FROM coupons WHERE userId = ? AND code = ?`,
			[userId, couponCode],
			(err, row) => {
				if (err) {
					return reject(new Error("Something went wrong"));
				}
				return resolve(row);
			}
		);
	});
};

const createNewUser = async (userId) => {
	return new Promise((resolve, reject) => {
		const id = randomUUID();
		const code = Math.random().toString(36).substring(2, 8).toUpperCase();
		const value = 10.0;
		const valid = true;
		db.run(
			`INSERT INTO coupons (id, userId, code, value, valid) VALUES (?, ?, ?, ?, ?);`,
			[id, userId, code, value, valid],
			(err) => {
				if (err) {
					return reject(new Error("Something went wrong"));
				}
				return resolve({
					id,
					userId,
					code,
					value,
					valid,
				});
			}
		);
	});
};

const redeemOneByUserIdAndCode = async (userId, couponCode) => {
	return new Promise(async (resolve, reject) => {
		const coupon = await findByUserIdAndCode(userId, couponCode);
		if (!coupon) {
			return reject(new Error("Coupon not found"));
		}
		if (!coupon.valid) {
			return reject(new Error("Coupon already used"));
		}
		coupon.valid = false;
		await saveOne(coupon);
		await users.addBalance(userId, coupon.value);
		return resolve(coupon);
	});
};

export default {
	saveOne,
	findByUserId,
	findByUserIdAndCode,
	createNewUser,
	redeemOneByUserIdAndCode,
};
