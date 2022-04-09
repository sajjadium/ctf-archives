import { SystemKind, SystemState } from "@amongst/game-common";
import { SettingsAction } from "@amongst/game-common/";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

export class SettingsSystem extends System<SystemKind.Settings> {
	private device: string;

	public constructor(id: number, device: string) {
		super(SystemKind.Settings, id);
		this.device = device;
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

		const action = SettingsAction.fromUnknown(actionJson);
		let updated = false;

		if (action.color !== undefined) {
			if (Array.from(game.players.values()).every((p) => p.color !== action.color)) {
				player.color = action.color;
				updated = true;
			}
		}

		if (action.name !== undefined && action.name !== "") {
			player.name = action.name;
			updated = true;
		}

		if (updated) {
			game.players.forEach((p) => {
				p.pushUpdate(
					new GameUpdate.PlayerChangedSettings({
						id: player.id,
						name: player.name,
						color: player.color
					})
				);
			});
		}

		if (action.exit) {
			player.setSystem(game, game.level.movementSystem);
		}
	}

	public afterTick(_game: Game) {
		// nothing to do
	}

	public detach(_game: Game, _player: Player) {
		// nothing to do
	}
}
