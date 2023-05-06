import { SatelliteAction, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { BasicController } from "./BasicController.js";
import { MovementController } from "./MovementController.js";

export class SatelliteController extends BasicController<SatelliteAction> {
	public readonly kind = SystemKind.Satellite;
	public state: SystemState.Satellite;
	public flags?: string[];

	public constructor(state: SystemState.Satellite) {
		super();
		this.state = state;
	}

	public exit(game: Game, self: Self) {
		this.queue.push(new SatelliteAction({ action: "exit" }));
		self.setController(game, new MovementController());
	}

	public updateFlag(update: GameUpdate.SatelliteUpdate): void {
		this.flags = update.flags;
	}

	public attach(game: Game, self: Self) {
		super.attach(game, self);
	}

	public detach(game: Game, self: Self): void {
		super.detach(game, self);
	}
}
