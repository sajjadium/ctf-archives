import { Game } from "../Game.js";
import { Self } from "../Self.js";

export abstract class BasicController<T extends { toJson: () => unknown }> {
	public queue: T[];

	public constructor() {
		this.queue = [];
	}

	public attach(_game: Game, _self: Self) {
		this.queue = [];
	}

	public advance(
		game: Game,
		self: Self,
		amount: number
	) {
		for (let i = Math.floor(game.self.tick + 1); i < game.self.tick + amount; i++) {
			this.beforeTick(game, self);
			const action = this.queue.shift();

			if (action !== undefined) {
				self.socket.emit("action", { syncId: self.syncId, tick: i, action: action.toJson() });
			}
		}

		game.self.tick += amount;
	}

	public detach(game: Game, self: Self) {
		// If the queue isn't empty, we need to send the remaining actions or else we might desync.
		// This might move the player further ahead of the server than usual, but they should recover pretty quickly.
		while (true) {
			const action = this.queue.shift();

			if (action === undefined) {
				break;
			}

			game.self.tick = Math.floor(game.self.tick + 1);
			self.socket.emit("action", { syncId: self.syncId, tick: game.self.tick, action: action.toJson() });
		}
	}

	protected beforeTick(_game: Game, _self: Self) {
		// Inheriting classes may use this to do something every tick.
	}
}
