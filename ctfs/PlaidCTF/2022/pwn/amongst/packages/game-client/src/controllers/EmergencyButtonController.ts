import { EmergencyButtonAction, SystemKind } from "@amongst/game-common";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { MovementController } from ".";
import { BasicController } from "./BasicController.js";

export class EmergencyButtonController extends BasicController<EmergencyButtonAction> {
	public readonly kind = SystemKind.EmergencyButton;

	public constructor() {
		super();
	}

	public attach(game: Game, self: Self) {
		super.attach(game, self);
	}

	public press(): void {
		this.queue.push(new EmergencyButtonAction({ action: "press" }));
		// don't bother setting the controller, because we're going to desync in a moment to get it set for us
	}

	public exit(game: Game, self: Self): void {
		this.queue.push(new EmergencyButtonAction({ action: "exit" }));
		self.setController(game, new MovementController());
	}

	public detach(game: Game, self: Self): void {
		super.detach(game, self);
	}
}
