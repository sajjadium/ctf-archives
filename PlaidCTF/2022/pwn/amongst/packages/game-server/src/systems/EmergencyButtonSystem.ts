import { EmergencyButtonAction, SystemKind, SystemState } from "@amongst/game-common";

import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

export class EmergencyButtonSystem extends System<SystemKind.EmergencyButton> {
	private device: string;
	private invokedBy: Player | undefined;

	public constructor(id: number, device: string) {
		super(SystemKind.EmergencyButton, id);
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
		if (player.dead || actionJson === undefined) {
			return;
		}

		const action = EmergencyButtonAction.fromUnknown(actionJson);

		switch (action.action) {
			case "exit": {
				player.setSystem(game, game.level.movementSystem);
				break;
			}

			case "press": {
				if (player.dead) {
					throw new Error("Player is dead");
				}

				if (player.emergencyMeetings === 0) {
					throw new Error("No emergency meetings left");
				}

				player.emergencyMeetings--;
				this.invokedBy = player;
				break;
			}
		}
	}

	public afterTick(game: Game) {
		if (this.invokedBy !== undefined) {
			game.level.meetingSystem.initMeeting(game, this.invokedBy.id, { kind: "emergency" });
			this.invokedBy = undefined;
		}
	}

	public detach(_game: Game, _player: Player) {
		// nothing to do
	}
}
