import { Socket } from "net";

import { RecalibrateEngineAction, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

export class RecalibrateEngineSystem extends System<SystemKind.RecalibrateEngine> {
	private device: string;
	private player: Player;
	private complete: boolean;
	private socket: Socket;
	private buffer: Buffer;

	public constructor(id: number, device: string, player: Player) {
		super(SystemKind.RecalibrateEngine, id);
		this.device = device;
		this.player = player;
		this.complete = false;
		this.socket = new Socket();
		this.buffer = Buffer.alloc(0);
	}

	public accept(game: Game, player: Player, device?: string): boolean {
		return device === this.device && player === this.player;
	}

	public attach(_game: Game, _player: Player) {
		this.socket = new Socket();
		this.socket.connect({
			host: process.env.RECALIBRATE_ENGINE_HOST ?? "localhost",
			port: parseInt(process.env.RECALIBRATE_ENGINE_PORT ?? "25581", 10)
		});
		this.socket.on("error", (error) => console.error(error));
		this.socket.on("data", this.onData.bind(this));
		this.buffer = Buffer.alloc(0);
	}

	public getStateForPlayer(player: Player): SystemState | undefined {
		if (player !== this.player) {
			return undefined;
		}

		return this.getStateForValidPlayer();
	}

	public tick(game: Game, player: Player, actionJson?: unknown) {
		if (actionJson === undefined) {
			return;
		}

		const action = RecalibrateEngineAction.fromUnknown(actionJson);

		if (action.button === 0) {
			player.setSystem(game, game.level.movementSystem);
			return;
		}

		this.socket.write(String.fromCharCode(action.button + 0x30));
	}

	public afterTick(_game: Game): void {
		// nothing to do
	}

	public detach(_game: Game, _player: Player) {
		this.socket.destroy();
	}

	public blockVictory(): boolean {
		return !this.complete;
	}

	private onData(data: Buffer) {
		this.buffer = Buffer.concat([this.buffer, data]);

		while (true) {
			const messageEnd = this.buffer.indexOf("\n");

			if (messageEnd === -1) {
				return;
			}

			const messageType = String.fromCharCode(this.buffer[0]);
			const message = this.buffer.toString("utf8", 1, messageEnd);
			this.buffer = this.buffer.slice(messageEnd + 1);

			switch (messageType) {
				case ">": {
					this.player.pushUpdate(
						new GameUpdate.RecalibrateEngineUpdate({
							event: "flash",
							body: message
						})
					);
					break;
				}

				case ":": {
					this.player.pushUpdate(
						new GameUpdate.RecalibrateEngineUpdate({
							event: "display",
							body: message
						})
					);
					break;
				}

				case "!": {
					this.complete = true;
					this.updatePlayers();
					break;
				}
			}
		}
	}

	private getStateForValidPlayer() {
		return {
			kind: this.kind,
			id: this.id,
			devices: !this.complete ? [this.device] : [],
			complete: this.complete
		};
	}

	private updatePlayers() {
		this.player.pushUpdate(
			new GameUpdate.SystemStateUpdate({
				state: this.getStateForValidPlayer()
			})
		);
	}
}
