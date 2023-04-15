import galleonSpritesheetUrl from "@assets/galleon.png";
import galleonHaloSpritesheetUrl from "@assets/galleon-halo.png";

import { HalfHeading } from "@/types/HalfHeading.js";
import { ScreenPoint } from "@/types/ScreenPoint.js";

const size = new ScreenPoint(90, 136);
const anchor = new ScreenPoint(45, 68);

export const GalleonSpritesheet = {
	url: galleonSpritesheetUrl,
	size: new ScreenPoint(size.x * 5, size.y * 2)
};

export const GalleonHaloSpritesheet = {
	url: galleonHaloSpritesheetUrl,
	size: new ScreenPoint(size.x * 5, size.y * 2)
};

export const GalleonFrames = {
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
		offset: new ScreenPoint(size.x * 0.5, size.y),
		size,
		anchor
	},
	[HalfHeading.Northwest]: {
		offset: new ScreenPoint(size.x * 1.5, size.y),
		size,
		anchor
	},
	[HalfHeading.Southwest]: {
		offset: new ScreenPoint(size.x * 2.5, size.y),
		size,
		anchor
	},
	[HalfHeading.Southeast]: {
		offset: new ScreenPoint(size.x * 3.5, size.y),
		size,
		anchor
	}
};