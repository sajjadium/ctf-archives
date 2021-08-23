const help = "Rolls a number";
const run = (ws, args, data) => {
	let max = 100;
	if(args[1] && !isNaN(args[1])) {
		max = parseInt(args[1]);
	}
	data.msg += `You rolled: ${Math.floor(Math.random() * max + 1)}, ${ws.user}`;
};

module.exports = { help, run };