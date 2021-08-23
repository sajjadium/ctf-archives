const help = "...!";

const secret = require("../commands.js").cmds.secret.secret;

const run = (ws, args, data) => {
	if(args[1] === secret) {
		data.msg += process.env.FLAG;
	}
	else {
		data.msg += "Incorrect secret!";
	}
};

module.exports = { help, run };