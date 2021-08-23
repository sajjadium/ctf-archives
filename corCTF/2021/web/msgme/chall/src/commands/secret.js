const help = "...?";

const secret = require("crypto").randomBytes(64).toString("base64");

const run = (ws, args, data) => {
	if(ws.admin && data.to === "admin") {
		data.msg += secret;
        return;
	}
	data.msg += "nope";
};

module.exports = { help, run, secret };