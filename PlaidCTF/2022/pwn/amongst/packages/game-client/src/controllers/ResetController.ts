import { ResetAction, SystemKind } from "@amongst/game-common";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { MovementController } from ".";
import { BasicController } from "./BasicController.js";

export class ResetController extends BasicController<ResetAction> {
	public readonly kind = SystemKind.Reset;

	public constructor() {
		super();
	}

	public attach(game: Game, self: Self) {
		super.attach(game, self);
	}

	public reset(game: Game, self: Self): void {
		// this.queue.push(new ResetAction({ action: "reset" }));
		// don't set controller, because it doesn't matter
		const action = new ResetAction({ action: "start" });
		self.socket.emit("action", { syncId: self.syncId, tick: 995, action: action.toJson() });
	}

	public exit(game: Game, self: Self): void {
		this.queue.push(new ResetAction({ action: "exit" }));
		self.setController(game, new MovementController());
	}

	public start(): void {
		this.queue.push(new ResetAction({ action: "start" }));
	}

	public detach(game: Game, self: Self): void {
		super.detach(game, self);
	}
}
