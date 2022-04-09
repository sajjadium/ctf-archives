import { Color, SystemKind } from "@amongst/game-common";
import { SettingsAction } from "@amongst/game-common";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { MovementController } from ".";
import { BasicController } from "./BasicController.js";

export class SettingsController extends BasicController<SettingsAction> {
	public readonly kind = SystemKind.Settings;

	public constructor() {
		super();
	}

	public attach(game: Game, self: Self) {
		super.attach(game, self);
	}

	public update(color: Color, name: string): void {
		// Overwrite the entire queue, as this update will supercede all previous updates
		this.queue = [new SettingsAction({ exit: false, color, name })];
	}

	public exit(game: Game, self: Self): void {
		this.queue.push(new SettingsAction({ exit: true }));
		self.setController(game, new MovementController());
	}

	public detach(game: Game, self: Self): void {
		super.detach(game, self);
	}
}
