import { sessions } from "./index.js";

const DELETE_INTERVAL_MS = 30 * 60 * 1000;

export const startOptimizing = async () => {
	console.log(`Restarting the server:`);
	setInterval(() => {
		console.log(`Restarting the server with ${sessions.length} users.`);
		process.exit(0);
	}, DELETE_INTERVAL_MS);
};
