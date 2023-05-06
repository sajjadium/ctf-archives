const jwt = require("jsonwebtoken");
const secret = process.env.JWT_SECRET || "jwt secret";

const sign = (username, alert) => {
	return jwt.sign({
		username,
		alert
	}, secret);
};

const signData = (res, username, alert) => {
    res.cookie('session', sign(username, alert), { httpOnly: true });
};

module.exports = {
	secret, signData
};