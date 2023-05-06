import type { Socket } from "socket.io";

import { Color, PlayerVisualState, ShortVisibilityRadius, SystemKind, SystemState, VisibilityRadius } from "@amongst/game-common";
import { Point } from "@amongst/geometry";
import { ClientEvent, GameUpdate, ServerEvent, TickAction } from "@amongst/messages";

import { Body } from "./Body.js";
import { Game } from "./Game.js";
import { System } from "./systems/System.js";

export class Player {
	public game: Game;
	public id: string;
	public socket: Socket<ClientEvent, ServerEvent>;
	public name: string;
	public color: Color;
	public location: Point;
	public visualState: PlayerVisualState;
	public pendingUpdates: GameUpdate[];
	public pendingActions: TickAction[];
	public nextPlayableTick: number;
	public system: System;
	public dead: boolean;
	public hoaxer: boolean;
	public recentLocations: Point[];
	public emergencyMeetings: number;
	public desynced: boolean;
	public syncId: number;

	private onReceiveAction = this.$onReceiveAction.bind(this);
	private onRequestSync = this.$onRequestSync.bind(this);

	public constructor(
		game: Game,
		id: string,
		socket: Socket,
		name: string,
		color: Color,
		location: Point,
		visualState: PlayerVisualState
	) {
		this.game = game;
		this.id = id;
		this.socket = socket;
		this.name = name;
		this.color = color;
		this.location = location;
		this.visualState = visualState;
		this.pendingUpdates = [];
		this.pendingActions = [];
		this.nextPlayableTick = 0;
		this.system = game.level.movementSystem;
		this.dead = false;
		this.hoaxer = false;
		this.recentLocations = [];
		this.desynced = false;
		this.syncId = 0;
		this.emergencyMeetings = 1;

		this.socket.on("action", this.onReceiveAction);
		this.socket.on("requestSync", this.onRequestSync);
	}

	public pushUpdate(update: GameUpdate): void {
		this.pendingUpdates.push(update);
	}

	public flushUpdates(): void {
		this.socket.emit("update", {
			tick: this.game.tick,
			partialTick: this.game.tick + this.game.timeInfo!.partialTick,
			updates: this.pendingUpdates.map((update) => update.toJson())
		});
		this.pendingUpdates = [];
	}

	public getAction(): unknown {
		if (this.pendingActions.length === 0 || this.pendingActions[0].tick !== this.game.tick) {
			// no actions for this tick
			return undefined;
		}

		return this.pendingActions.shift()!.action;
	}

	public canSeePlayer(target: Player): boolean {
		if (target.system.kind === SystemKind.Vent) {
			return false;
		}

		if (this.dead) {
			return true;
		}

		if (target.dead) {
			return false;
		}

		const dist = target.location.dist(this.location);

		if (dist < ShortVisibilityRadius) {
			return true;
		}

		if (dist < VisibilityRadius && !this.game.level.map.hasWallBetween(this.location, target.location, true)) {
			return true;
		}

		return false;
	}

	public canSeeBody(target: Body): boolean {
		if (this.dead) {
			return true;
		}

		const dist = target.location.dist(this.location);

		if (dist < ShortVisibilityRadius) {
			return true;
		}

		if (dist < VisibilityRadius && !this.game.level.map.hasWallBetween(this.location, target.location, true)) {
			return true;
		}

		return false;
	}

	public teardown(): void {
		this.socket.off("action", this.onReceiveAction);
		this.socket.off("requestSync", this.onRequestSync);
	}

	public desync() {
		this.desynced = true;
	}

	public sync() {
		this.desynced = false;
		this.syncId++;
		this.socket.emit("sync", {
			id: this.syncId,
			tick: this.game.tick,
			partialTick: this.game.tick + this.game.timeInfo!.partialTick,
			nextPlayableTick: this.game.tick + 1,
			self: {
				id: this.id,
				name: this.name,
				color: this.color,
				location: this.location.toJson(),
				visualState: this.visualState,
				system: this.system.id,
				dead: this.dead,
				hoaxer: this.hoaxer,
				emergencyMeetings: this.emergencyMeetings,
			},
			others: (
				[...this.game.players.values()]
					.filter((player) => player !== this)
					.map((player) => ({
						id: player.id,
						name: player.name,
						color: player.color,
					}))
			),
			level: {
				map: this.game.level.map.id,
				systems: (
					this.game.level.systems.valueSeq()
						.map((system) => system.getStateForPlayer(this))
						.filter((state): state is SystemState => state !== undefined)
						.toArray()
				)
			}
		});

		this.pendingActions = [];
		this.pendingUpdates = [];
		this.nextPlayableTick = this.game.tick + 1;
	}

	public setSystem(game: Game, system: System): void {
		this.system.detach(game, this);
		this.system = system;
		this.system.attach(game, this);
	}

	private $onReceiveAction(tickAction: TickAction): void {
		if (tickAction.tick <= this.game.tick) {
			// eslint-disable-next-line no-console
			console.log(
				"[DESYNC]",
				`Rejection action from player ${this.id} for tick ${tickAction.tick}`,
				"(trying to play in the past)"
			);
			// This counts as a desync since the player's state will diverge from ours
			this.desync();
			return;
		}

		if (tickAction.tick < this.nextPlayableTick) {
			// eslint-disable-next-line no-console
			console.log(
				`Rejection action from player ${this.id} for tick ${tickAction.tick}`,
				"(trying to play before the next playable tick)"
			);
			// Probably not a desync?
			return;
		}

		if (tickAction.syncId !== this.syncId) {
			// eslint-disable-next-line no-console
			console.log(
				`Rejection action from player ${this.id} for tick ${tickAction.tick}`,
				"(trying to play on the incorrect sync id)"
			);
			// Don't count this as a desync, since we might already be recovering from one
			return;
		}

		this.pendingActions.push(tickAction);
		this.nextPlayableTick = tickAction.tick + 1;
	}

	private $onRequestSync(): void {
		this.desync();
	}
}
