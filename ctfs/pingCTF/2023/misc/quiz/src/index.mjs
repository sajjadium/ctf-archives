import { generate } from "random-words";
import readline from "node:readline/promises";

const rl = readline.createInterface({
	input: process.stdin,
	output: process.stdout,
});

var FLAG = process.env.FLAG ?? "ping{FAKE}";
var questions = [];

for (var i = 0; i < 100; i++) {
	questions.push(generate(50).join(" ") + "?");
}

async function start() {
	for (var i = 0; i < 25; i++) {
		console.log(`question nr: ${i + 1}`);
		console.log(questions[Math.floor(Math.random() * questions.length)]);
		var answer = await rl.question(
			"answers: \n1) ?????????????????\n2) ?????????????????\n3) ?????????????????\n4) ?????????????????\n5) ?????????????????\nchoose your answer: "
		);
		if (answer != Math.floor(Math.random() * 5) + 1) {
			console.log("WRONG ANSWER");
			process.exit(0);
		}
	}
	console.log("CONGRATULATIONS here is your reward:", FLAG);
	process.exit(0);
}

start();
