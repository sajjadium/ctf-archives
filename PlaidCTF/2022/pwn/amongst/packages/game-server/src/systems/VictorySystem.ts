import { HoldPurpose, SystemKind, SystemState } from "@amongst/game-common";

import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

export class VictorySystem extends System<SystemKind.Victory> {
	public constructor(id: number) {
		super(SystemKind.Victory, id);
	}

	public getStateForPlayer(_player: Player): SystemState | undefined {
		return undefined;
	}

	public accept(_game: Game, _player: Player): boolean {
		return false;
	}

	public attach(_game: Game, _player: Player) {
		throw new Error("Attaching to the victory system is not allowed");
	}

	public tick(_game: Game, _player: Player, _actionJson?: unknown) {
		throw new Error("Taking actions in the victory system is not allowed");
	}

	public afterTick(game: Game) {
		let livingHoaxers = 0;
		let livingShipmates = 0;

		game.players.forEach((player) => {
			if (!player.dead) {
				if (player.hoaxer) {
					livingHoaxers++;
				} else {
					livingShipmates++;
				}
			}
		});

		if (game.level.holdSystem.purpose.kind === HoldPurpose.Kind.GameEnd) {
			return;
		}

		// If all hoaxers are dead, then the shipmates win.
		if (livingHoaxers === 0) {
			game.level.holdSystem.init(game, game.tick + 10, new HoldPurpose.GameEnd(true));
			game.players.forEach((player) => {
				player.setSystem(game, game.level.holdSystem);
				player.desync();
			});
			return;
		}

		// If there are at least as many hoaxers as shipmates, then the hoaxers win.
		if (livingHoaxers >= livingShipmates) {
			game.level.holdSystem.init(game, game.tick + 10, new HoldPurpose.GameEnd(false));
			game.players.forEach((player) => {
				player.setSystem(game, game.level.holdSystem);
				player.desync();
			});
			return;
		}

		// If the shipmates finish all of their tasks, then the shipmates win.
		let allTasksComplete = true;

		for (const system of game.level.systems.values()) {
			if (system.blockVictory()) {
				allTasksComplete = false;
				break;
			}
		}

		if (allTasksComplete) {
			game.level.holdSystem.init(game, game.tick + 10, new HoldPurpose.GameEnd(true));
			game.players.forEach((player) => {
				player.setSystem(game, game.level.holdSystem);
				player.desync();
			});
			return;
		}

		// Otherwise, the game continues.
	}

	public detach(_game: Game, _player: Player) {
		throw new Error("Detaching from the victory system is not allowed");
	}
}
