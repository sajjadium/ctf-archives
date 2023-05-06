import { LevelMap } from "@amongst/game-common";

import { Dropship } from "./Dropship.js";
import { TheShelld } from "./TheShelld.js";

export function getLevelMap(id: string): LevelMap {
	switch (id) {
		case "shelld": return LevelMap.fromJson(TheShelld);
		case "dropship": return LevelMap.fromJson(Dropship);
		default: throw new Error(`Unknown level id: ${id}`);
	}
}
