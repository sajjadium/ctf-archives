import { RecalibrateEngineAction, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { BasicController } from "./BasicController.js";
import { MovementController } from "./MovementController.js";

export class RecalibrateEngineController extends BasicController<RecalibrateEngineAction> {
	public readonly kind = SystemKind.RecalibrateEngine;
	public state: SystemState.RecalibrateEngine;
	public display?: string;
	public flash?: { pattern: number[]; start: number };

	public constructor(state: SystemState.RecalibrateEngine) {
		super();
		this.state = state;
	}

	public send(button: number) {
		this.queue.push(new RecalibrateEngineAction({ button }));
	}

	public exit(game: Game, self: Self) {
		this.queue.push(new RecalibrateEngineAction({ button: 0 }));
		self.setController(game, new MovementController());
	}

	public receive(self: Self, update: GameUpdate.RecalibrateEngineUpdate): void {
		switch (update.event) {
			case "display": {
				this.display = update.body;
				break;
			}

			case "flash": {
				this.flash = { pattern: update.body.split("").map(Number), start: self.tick };
				break;
			}
		}
	}

	public attach(game: Game, self: Self) {
		super.attach(game, self);
		this.display = undefined;
		this.flash = undefined;
	}

	public detach(game: Game, self: Self): void {
		super.detach(game, self);
	}

	public updateState(state: SystemState.RecalibrateEngine): void {
		this.state = state;
	}
}
