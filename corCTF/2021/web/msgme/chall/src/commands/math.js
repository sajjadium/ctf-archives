const help = "2+2=4-1=3 quick maffs";
const run = (ws, args, data) => {
	data.msg += args.slice(1).join(" ");
	data.type = "sandbox";
};

module.exports = { help, run };