import { ResetAction, SystemKind, SystemState } from "@amongst/game-common";

import { Game } from "../Game.js";
import { Level } from "../levels/Level.js";
import { TheShelld } from "../levels/TheShelld.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

export class ResetSystem extends System<SystemKind.Reset> {
	private device: string;
	private resetTo?: new () => Level;

	public constructor(id: number, device: string) {
		super(SystemKind.Reset, id);
		this.device = device;
		this.resetTo = undefined;
	}

	public getStateForPlayer(_player: Player): SystemState | undefined {
		return {
			kind: this.kind,
			id: this.id,
			devices: [this.device]
		};
	}

	public accept(_game: Game, _player: Player, device?: string): boolean {
		return this.device === device;
	}

	public attach(_game: Game, _player: Player) {
		// nothing to do
	}

	public tick(
		game: Game,
		player: Player,
		actionJson?: unknown
	) {
		if (actionJson === undefined) {
			return;
		}

		const action = ResetAction.fromUnknown(actionJson);

		switch (action.action) {
			case "exit": {
				player.setSystem(game, game.level.movementSystem);
				break;
			}

			case "start": {
				this.resetTo = TheShelld;
				break;
			}
		}
	}

	public afterTick(game: Game) {
		if (this.resetTo !== undefined) {
			game.level = new this.resetTo();
			game.level.initialize(game);
		}
	}

	public detach(_game: Game, _player: Player) {
		// nothing to do
	}
}
