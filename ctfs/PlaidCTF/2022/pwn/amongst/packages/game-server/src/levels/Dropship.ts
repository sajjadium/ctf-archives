import { getLevelMap } from "@amongst/data";

import { Game } from "../Game.js";
import { ResetSystem } from "../systems/ResetSystem.js";
import { SettingsSystem } from "../systems/SettingsSystem.js";
import { Level } from "./Level.js";

export class Dropship extends Level {
	private settingsSystem: SettingsSystem;
	private resetSystem: ResetSystem;

	public constructor() {
		super(getLevelMap("dropship"));
		this.settingsSystem = new SettingsSystem(this.getNextSystemId(), "computer");
		this.resetSystem = new ResetSystem(this.getNextSystemId(), "button");
	}

	public initialize(game: Game): void {
		super.initialize(game);
		this.systemMap = this.systemMap.set(this.settingsSystem.id, this.settingsSystem);
		this.systemMap = this.systemMap.set(this.resetSystem.id, this.resetSystem);
	}
}
