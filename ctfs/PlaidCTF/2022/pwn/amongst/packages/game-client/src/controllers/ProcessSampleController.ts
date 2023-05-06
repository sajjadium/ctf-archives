import { ProcessSampleAction, ProcessSampleTime, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { BasicController } from "./BasicController.js";
import { MovementController } from "./MovementController.js";

export class ProcessSampleController extends BasicController<ProcessSampleAction> {
	public readonly kind = SystemKind.ProcessSample;
	public state: SystemState.ProcessSample;
	public display?: string;

	public constructor(state: SystemState.ProcessSample) {
		super();
		this.state = state;
	}

	public begin(game: Game, self: Self) {
		this.queue.push(new ProcessSampleAction({ action: "begin" }));
		this.state.timerEndsAt = Math.floor(self.tick) + ProcessSampleTime;
	}

	public end(game: Game, self: Self) {
		this.queue.push(new ProcessSampleAction({ action: "end" }));
	}

	public exit(game: Game, self: Self) {
		this.queue.push(new ProcessSampleAction({ action: "exit" }));
		self.setController(game, new MovementController());
	}

	public updateDisplay(update: GameUpdate.ProcessSampleDisplayUpdate): void {
		this.display = update.content;
	}

	public attach(game: Game, self: Self) {
		super.attach(game, self);
	}

	public detach(game: Game, self: Self): void {
		super.detach(game, self);
	}

	public updateState(state: SystemState.ProcessSample): void {
		this.state = state;
	}
}
