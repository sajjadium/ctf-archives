import sloopSpritesheetUrl from "@assets/sloop.png";
import sloopHaloSpritesheetUrl from "@assets/sloop-halo.png";

import { HalfHeading } from "@/types/HalfHeading.js";
import { ScreenPoint } from "@/types/ScreenPoint.js";

const size = new ScreenPoint(90, 68);
const anchor = new ScreenPoint(45, 34);

export const SloopSpritesheet = {
	url: sloopSpritesheetUrl,
	size: new ScreenPoint(size.x * 4, size.y * 2)
};

export const SloopHaloSpritesheet = {
	url: sloopHaloSpritesheetUrl,
	size: new ScreenPoint(size.x * 4, size.y * 2)
};

export const SloopFrames = {
	[HalfHeading.East]: {
		offset: new ScreenPoint(0, 0),
		size,
		anchor
	},
	[HalfHeading.North]: {
		offset: new ScreenPoint(size.x, 0),
		size,
		anchor
	},
	[HalfHeading.West]: {
		offset: new ScreenPoint(size.x * 2, 0),
		size,
		anchor
	},
	[HalfHeading.South]: {
		offset: new ScreenPoint(size.x * 3, 0),
		size,
		anchor
	},

	[HalfHeading.Northeast]: {
		offset: new ScreenPoint(0, size.y),
		size,
		anchor
	},
	[HalfHeading.Northwest]: {
		offset: new ScreenPoint(size.x, size.y),
		size,
		anchor
	},
	[HalfHeading.Southwest]: {
		offset: new ScreenPoint(size.x * 2, size.y),
		size,
		anchor
	},
	[HalfHeading.Southeast]: {
		offset: new ScreenPoint(size.x * 3, size.y),
		size,
		anchor
	}
};