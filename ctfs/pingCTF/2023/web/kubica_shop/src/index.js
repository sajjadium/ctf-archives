import express from "express";
import cookieParser from "cookie-parser";

import rl from "./ratelimit.js";
import products from "./repositories/products.js";
import users from "./repositories/users.js";
import coupons from "./repositories/coupons.js";
import { init } from "./repositories/db.js";

init();

const app = express();
const port = 3000;

const findUser = async (req) => {
	const user = await users.findById(req.cookies.token);
	if (user) {
		user["password"] = undefined;
		user["coupons"] = await coupons.findByUserId(user.id);
		user["products"] = await products.findByUserId(user.id);
		return {
			user,
		};
	} else {
		return {
			user: null,
		};
	}
};

app.set("view engine", "ejs");
app.use(express.static("static"));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());

app.get("/", async (req, res) => {
	try {
		const productsData = await products.findAll();
		const userData = await findUser(req);
		res.render("index", {
			...userData,
			products: productsData,
		});
	} catch (err) {
		res.render("error", {
			error: err?.message ?? "Something went wrong",
		});
	}
});

app.get("/auth", async (req, res) => {
	try {
		const userData = await findUser(req);
		res.render("auth", userData);
	} catch (err) {
		res.render("error", {
			error: err?.message ?? "Something went wrong",
		});
	}
});

app.get("/me", async (req, res) => {
	try {
		const userData = await findUser(req);
		if (!userData.user) {
			return res.redirect("/");
		}
		res.render("me", userData);
	} catch (err) {
		res.render("error", {
			error: err?.message ?? "Something went wrong",
		});
	}
});

app.get("/*", (req, res) => {
	res.redirect("/");
});

app.post("/api/auth", rl, async (req, res) => {
	try {
		const { username, password } = req.body;
		if (
			typeof username !== "string" ||
			typeof password !== "string" ||
			username.length > 32 ||
			password.length > 32 ||
			username.length < 2 ||
			password.length < 2
		) {
			return res.json({
				error: "Username or password is too long or too short",
			});
		}
		// let session = sessions.find((session) => session.username === username);
		let token;
		const user = await users.findByUsername(username);
		if (!user) {
			const newUser = await users.createOne(username, password);
			await coupons.createNewUser(newUser.id);
			token = newUser.id;
		} else if (user.password !== password) {
			return res.json({
				error: "Invalid username or password",
			});
		} else {
			token = user.id;
		}
		res.cookie("token", token);
		return res.json({
			success: true,
		});
	} catch (err) {
		return res.json({
			error: "Something went wrong",
		});
	}
});

app.post("/api/redeem", async (req, res) => {
	try {
		const userData = await findUser(req);
		if (!userData.user) {
			return res.json({
				error: "You are not logged in",
			});
		}
		const { couponCode } = req.body;
		if (typeof couponCode !== "string" || couponCode.length !== 6) {
			return res.json({
				error: "Invalid coupon code",
			});
		}
		const userId = userData.user.id;
		await coupons.redeemOneByUserIdAndCode(userId, couponCode);
		return res.json({
			success: true,
		});
	} catch (err) {
		return res.json({
			error: err?.message ?? "Something went wrong",
		});
	}
});

app.post("/api/buy", async (req, res) => {
	try {
		const user = await users.findById(req.cookies.token);
		if (!user) {
			return res.json({
				error: "You are not logged in",
			});
		}
		const { productId } = req.body;
		const correctProductId =
			typeof productId === "string" &&
			/^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$/.test(productId);

		if (!correctProductId) {
			return res.json({
				error: "Invalid product ID",
			});
		}

		const product = await products.findById(productId);
		if (!product) {
			return res.json({
				error: "Invalid product",
			});
		}
		await products.buy(user, product);
		return res.json({
			success: true,
		});
	} catch (err) {
		return res.json({
			error: err?.message ?? "Something went wrong",
		});
	}
});

app.listen(port, () => {
	console.log(`Server is running on http://localhost:${port}`);
});
