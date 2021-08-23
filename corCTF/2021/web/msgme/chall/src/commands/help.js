const commands = require("../commands.js");

const help = "Provides help for the command system.";
const run = (ws, args, data) => {
	let target = args[1];
	
	if(!target) {
		data.msg += "Commands: !" + Object.keys(commands.cmds).join(" !");
		return;
	}

	if(target.startsWith("!")) {
		target = target.slice(1);
	}

	if(target && commands.cmds[target]) {
		data.msg += `!${target}: ${commands.cmds[target].help}`;
	}
	else {
		data.msg += `Command not found.`;
	}

	return;
};

module.exports = { help, run };