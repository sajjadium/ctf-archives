import cluster, { Worker as ClusterWorker } from "cluster";
import { createServer as createHttpServer, Server as HttpServer } from "http";
import { Server as SocketServer } from "socket.io";

import { Game } from "@amongst/game-server";

import { IpcHandler } from "./IpcHandler.js";
import { IpcMessage } from "./IpcMessage.js";

export class Worker extends IpcHandler<
	IpcMessage.Worker.Request,
	IpcMessage.Worker.Response,
	IpcMessage.Primary.Request,
	IpcMessage.Primary.Response
> {
	private id: number;
	private httpServer: HttpServer;
	private socketServer: SocketServer;
	private worker: ClusterWorker;
	private games: Map<string, Game>;

	public constructor(id: number) {
		super();
		this.id = id;
		this.httpServer = createHttpServer();
		this.socketServer = new SocketServer(this.httpServer);
		this.worker = cluster.worker!;
		this.games = new Map();
	}

	public start() {
		super.start();

		// eslint-disable-next-line no-console
		console.log(`Worker ${this.id}: started`);

		this.socketServer.on("connection", (socket) => {
			socket.on("ping", (ack: () => void) => ack());

			socket.once("join", () => {
				const gameId = socket.handshake.query.game;

				if (typeof gameId !== "string") {
					socket.disconnect();
					return;
				}

				const game = this.games.get(gameId);

				if (game === undefined) {
					// eslint-disable-next-line no-console
					console.log(`Worker ${this.id}: received connection for unknown game ${gameId}`);
					socket.disconnect();
					return;
				}

				if (game.players.size >= 10) {
					// eslint-disable-next-line no-console
					console.log(`Worker ${this.id}: game ${gameId} is full`);
					socket.disconnect();
					return;
				}

				let name = socket.handshake.query.name;

				if (typeof name !== "string") {
					name = "Player";
				}

				name = name.replace(/[^\x20-\x7e]/g, "").substring(0, 20);

				if (name.length === 0) {
					name = "Player";
				}

				const playerId = game.addPlayer(socket, name);
				// eslint-disable-next-line no-console
				console.log(`Worker ${this.id}: received connection for game ${gameId} (player ${playerId})`);

				socket.on("disconnect", () => {
					// eslint-disable-next-line no-console
					console.log(`Disconnect ${socket.id} from worker ${this.id}`);
					game.removePlayer(playerId);

					if (game.isEmpty()) {
						// eslint-disable-next-line no-console
						console.log(`Worker ${this.id}: removing game ${gameId}`);
						game.stop();
						this.games.delete(gameId);
						this.sendRequest(this.worker, { kind: IpcMessage.Primary.Kind.CloseGame, id: gameId });
					}
				});
			});
		});

		this.httpServer.listen(this.getPort(), process.env.BIND_ADDRESS ?? "127.0.0.1");
	}

	protected async handleRequest(
		worker: ClusterWorker,
		request: IpcMessage.Worker.Request
	): Promise<IpcMessage.Worker.Response> {
		switch (request.kind) {
			case IpcMessage.Worker.Kind.CreateGame: {
				const game = new Game();
				this.games.set(request.id, game);
				game.start();
				// eslint-disable-next-line no-console
				console.log(`Worker ${this.id}: created game ${request.id}`);

				return {
					kind: IpcMessage.Worker.Kind.CreateGame,
					id: request.id,
					port: this.getPort()
				};
			}

			case IpcMessage.Worker.Kind.GetPort: {
				return {
					kind: IpcMessage.Worker.Kind.GetPort,
					port: this.getPort()
				};
			}
		}
	}

	protected setIpcListener(fn: (worker: ClusterWorker, request: any) => void) {
		this.worker.on("message", (message) => {
			fn(this.worker, message);
		});
	}

	private getPort() {
		return 60000 + this.id;
	}
}
