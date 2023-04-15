import cannonSpritesheetUrl from "@assets/cannon.png";

import { ScreenPoint } from "@/types/ScreenPoint.js";

const size = new ScreenPoint(15, 15);
const anchor = new ScreenPoint(7.5, 7.5);

export const CannonSpritesheet = {
	url: cannonSpritesheetUrl,
	size: new ScreenPoint(size.x * 4, size.y * 4)
};

export const CannonFrames = {
	// [1]: {
	// 	offset: new ScreenPoint(size.x * 0.5, 0),
	// 	size,
	// 	anchor
	// },
	// [2]: {
	// 	offset: new ScreenPoint(size.x * 1.5, 0),
	// 	size,
	// 	anchor
	// },
	// [3]: {
	// 	offset: new ScreenPoint(size.x * 2.5, 0),
	// 	size,
	// 	anchor
	// },
	cannonball: {
		offset: new ScreenPoint(0, 0),
		size,
		anchor
	},
	smoke1: {
		offset: new ScreenPoint(0, size.y),
		size,
		anchor
	},
	smoke2: {
		offset: new ScreenPoint(size.x, size.y),
		size,
		anchor
	},
	smoke3: {
		offset: new ScreenPoint(size.x * 2, size.y),
		size,
		anchor
	},
	hit1: {
		offset: new ScreenPoint(0, size.y * 2),
		size,
		anchor
	},
	hit2: {
		offset: new ScreenPoint(size.x, size.y * 2),
		size,
		anchor
	},
	hit3: {
		offset: new ScreenPoint(size.x * 2, size.y * 2),
		size,
		anchor
	},
	hit4: {
		offset: new ScreenPoint(size.x * 3, size.y * 2),
		size,
		anchor
	},
	splash1: {
		offset: new ScreenPoint(0, size.y * 3),
		size,
		anchor
	},
	splash2: {
		offset: new ScreenPoint(size.x, size.y * 3),
		size,
		anchor
	},
	splash3: {
		offset: new ScreenPoint(size.x * 2, size.y * 3),
		size,
		anchor
	},
	splash4: {
		offset: new ScreenPoint(size.x * 3, size.y * 3),
		size,
		anchor
	},
	blank: {
		offset: new ScreenPoint(size.x * 3, 0),
		size,
		anchor
	}
};