import { Socket } from "socket.io-client";

import { SystemKind } from "@amongst/game-common";
import { Point } from "@amongst/geometry";
import { ClientEvent, GameSync, GameUpdate, GameUpdateBundle, ServerEvent } from "@amongst/messages";

import { Body } from "./Body.js";
import {
	ConspiracyController,
	FileTransferController,
	getController,
	HoldController,
	ProcessSampleController,
	PurchaseSnackController,
	RecalibrateEngineController,
	SatelliteController
} from "./controllers/index.js";
import { ProvideCredentialsController } from "./controllers/ProvideCredentialsController.js";
import { Level } from "./Level.js";
import { Player } from "./Player.js";
import { Self } from "./Self.js";

export class Game {
	public lastUpdate: number;
	public tick: number;
	public partialTick: number;
	public self: Self;
	public others: Map<string, Player>;
	public bodies: Map<string, Body>;
	public level: Level;

	public constructor(
		tick: number,
		partialTick: number,
		self: Self,
		others: Map<string, Player>,
		level: Level
	) {
		this.lastUpdate = Date.now();
		this.tick = tick;
		this.partialTick = partialTick;
		this.self = self;
		this.others = others;
		this.bodies = new Map();
		this.level = level;
	}

	public static fromSync(
		sync: GameSync,
		socket: Socket<ServerEvent, ClientEvent>
	) {
		const level = Level.fromSync(sync.level);

		const game = new Game(
			sync.tick,
			sync.partialTick,
			new Self(
				sync.self.id,
				socket,
				sync.self.name,
				sync.self.color,
				Point.fromJson(sync.self.location),
				sync.self.visualState,
				sync.self.dead,
				sync.self.hoaxer,
				sync.self.emergencyMeetings,
				sync.id,
				sync.nextPlayableTick + 10, // TODO: move this to a constant or something
				getController(level.systems.get(sync.self.system)!)
			),
			new Map(sync.others.map((player) => [player.id, new Player(player.id, player.name, player.color)])),
			level
		);

		game.self.controller.attach(game, game.self);
		return game;
	}

	public applyUpdates(bundle: GameUpdateBundle) {
		if (bundle.tick !== this.tick + 1) {
			// Not fatal, as this sometimes happens under normal circumstances (e.g. after desync)
			// eslint-disable-next-line no-console
			console.warn(`Tick mismatch: expected ${this.tick + 1}, got ${bundle.tick}`);
		}

		this.tick = bundle.tick;
		this.partialTick = bundle.partialTick;
		this.lastUpdate = Date.now();

		for (const updateJson of bundle.updates) {
			this.applyUpdate(GameUpdate.fromJson(updateJson));
		}
	}

	public copyFrom(other: Game) {
		this.tick = other.tick;
		this.self = other.self;
		this.others = other.others;
		this.bodies = other.bodies;
		this.level = other.level;
	}

	private applyUpdate(update: GameUpdate) {
		switch (update.kind) {
			case GameUpdate.Kind.PlayerJoined: {
				const player = new Player(update.id, update.name, update.color);
				this.others.set(update.id, player);
				return;
			}

			case GameUpdate.Kind.PlayerLeft: {
				this.others.delete(update.id);
				return;
			}

			case GameUpdate.Kind.VisibilityUpdate: {
				// Reset everything
				for (const player of this.others.values()) {
					player.location = undefined;
					player.visualState = undefined;
					player.dead = false;
					player.hoaxer = false;
				}

				this.bodies.clear();

				// Process the updates
				for (const playerUpdate of update.players) {
					const player = this.others.get(playerUpdate.id);

					if (player === undefined) {
						throw new Error(`Player ${playerUpdate.id} not found`);
					}

					player.location = playerUpdate.location;
					player.visualState = playerUpdate.visualState;
					player.dead = playerUpdate.dead;
					player.hoaxer = playerUpdate.hoaxer;
				}

				for (const bodyUpdate of update.bodies) {
					const body = new Body(bodyUpdate.id, bodyUpdate.color, bodyUpdate.location);
					this.bodies.set(body.id, body);
				}

				return;
			}

			case GameUpdate.Kind.PlayerChangedSettings: {
				const player = update.id === this.self.id ? this.self : this.others.get(update.id);

				if (player === undefined) {
					throw new Error(`Player ${update.id} not found`);
				}

				player.name = update.name;
				player.color = update.color;

				return;
			}

			case GameUpdate.Kind.SystemStateUpdate: {
				this.level.updateSystemState(update.state);

				// Also send the update to the controller, for controller types that support it
				if (
					update.state.kind === SystemKind.ProcessSample
					&& this.self.controller instanceof ProcessSampleController
					&& this.self.controller.state.id === update.state.id
				) {
					this.self.controller.updateState(update.state);
				}

				if (
					update.state.kind === SystemKind.ProvideCredentials
					&& this.self.controller instanceof ProvideCredentialsController
					&& this.self.controller.state.id === update.state.id
				) {
					this.self.controller.updateState(update.state);
				}

				if (
					update.state.kind === SystemKind.PurchaseSnack
					&& this.self.controller instanceof PurchaseSnackController
					&& this.self.controller.state.id === update.state.id
				) {
					this.self.controller.updateState(update.state);
				}

				if (
					update.state.kind === SystemKind.RecalibrateEngine
					&& this.self.controller instanceof RecalibrateEngineController
					&& this.self.controller.state.id === update.state.id
				) {
					this.self.controller.updateState(update.state);
				}

				if (
					update.state.kind === SystemKind.Hold
					&& this.self.controller instanceof HoldController
					&& this.self.controller.state.id === update.state.id
				) {
					this.self.controller.updateState(update.state);
				}

				return;
			}

			case GameUpdate.Kind.FileDownloadPacket: {
				if (
					this.self.controller instanceof FileTransferController
					&& this.self.controller.state.id === update.id
				) {
					this.self.controller.receive(this, this.self, update);
				}
				return;
			}

			case GameUpdate.Kind.ProcessSampleDisplayUpdate: {
				if (this.self.controller instanceof ProcessSampleController) {
					this.self.controller.updateDisplay(update);
				}
				return;
			}

			case GameUpdate.Kind.ProvideCredentialsResponse: {
				if (this.self.controller instanceof ProvideCredentialsController) {
					this.self.controller.receive(update);
				}
				return;
			}

			case GameUpdate.Kind.PurchaseSnackLayoutReady: {
				if (this.self.controller instanceof PurchaseSnackController) {
					this.self.controller.receiveLayout(update);
				}
				return;
			}

			case GameUpdate.Kind.PurchaseSnackOutput: {
				if (this.self.controller instanceof PurchaseSnackController) {
					this.self.controller.receiveOutput(update);
				}
				return;
			}

			case GameUpdate.Kind.RecalibrateEngineUpdate: {
				if (this.self.controller instanceof RecalibrateEngineController) {
					this.self.controller.receive(this.self, update);
				}
				return;
			}

			case GameUpdate.Kind.ConspiracyUpdate: {
				if (this.self.controller instanceof ConspiracyController) {
					this.self.controller.updateFlag(update);
				}
				return;
			}

			case GameUpdate.Kind.SatelliteUpdate: {
				if (this.self.controller instanceof SatelliteController) {
					this.self.controller.updateFlag(update);
				}
				return;
			}
		}
	}
}
