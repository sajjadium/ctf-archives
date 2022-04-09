import { Set } from "immutable";

import { getLevelMap } from "@amongst/data";
import { HoldPurpose } from "@amongst/game-common";

import { Game } from "../Game.js";
import { ConspiracySystem } from "../systems/ConspiracySystem.js";
import { EmergencyButtonSystem } from "../systems/EmergencyButtonSystem.js";
import { FileTransferSystem } from "../systems/FileTransferSystem.js";
import { ProcessSampleSystem } from "../systems/ProcessSampleSystem.js";
import { ProvideCredentialsSystem } from "../systems/ProvideCredentialsSystem.js";
import { PurchaseSnackSystem } from "../systems/PurchaseSnackSystem.js";
import { RecalibrateEngineSystem } from "../systems/RecalibrateEngineSystem.js";
import { SatelliteSystem } from "../systems/SatelliteSystem.js";
import { System } from "../systems/System.js";
import { VentSystem } from "../systems/VentSystem.js";
import { VictorySystem } from "../systems/VictorySystem.js";
import { Level } from "./Level.js";

export class TheShelld extends Level {
	private emergencyButtonSystem: System;
	private ventSystems: System[];
	private victorySystem: VictorySystem;
	private taskSystems: System[];
	private conspiracySystem: ConspiracySystem;
	private satelliteSystem: SatelliteSystem;

	public constructor() {
		super(getLevelMap("shelld"));
		this.emergencyButtonSystem = new EmergencyButtonSystem(this.getNextSystemId(), "emergency-button");
		this.victorySystem = new VictorySystem(this.getNextSystemId());
		this.ventSystems = [
			new VentSystem(this.getNextSystemId(), Set.of("vent-communications", "vent-navigation")),
			new VentSystem(this.getNextSystemId(), Set.of("vent-cafeteria", "vent-medbay", "vent-electrical-east")),
			new VentSystem(this.getNextSystemId(), Set.of("vent-lower-engine", "vent-electrical-west", "vent-hallway"))
		];
		this.taskSystems = [];
		this.conspiracySystem = new ConspiracySystem(this.getNextSystemId(), "conspiracy-board");
		this.satelliteSystem = new SatelliteSystem(this.getNextSystemId(), "satellite");
	}

	public initialize(game: Game): void {
		super.initialize(game);

		// Choose a random player to be a hoaxer
		const hoaxerCount = game.players.size < 6 ? 1 : 2;
		const shuffledPlayers = [...game.players.values()];

		for (let i = shuffledPlayers.length - 1; i > 0; i--) {
			const j = Math.floor(Math.random() * (i + 1));
			const tmp = shuffledPlayers[i];
			shuffledPlayers[i] = shuffledPlayers[j];
			shuffledPlayers[j] = tmp;
		}

		const hoaxers = shuffledPlayers.slice(0, hoaxerCount);
		const shipmates = shuffledPlayers.slice(hoaxerCount);
		hoaxers.forEach((player) => {
			player.hoaxer = true;
		});

		// Distribute tasks to shipmates
		this.taskSystems = [];

		shipmates.forEach((player) => {
			this.taskSystems.push(
				new FileTransferSystem(this.getNextSystemId(), player, "data-download", "data-upload")
			);
			this.taskSystems.push(new ProvideCredentialsSystem(this.getNextSystemId(), "login", player));
			this.taskSystems.push(new PurchaseSnackSystem(this.getNextSystemId(), "vending", player));
			this.taskSystems.push(new RecalibrateEngineSystem(this.getNextSystemId(), "keypad", player));
		});

		for (let i = 0; i < Math.floor(shipmates.length / 2); i++) {
			this.taskSystems.push(
				new ProcessSampleSystem(this.getNextSystemId(), "centrifuge", shipmates[2 * i], shipmates[2 * i + 1])
			);
		}

		this.systemMap = (
			this.systemMap
				.set(this.emergencyButtonSystem.id, this.emergencyButtonSystem)
				.set(this.victorySystem.id, this.victorySystem)
				.set(this.conspiracySystem.id, this.conspiracySystem)
				.set(this.satelliteSystem.id, this.satelliteSystem)
		);

		for (const system of this.ventSystems) {
			this.systemMap = this.systemMap.set(system.id, system);
		}

		for (const system of this.taskSystems) {
			this.systemMap = this.systemMap.set(system.id, system);
		}

		this.holdSystem.init(game, game.tick + 100, new HoldPurpose.GameStart(hoaxerCount));

		game.players.forEach((player) => {
			player.setSystem(game, this.holdSystem);
		});
	}
}
