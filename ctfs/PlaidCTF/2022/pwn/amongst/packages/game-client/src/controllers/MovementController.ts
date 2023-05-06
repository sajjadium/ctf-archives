import {
	ClientKillRadius,
	Direction,
	MoveAction,
	PlayerSpeed,
	PlayerVisualState,
	ReportRadius,
	SystemKind,
	SystemState
} from "@amongst/game-common";
import { Point } from "@amongst/geometry";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { getController } from "./index.js";

export class MovementController {
	public readonly kind = SystemKind.Movement;
	public partialMovement: Point;
	public displayLocation: Point;
	public displayVisualState: PlayerVisualState;

	public constructor() {
		this.partialMovement = Point.Origin;

		// These don't matter, since we'll get attached before they get read
		this.displayLocation = Point.Origin;
		this.displayVisualState = { kind: PlayerVisualState.Kind.Idle, direction: Direction.Left };
	}

	public attach(game: Game, self: Self) {
		this.partialMovement = Point.Origin;
		this.displayLocation = self.location;
		this.displayVisualState = self.visualState;
	}

	public advance(
		game: Game,
		self: Self,
		amount: number,
		movement: Point,
		interact: boolean,
		kill: boolean,
		report: boolean
	) {
		while (amount > 0) {
			const tickFinishTime = Math.floor(self.tick + 1) - self.tick;
			const step = Math.min(amount, tickFinishTime);
			game.self.tick += step;
			const newSystem = this.partialAdvance(
				game,
				self,
				step,
				step === tickFinishTime,
				movement,
				interact,
				kill,
				report
			);
			amount -= step;

			if (newSystem !== undefined) {
				self.setController(game, getController(newSystem));
				break;
			}
		}
	}

	public partialAdvance(
		game: Game,
		self: Self,
		amount: number,
		finishTick: boolean,
		movement: Point,
		interact: boolean,
		kill: boolean,
		report: boolean
	): SystemState | undefined {
		this.partialMovement = this.partialMovement.add(movement.scale(amount * PlayerSpeed));

		this.displayLocation = self.location.add(this.partialMovement);

		if (!self.dead) {
			this.displayLocation = game.level.map.applyWalls(this.displayLocation);
			this.displayLocation = game.level.map.applyBounds(this.displayLocation);
		}

		this.displayVisualState = (
			this.partialMovement.isOrigin()
				? { kind: PlayerVisualState.Kind.Idle, direction: self.visualState.direction }
				: {
					kind: PlayerVisualState.Kind.Moving,
					direction: (
						this.partialMovement.x < 0 ? Direction.Left :
						this.partialMovement.x > 0 ? Direction.Right :
						self.visualState.direction
					),
					frame: (
						self.visualState.kind === PlayerVisualState.Kind.Moving
							? (self.visualState.frame + 1) % 12
							: 0
					)
				}
		);

		if (finishTick) {
			self.location = this.displayLocation;
			self.visualState = this.displayVisualState;

			const delta = this.partialMovement;


			this.partialMovement = Point.Origin;

			if (interact) {
				const device = game.level.map.getDeviceAtPoint(self.location);

				if (device !== undefined) {
					const system = game.level.getSystemForDevice(device.id);

					if (system !== undefined) {
						const action = new MoveAction({
							delta,
							bonusAction: new MoveAction.BonusAction.Interact({
								system: system.id,
								device: device.id
							})
						});

						self.socket.emit("action", {
							syncId: self.syncId,
							tick: Math.round(self.tick),
							action: action.toJson()
						});

						return system;
					}
				}
			} else if (self.hoaxer && kill && !self.dead) {
				// Target the closest valid non-hoaxer
				const players = (
					Array.from(game.others.values())
						.filter((player) => player.location !== undefined)
						.filter((player) => player.hoaxer !== true)
						.filter((player) => !player.dead)
						.sort((a, b) => a.location!.dist(self.location) - b.location!.dist(self.location))
				);

				for (const target of players) {
					if (game.level.map.hasWallBetween(self.location, target.location!)) {
						continue;
					}

					if (target.location!.dist(self.location) <= ClientKillRadius) {
						const action = new MoveAction({
							delta,
							bonusAction: new MoveAction.BonusAction.Kill({
								target: target.id,
								at: target.location!
							})
						});

						self.location = target.location!;

						self.socket.emit("action", {
							syncId: self.syncId,
							tick: Math.round(self.tick),
							action: action.toJson()
						});

						return undefined;
					}
				}
			} else if (report && !self.dead) {
				// Target the closest valid body
				const bodies = (
					Array.from(game.bodies.values())
						.sort((a, b) => a.location.dist(self.location) - b.location.dist(self.location))
						.filter((body) => !game.level.map.hasWallBetween(self.location, body.location, true))
				);

				if (bodies.length > 0) {
					const target = bodies[0];

					if (target.location.dist(self.location) <= ReportRadius) {
						const action = new MoveAction({
							delta,
							bonusAction: new MoveAction.BonusAction.Report({
								body: target.id
							})
						});

						self.socket.emit("action", {
							syncId: self.syncId,
							tick: Math.round(self.tick),
							action: action.toJson()
						});

						return undefined;
					}
				}
			}

			if (!delta.isOrigin()) {
				const action = new MoveAction({ delta });
				self.socket.emit("action", {
					syncId: self.syncId,
					tick: Math.round(self.tick),
					action: action.toJson()
				});
			}
		}

		return undefined;
	}

	public detach(_game: Game, _self: Self) {
		// nothing to do
	}
}
