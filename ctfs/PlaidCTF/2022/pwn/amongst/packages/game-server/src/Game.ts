import type { Socket } from "socket.io";

import { Color, Direction, MsPerTick, PlayerVisualState } from "@amongst/game-common";
import { ClientEvent, GameUpdate, ServerEvent } from "@amongst/messages";

import { Body } from "./Body.js";
import { Dropship } from "./levels/Dropship.js";
import { Level } from "./levels/Level.js";
import { Player } from "./Player.js";

export class Game {
	public players: Map<string, Player>;
	public bodies: Map<string, Body>;
	public tick: number;
	public timeInfo?: {
		interval: NodeJS.Timeout;
		lastTick: number;
		partialTick: number;
	};
	public level: Level;

	public constructor() {
		this.players = new Map();
		this.bodies = new Map();
		this.tick = 0;
		this.level = new Dropship();
		this.level.initialize(this);
	}

	public isEmpty(): boolean {
		return this.players.size === 0;
	}

	public addPlayer(socket: Socket<ClientEvent, ServerEvent>, name: string) {
		let playerId = "";

		do {
			playerId = Math.random().toString(36).substring(2, 10);
		} while (this.players.has(playerId));

		const usedColors = new Set([...this.players.values()].map((player) => player.color));
		const color = Color.List.find((c) => !usedColors.has(c)) ?? Color.Red;
		const position = this.level.map.spawnPoints.get(color);

		if (position === undefined) {
			throw new Error("No spawn point for color");
		}

		const player = new Player(
			this,
			playerId,
			socket,
			name,
			color,
			position,
			{ kind: PlayerVisualState.Kind.Idle, direction: Direction.Right },
		);

		this.players.forEach((otherPlayer) => {
			otherPlayer.pushUpdate(
				new GameUpdate.PlayerJoined({
					id: player.id,
					name: player.name,
					color: player.color,
				})
			);
		});

		this.players.set(playerId, player);
		player.desync();

		return playerId;
	}

	public removePlayer(id: string) {
		const player = this.players.get(id);

		if (player === undefined) {
			throw new Error("Player not found");
		}

		player.teardown();
		this.players.delete(id);

		this.players.forEach((otherPlayer) => {
			otherPlayer.pushUpdate(
				new GameUpdate.PlayerLeft({
					id: player.id,
				})
			);
		});
	}

	public start() {
		this.timeInfo = {
			interval: setInterval(() => this.checkTick(), MsPerTick),
			lastTick: Date.now(),
			partialTick: 0,
		};
	}

	public stop() {
		if (this.timeInfo === undefined) {
			throw new Error("Game not started");
		}

		clearInterval(this.timeInfo.interval);
		this.timeInfo = undefined;
	}

	public disconnect() {
		this.players.forEach((player) => {
			player.socket.disconnect();
		});
	}

	private checkTick() {
		if (this.timeInfo === undefined) {
			throw new Error("Game not started");
		}

		try {
			const now = Date.now();
			const deltaMs = now - this.timeInfo.lastTick;
			const deltaTick = deltaMs / MsPerTick;
			this.timeInfo.lastTick = now;
			this.timeInfo.partialTick += deltaTick;

			while (this.timeInfo.partialTick >= 1) {
				this.timeInfo.partialTick -= 1;
				this.doTick();
			}
		} catch (error) {
			// We sometimes crash here after cleaning up a game, because it tries to tick extra times.
			// Log the error but don't crash.
			console.error(error);
		}
	}

	private doTick() {
		const actions = (
			[...this.players.values()]
				.map((player) => ({ player, action: player.getAction() }))
		);

		this.tick++;

		for (const { player, action } of actions) {
			try {
				player.system.tick(this, player, action);
			} catch (error) {
				// Something went wrong, probably invalid input from the player
				console.log(
					`Player ${player.id} desynced on tick ${this.tick}:`,
					error instanceof Error ? error.message : error
				);
				player.desync();
			}
		}

		for (const system of this.level.systems.values()) {
			system.afterTick(this);
		}

		for (const sourcePlayer of this.players.values()) {
			let visiblePlayers: GameUpdate.VisibilityUpdate.Player[] = [];
			let visibleBodies: GameUpdate.VisibilityUpdate.Body[] = [];

			for (const targetPlayer of this.players.values()) {
				if (sourcePlayer === targetPlayer) {
					continue;
				}

				if (sourcePlayer.canSeePlayer(targetPlayer)) {
					visiblePlayers.push(
						new GameUpdate.VisibilityUpdate.Player({
							id: targetPlayer.id,
							location: targetPlayer.location,
							visualState: targetPlayer.visualState,
							dead: targetPlayer.dead,
							hoaxer: sourcePlayer.hoaxer ? targetPlayer.hoaxer : undefined,
						})
					);
				}
			}

			for (const body of this.bodies.values()) {
				if (sourcePlayer.canSeeBody(body)) {
					visibleBodies.push(
						new GameUpdate.VisibilityUpdate.Body({
							id: body.id,
							color: body.color,
							location: body.location,
						})
					);
				}
			}

			const visibilityUpdate = new GameUpdate.VisibilityUpdate({
				players: visiblePlayers,
				bodies: visibleBodies,
			});

			if (sourcePlayer.desynced) {
				sourcePlayer.sync();
			}

			sourcePlayer.pushUpdate(visibilityUpdate);
			sourcePlayer.flushUpdates();
		}
	}
}
