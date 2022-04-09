import {
	ClientFloatingPointError,
	Direction,
	KillLag,
	KillRadius,
	MoveAction,
	PlayerSpeed,
	PlayerVisualState,
	ReportRadius,
	SystemKind,
	SystemState
} from "@amongst/game-common";

import { Body } from "../Body.js";
import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

export class MovementSystem extends System<SystemKind.Movement> {
	private pendingReportMeeting?: {
		invokedBy: string;
		body: string;
	};

	public constructor(id: number) {
		super(SystemKind.Movement, id);
	}

	public getStateForPlayer(_player: Player): SystemState | undefined {
		return {
			kind: this.kind,
			id: this.id,
			devices: []
		};
	}

	public accept(_game: Game, _player: Player, _device?: string): boolean {
		return true;
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
			actionJson = { delta: [0, 0] };
		}

		const action = MoveAction.fromUnknown(actionJson);

		if (action.delta.mag() > PlayerSpeed + ClientFloatingPointError) {
			throw new Error("Not allowed to move that fast");
		}

		player.location = player.location.add(action.delta);

		if (!player.dead) {
			player.location = game.level.map.applyWalls(player.location);
		}

		player.location = game.level.map.applyBounds(player.location);
		player.recentLocations.push(player.location);

		if (player.recentLocations.length > KillLag) {
			player.recentLocations.shift();
		}

		if (action.delta.isOrigin()) {
			player.visualState = {
				kind: PlayerVisualState.Kind.Idle,
				direction: player.visualState.direction,
			};
		} else {
			player.visualState = {
				kind: PlayerVisualState.Kind.Moving,
				direction: (
					action.delta.x < 0 ? Direction.Left :
					action.delta.x > 0 ? Direction.Right :
					player.visualState.direction
				),
				frame: ( // TODO: remove hardcoding?
					player.visualState.kind === PlayerVisualState.Kind.Moving ? (player.visualState.frame + 1) % 12 :
					0
				)
			};
		}

		const bonusAction = action.bonusAction;

		switch (bonusAction?.kind) {
			case MoveAction.BonusAction.Kind.Kill: {
				if (!player.hoaxer) {
					throw new Error("Player is not hoaxer");
				}

				if (player.dead) {
					throw new Error("Player is dead");
				}

				const target = game.players.get(bonusAction.target);

				if (target === undefined) {
					throw new Error("Target player not found");
				}

				if (target.hoaxer) {
					throw new Error("Target is hoaxer");
				}

				if (target.dead) {
					throw new Error("Target is already dead");
				}

				if (player.location.dist(bonusAction.at) > KillRadius) {
					throw new Error("Out of range");
				}

				if (
					!target.location.equals(bonusAction.at)
					&& target.recentLocations.every((location) => !location.equals(bonusAction.at))
				) {
					throw new Error("Target location not recent");
				}

				if (game.level.map.hasWallBetween(player.location, bonusAction.at)) {
					throw new Error("Blocked by wall");
				}

				player.location = bonusAction.at;
				target.dead = true;
				game.bodies.set(target.id, new Body(target.id, target.color, target.location));
				target.desync(); // Getting killed always causes a desync

				break;
			}

			case MoveAction.BonusAction.Kind.Interact: {
				const system = game.level.systems.get(bonusAction.system);

				if (system === undefined) {
					throw new Error("System not found");
				}

				const device = game.level.map.devices.get(bonusAction.device);

				if (device === undefined || !device.hitArea.contains(player.location)) {
					throw new Error("Failed to interact with device");
				}

				if (!system.accept(game, player, device.id)) {
					throw new Error("System rejected interaction");
				}

				player.setSystem(game, system);
				break;
			}

			case MoveAction.BonusAction.Kind.Report: {
				if (player.dead) {
					throw new Error("Player is dead");
				}

				const target = game.bodies.get(bonusAction.body);

				if (target === undefined) {
					throw new Error("Target body not found");
				}

				if (player.location.dist(target.location) > ReportRadius) {
					throw new Error("Out of range");
				}

				if (game.level.map.hasWallBetween(player.location, target.location, true)) {
					throw new Error("Blocked by wall");
				}

				this.pendingReportMeeting = {
					invokedBy: player.id,
					body: bonusAction.body
				};
			}
		}
	}

	public afterTick(game: Game): void {
		if (this.pendingReportMeeting !== undefined) {
			game.level.meetingSystem.initMeeting(
				game,
				this.pendingReportMeeting.invokedBy,
				{ kind: "body", body: this.pendingReportMeeting.body }
			);

			this.pendingReportMeeting = undefined;
		}
	}

	public detach(_game: Game, _player: Player) {
		// nothing to do
	}
}
