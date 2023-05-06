import { Map } from "immutable";

import { LevelMap } from "@amongst/game-common";

import { Game } from "../Game.js";
import { HoldSystem } from "../systems/HoldSystem.js";
import { MeetingSystem } from "../systems/MeetingSystem.js";
import { MovementSystem } from "../systems/MovementSystem.js";
import { System } from "../systems/System.js";

export abstract class Level {
	public readonly map: LevelMap;
	public readonly movementSystem: MovementSystem;
	public readonly meetingSystem: MeetingSystem;
	public readonly holdSystem: HoldSystem;
	protected systemMap: Map<number, System>;
	private systemIdCounter: number;

	public constructor(map: LevelMap) {
		this.map = map;
		this.systemIdCounter = 0;
		this.movementSystem = new MovementSystem(this.getNextSystemId());
		this.meetingSystem = new MeetingSystem(this.getNextSystemId());
		this.holdSystem = new HoldSystem(this.getNextSystemId());
		this.systemMap = Map();
	}

	public get systems() {
		return this.systemMap;
	}

	public initialize(game: Game): void {
		game.players.forEach((player) => {
			const spawnPoint = this.map.spawnPoints.get(player.color);

			if (spawnPoint === undefined) {
				throw new Error(`No spawn point for player ${player.color}`);
			}

			player.location = spawnPoint;
			player.dead = false;
			player.hoaxer = false;
			player.setSystem(game, this.movementSystem);
			player.desync();
		});

		game.bodies.clear();

		this.systemMap = Map<number, System>([
			[this.movementSystem.id, this.movementSystem],
			[this.meetingSystem.id, this.meetingSystem],
			[this.holdSystem.id, this.holdSystem],
		]);
	}

	protected getNextSystemId(): number {
		this.systemIdCounter++;
		return this.systemIdCounter;
	}
}
