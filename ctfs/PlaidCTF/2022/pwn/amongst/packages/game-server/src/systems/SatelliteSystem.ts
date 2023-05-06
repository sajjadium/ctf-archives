import { SatelliteAction, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

const Flag = process.env.SATELLITE_FLAG ?? "PCTF{SAMPLE_FLAG_USE_ENV_PLS}";
const ExploreFlag = process.env.EXPLORE_FLAG ?? "PCTF{SAMPLE_FLAG_USE_ENV_PLS}";

export class SatelliteSystem extends System<SystemKind.Satellite> {
	private device: string;

	public constructor(id: number, device: string) {
		super(SystemKind.Satellite, id);
		this.device = device;
	}

	public getStateForPlayer(_player: Player): SystemState | undefined {
		return {
			kind: this.kind,
			id: this.id,
			devices: [this.device]
		};
	}

	public accept(_game: Game, player: Player, device?: string): boolean {
		return this.device === device;
	}

	public attach(_game: Game, player: Player) {
		if (!player.dead) {
			player.pushUpdate(
				new GameUpdate.SatelliteUpdate({
					flags: [Flag, ExploreFlag]
				})
			);
		}
	}

	public tick(
		game: Game,
		player: Player,
		actionJson?: unknown
	) {
		if (player.dead || actionJson === undefined) {
			return;
		}

		const action = SatelliteAction.fromUnknown(actionJson);

		switch (action.action) {
			case "exit": {
				player.setSystem(game, game.level.movementSystem);
				break;
			}
		}
	}

	public afterTick(_game: Game) {
		// nothing to do
	}

	public detach(_game: Game, _player: Player) {
		// nothing to do
	}
}
