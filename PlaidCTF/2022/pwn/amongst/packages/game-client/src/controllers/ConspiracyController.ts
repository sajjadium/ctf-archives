import { ConspiracyAction, ProcessSampleAction, ProcessSampleTime, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { BasicController } from "./BasicController.js";
import { MovementController } from "./MovementController.js";

export class ConspiracyController extends BasicController<ConspiracyAction> {
	public readonly kind = SystemKind.Conspiracy;
	public state: SystemState.Conspiracy;
	public flags?: string[];

	public constructor(state: SystemState.Conspiracy) {
		super();
		this.state = state;
	}

	public exit(game: Game, self: Self) {
		this.queue.push(new ConspiracyAction({ action: "exit" }));
		self.setController(game, new MovementController());
	}

	public updateFlag(update: GameUpdate.ConspiracyUpdate): void {
		this.flags = update.flags;
	}

	public attach(game: Game, self: Self) {
		super.attach(game, self);
	}

	public detach(game: Game, self: Self): void {
		super.detach(game, self);
	}
}
