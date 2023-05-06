import { Socket } from "net";
import { Map } from "immutable";

import { PurchaseSnackAction, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

const Snacks = [
	"Potato Chips",
	"Chocolate Bar",
	"Chocolate Candy",
	"Cookies",
	"Peanut Butter Cups"
];

export class PurchaseSnackSystem extends System<SystemKind.PurchaseSnack> {
	private device: string;
	private player: Player;
	private desiredSnack: string;
	private complete: boolean;
	private layout: Map<string, string>;
	private socket: Socket;
	private buffer: Buffer;

	public constructor(id: number, device: string, player: Player) {
		super(SystemKind.PurchaseSnack, id);
		this.device = device;
		this.player = player;
		this.desiredSnack = Snacks[Math.floor(Math.random() * Snacks.length)];
		this.complete = false;
		this.layout = Map();
		this.socket = new Socket();
		this.buffer = Buffer.alloc(0);
	}

	public accept(game: Game, player: Player, device?: string): boolean {
		return device === this.device && player === this.player;
	}

	public attach(_game: Game, _player: Player) {
		this.socket = new Socket();
		this.socket.connect({
			host: process.env.PURCHASE_SNACK_HOST ?? "localhost",
			port: parseInt(process.env.PURCHASE_SNACK_PORT ?? "35360", 10)
		});
		this.socket.on("error", (error) => console.error(error));
		this.socket.on("data", this.onData.bind(this));
		this.buffer = Buffer.alloc(0);
		this.layout = Map();
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

		const action = PurchaseSnackAction.fromUnknown(actionJson);

		if (action.exit) {
			player.setSystem(game, game.level.movementSystem);
			return;
		}

		this.socket.write(`${action.selection}\n`, "latin1");
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
			const message = this.buffer.toString("latin1", 1, messageEnd);
			this.buffer = this.buffer.slice(messageEnd + 1);

			switch (messageType) {
				case ">": {
					const [location, snack] = message.split("\t");
					this.layout = this.layout.set(location, snack);
					break;
				}

				case "<": {
					this.player.pushUpdate(
						new GameUpdate.PurchaseSnackLayoutReady({
							layout: this.layout
						})
					);
					break;
				}

				case ":": {
					this.player.pushUpdate(
						new GameUpdate.PurchaseSnackOutput({
							event: "display",
							body: message
						})
					);
					break;
				}

				case "!": {
					if (message === this.desiredSnack) {
						this.complete = true;
						this.updatePlayers();
					}

					this.player.pushUpdate(
						new GameUpdate.PurchaseSnackOutput({
							event: "dispense",
							body: message
						})
					);
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
			desiredSnack: this.desiredSnack,
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
