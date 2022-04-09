import { Set } from "immutable";

import { SystemKind, SystemState, VentAction } from "@amongst/game-common";

import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

export class VentSystem extends System<SystemKind.Vent> {
	private devices: Set<string>;

	public constructor(id: number, devices: Set<string>) {
		super(SystemKind.Vent, id);
		this.devices = devices;
	}

	public getStateForPlayer(player: Player): SystemState | undefined {
		if (!player.hoaxer) {
			return undefined;
		}

		return {
			kind: this.kind,
			id: this.id,
			devices: this.devices.toArray()
		};
	}

	public accept(_game: Game, player: Player, device?: string): boolean {
		return player.hoaxer && device !== undefined && this.devices.has(device);
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

		const action = VentAction.fromUnknown(actionJson);

		if (action.exit === true) {
			player.setSystem(game, game.level.movementSystem);
			return;
		}

		if (this.devices.has(action.target)) {
			const device = game.level.map.devices.get(action.target);
			if (device !== undefined) {
				player.location = device.getBoundingBox().getCenter();
			}
		}
	}

	public afterTick(_game: Game): void {
		// nothing to do
	}

	public detach(_game: Game, _player: Player) {
		// nothing to do
	}
}
