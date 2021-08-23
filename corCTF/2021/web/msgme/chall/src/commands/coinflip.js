const help = "Flips a coin";
const run = (ws, args, data) => {
	data.msg += (Math.random() > 0.5 ? "Heads" : "Tails");
};

module.exports = { help, run };