const io = require("socket.io-client");
const { createHash } = require("crypto");
const { spawn } = require("child_process");

const SERVER_IP = process.env.SERVER_IP ?? "cairo.carmen.pwni.ng";

const [_node, _scriptName, url, ...command] = process.argv;

if (!url || command.length === 0) {
	process.stderr.write(`
Usage: node runner.js <url> <command to run>

Your command will be provided with the following environment variables:
  TARGET_IP: the IP address of the target instance
  SENSOR_PORT: the port of the sensor interface
  SENSOR_TOKEN: the token to authenticate with the sensor interface

Your command will be launched about 10 seconds before the instance is up, and will be automatically killed after the
instance is brought down.
	`.trim() + "\n");

	process.exit(1);
}

const yellow = (str) => `\x1b[33m${str}\x1b[0m`;
const blue = (str) => `\x1b[34m${str}\x1b[0m`;
const magenta = (str) => `\x1b[35m${str}\x1b[0m`;
const cyan = (str) => `\x1b[36m${str}\x1b[0m`;
const log = (message) => console.log(blue("[runner]") + " " + message);

const socket = io(`http://${SERVER_IP}`);

socket.once("connect", () => {
	log("Connected to server, obtaining proof of work");

	socket.emit("submitJob", { url });

	socket.once("challenge", (challenge) => {
		log(`Solving proof of work (prefix ${cyan(challenge.prefix)}, difficulty ${magenta(challenge.difficulty)})`);
		let i = 0;

		while (true) {
			let resultBuffer = createHash("sha256").update(challenge.prefix).update(i.toString()).digest();
			let value = resultBuffer.readUInt32BE(0);
			value >>>= (32 - challenge.difficulty);

			if (value === 0) {
				break;
			}

			i++;
		}

		log(`Submitting proof of work (response ${yellow(i.toString())})`);
		socket.emit("submitChallenge", i.toString());

		socket.on("position", (position) => {
			log(`Waiting in queue, ${position} jobs are queued in front of yours`);
		});

		socket.once("accepted", ({ response, launchingAt }) => {
			log("Running your command");
			log(`TARGET_IP    = ${cyan(response.targetIp)}`);
			log(`SENSOR_PORT  = ${magenta(response.sensorPort)}`);
			log(`SENSOR_TOKEN = ${yellow(response.sensorToken)}`);

			let proc = spawn(
				command[0],
				command.slice(1),
				{
					stdio: ["ignore", process.stdout, process.stderr],
					detached: true,
					env: {
						...process.env,
						TARGET_IP: response.targetIp,
						SENSOR_PORT: response.sensorPort,
						SENSOR_TOKEN: response.sensorToken
					}
				}
			);

			socket.once("processing", () => log("Instance has launched"));

			socket.once("done", () => {
				log("Instance has been killed, sending SIGINT to your process and closing the socket");
				socket.disconnect();
				process.kill(-proc.pid, "SIGINT");
			});
		});
	});
});
