import frigateSpritesheetUrl from "@assets/frigate.png";
import frigateHaloSpritesheetUrl from "@assets/frigate-halo.png";

import { HalfHeading } from "@/types/HalfHeading.js";
import { ScreenPoint } from "@/types/ScreenPoint.js";

const size = new ScreenPoint(90, 136);
const anchor = new ScreenPoint(45, 68);

export const FrigateSpritesheet = {
	url: frigateSpritesheetUrl,
	size: new ScreenPoint(size.x * 5, size.y)
};

export const FrigateHaloSpritesheet = {
	url: frigateHaloSpritesheetUrl,
	size: new ScreenPoint(size.x * 5, size.y)
};

export const FrigateFrames = {
	[HalfHeading.East]: {
		offset: new ScreenPoint(size.x * 0.5, 0),
		size,
		anchor
	},
	[HalfHeading.North]: {
		offset: new ScreenPoint(size.x * 1.5, 0),
		size,
		anchor
	},
	[HalfHeading.West]: {
		offset: new ScreenPoint(size.x * 2.5, 0),
		size,
		anchor
	},
	[HalfHeading.South]: {
		offset: new ScreenPoint(size.x * 3.5, 0),
		size,
		anchor
	},

	[HalfHeading.Northeast]: {
		offset: new ScreenPoint(size.x * 0.5, 0), // Doesn't actually matter, shouldn't be used...
		size,
		anchor
	},
	[HalfHeading.Northwest]: {
		offset: new ScreenPoint(size.x * 1.5, 0), // Doesn't actually matter, shouldn't be used...
		size,
		anchor
	},
	[HalfHeading.Southwest]: {
		offset: new ScreenPoint(size.x * 2.5, 0), // Doesn't actually matter, shouldn't be used...
		size,
		anchor
	},
	[HalfHeading.Southeast]: {
		offset: new ScreenPoint(size.x * 3.5, 0), // Doesn't actually matter, shouldn't be used...
		size,
		anchor
	}
};