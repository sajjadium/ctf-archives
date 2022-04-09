import cluster, { Worker } from "cluster";
import { Server } from "http";

import { IpcHandler } from "./IpcHandler.js";
import { IpcMessage } from "./IpcMessage.js";

const Host = process.env.HOST;

interface WorkerInfo {
	worker: Worker;
	activeGames: number;
}

export class Primary extends IpcHandler<
	IpcMessage.Primary.Request,
	IpcMessage.Primary.Response,
	IpcMessage.Worker.Request,
	IpcMessage.Worker.Response
> {
	private workers: Map<number, WorkerInfo>;
	private games: Map<string, WorkerInfo>;

	public constructor() {
		super();
		this.workers = new Map();
		this.games = new Map();
	}

	public start() {
		super.start();

		const workerCount = 1; // cpus().length - 1;

		for (let i = 0; i < workerCount; i++) {
			const worker = cluster.fork();
			this.workers.set(worker.id, { worker, activeGames: 0 });
		}

		cluster.on("exit", (worker, code, signal) => {
			// eslint-disable-next-line no-console
			console.error(`Worker ${worker.process.pid ?? "(unknown)"} died with code: ${code} and signal: ${signal}`);
			this.workers.delete(worker.id);
			const newWorker = cluster.fork();
			this.workers.set(newWorker.id, { worker: newWorker, activeGames: 0 });
		});

		this.startApiServer();
	}

	protected async handleRequest(
		worker: Worker,
		request: IpcMessage.Primary.Request
	): Promise<IpcMessage.Primary.Response> {
		switch (request.kind) {
			case IpcMessage.Primary.Kind.CloseGame: {
				const gameId = request.id;
				const workerInfo = this.games.get(gameId);

				if (workerInfo !== undefined && workerInfo.worker.id === worker.id) {
					workerInfo.activeGames--;
					this.games.delete(gameId);
				}

				return {
					kind: IpcMessage.Primary.Kind.CloseGame
				};
			}
		}
	}

	protected setIpcListener(fn: (worker: Worker, request: any) => void): void {
		cluster.on("message", fn);
	}

	private generateGameId() {
		let id = "";

		while (id.length === 0 || this.games.has(id)) {
			id = Math.random().toString(36).substring(2, 8).toUpperCase();
		}

		return id;
	}

	private async createGame() {
		// Find the worker with the least active games
		const workerInfo = Array.from(this.workers.values()).reduce((a, b) => a.activeGames < b.activeGames ? a : b);

		// Generate a unique game id
		const gameId = this.generateGameId();

		// Reserve the game id and update the worker info
		this.games.set(gameId, workerInfo);
		workerInfo.activeGames++;

		// Send the message to the worker
		const response = await this.sendRequest(
			workerInfo.worker,
			{
				kind: IpcMessage.Worker.Kind.CreateGame,
				id: gameId
			}
		);

		return { id: gameId, port: response.port };
	}

	private startApiServer() {
		const http = new Server();

		http.on("request", async (req, res) => {
			if (req.method === "POST" && req.url === "/api/create") {
				const { id, port } = await this.createGame();
				res.writeHead(200, { "Content-Type": "application/json" });
				res.write(JSON.stringify({ id, host: Host, port }));
				res.end();
			} else if (req.method === "GET" && req.url!.startsWith("/api/info/")) {
				const gameId = req.url!.substring(10);
				const workerInfo = this.games.get(gameId);

				if (workerInfo !== undefined) {
					const { port } = await this.sendRequest(workerInfo.worker, {
						kind: IpcMessage.Worker.Kind.GetPort
					});

					res.writeHead(200, { "Content-Type": "application/json" });
					res.write(JSON.stringify({ host: Host, port }));
					res.end();
				} else {
					res.writeHead(404, { "Content-Type": "application/json" });
					res.write(JSON.stringify({ error: "Game not found" }));
					res.end();
				}
			} else {
				res.writeHead(404, { "Content-Type": "text/plain" });
				res.write("Not found");
				res.end();
			}
		});

		http.listen(59999, process.env.BIND_ADDRESS ?? "127.0.0.1", () => {
			// eslint-disable-next-line no-console
			console.info("API server started on port 59999");
		});
	}
}
