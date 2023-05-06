import { SystemKind, SystemState } from "@amongst/game-common";
import { VentAction } from "@amongst/game-common";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { MovementController } from ".";
import { BasicController } from "./BasicController.js";

export class VentController extends BasicController<VentAction> {
	public readonly kind = SystemKind.Vent;
	public state: SystemState.Vent;

	public constructor(state: SystemState.Vent) {
		super();
		this.state = state;
	}

	public attach(game: Game, self: Self) {
		super.attach(game, self);
	}

	public moveTo(game: Game, self: Self, target: string): void {
		if (this.state.devices.includes(target)) {
			const device = game.level.map.devices.get(target);

			if (device !== undefined) {
				this.queue.push(new VentAction({ target }));
				self.location = device.getBoundingBox().getCenter();
			}
		}
	}

	public exit(game: Game, self: Self): void {
		this.queue.push(new VentAction({ exit: true, target: "" }));
		self.setController(game, new MovementController());
	}

	public detach(game: Game, self: Self): void {
		super.detach(game, self);
	}
}
