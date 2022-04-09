import { Map } from "immutable";

import { getLevelMap } from "@amongst/data";
import { LevelMap, SystemState } from "@amongst/game-common";
import { LevelSync } from "@amongst/messages/src/ServerEvent";

export class Level {
	public map: LevelMap;
	public systems: Map<number, SystemState>;

	public constructor(map: LevelMap, systems: Map<number, SystemState>) {
		this.map = map;
		this.systems = systems;
	}

	public static fromSync(sync: LevelSync): Level {
		return new Level(
			getLevelMap(sync.map),
			Map(sync.systems.map((system) => [system.id, system] as [number, SystemState])),
		);
	}

	public updateSystemState(state: SystemState) {
		this.systems = this.systems.set(state.id, state);
	}

	public getSystemForDevice(device: string): SystemState | undefined {
		for (const system of this.systems.values()) {
			if (system.devices.includes(device)) {
				return system;
			}
		}

		return undefined;
	}
}
