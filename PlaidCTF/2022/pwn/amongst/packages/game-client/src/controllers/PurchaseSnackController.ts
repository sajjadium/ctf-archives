import { List, Map } from "immutable";

import { PurchaseSnackAction, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { BasicController } from "./BasicController.js";
import { MovementController } from "./MovementController.js";

export class PurchaseSnackController extends BasicController<PurchaseSnackAction> {
	public readonly kind = SystemKind.PurchaseSnack;
	public state: SystemState.PurchaseSnack;
	public layout?: Map<string, string>;
	public display?: string;
	public dispensedSnacks: List<string>;
	public waiting: boolean;

	public constructor(state: SystemState.PurchaseSnack) {
		super();
		this.state = state;
		this.dispensedSnacks = List();
		this.waiting = true;
	}

	public send(selection: string) {
		this.queue.push(new PurchaseSnackAction({ exit: false, selection }));
		this.waiting = true;
	}

	public exit(game: Game, self: Self) {
		this.queue.push(new PurchaseSnackAction({ exit: true, selection: "" }));
		self.setController(game, new MovementController());
	}

	public receiveLayout(update: GameUpdate.PurchaseSnackLayoutReady): void {
		this.layout = update.layout;
		this.waiting = false;
	}

	public receiveOutput(update: GameUpdate.PurchaseSnackOutput): void {
		switch (update.event) {
			case "display": {
				this.display = update.body;
				this.waiting = false;
				break;
			}

			case "dispense": {
				this.dispensedSnacks = this.dispensedSnacks.push(update.body);
				this.waiting = false;
				break;
			}
		}
	}

	public attach(game: Game, self: Self) {
		super.attach(game, self);
		this.display = undefined;
		this.dispensedSnacks = List();
		this.waiting = true;
	}

	public detach(game: Game, self: Self): void {
		super.detach(game, self);
	}

	public updateState(state: SystemState.PurchaseSnack): void {
		this.state = state;
	}
}
