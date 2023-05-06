const help = "Asks the mythical magic 8-ball a question";
const run = (ws, args, data) => {
	let question = args.slice(1).join(" ");
	if(!question.endsWith("?")) {
		question += "?";
	}
	data.msg += question + " ";

	let responses = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes – definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Signs point to yes', 'Reply hazy', 'try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Dont count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful'];
	data.msg += responses[Math.floor(Math.random() * responses.length)];
};

module.exports = { help, run };