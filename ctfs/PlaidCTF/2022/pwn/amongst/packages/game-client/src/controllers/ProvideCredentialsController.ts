import { ProvideCredentialsAction, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { BasicController } from "./BasicController.js";
import { MovementController } from "./MovementController.js";

export class ProvideCredentialsController extends BasicController<ProvideCredentialsAction> {
	public readonly kind = SystemKind.ProvideCredentials;
	public state: SystemState.ProvideCredentials;
	public lastResponse?: GameUpdate.ProvideCredentialsResponse;

	public constructor(state: SystemState.ProvideCredentials) {
		super();
		this.state = state;
	}

	public send(username: string, password: string) {
		this.queue.push(new ProvideCredentialsAction({ exit: false, username, password }));
	}

	public exit(game: Game, self: Self) {
		this.queue.push(new ProvideCredentialsAction({ exit: true, username: "", password: "" }));
		self.setController(game, new MovementController());
	}

	public receive(update: GameUpdate.ProvideCredentialsResponse): void {
		this.lastResponse = update;
	}

	public attach(game: Game, self: Self) {
		super.attach(game, self);
		this.lastResponse = undefined;
	}

	public detach(game: Game, self: Self): void {
		super.detach(game, self);
	}

	public updateState(state: SystemState.ProvideCredentials): void {
		this.state = state;
	}
}
