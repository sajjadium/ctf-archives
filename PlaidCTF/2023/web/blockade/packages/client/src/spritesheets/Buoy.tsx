import buoySpritesheetUrl from "@assets/buoy.png";

import { ScreenPoint } from "@/types/ScreenPoint.js";

const size = new ScreenPoint(90, 136);
const anchor = new ScreenPoint(45, 68);

export const BuoySpritesheet = {
	url: buoySpritesheetUrl,
	size: new ScreenPoint(size.x * 4, size.y)
};

export const BuoyFrames = {
	[1]: {
		offset: new ScreenPoint(size.x * 0.5, 0),
		size,
		anchor
	},
	[2]: {
		offset: new ScreenPoint(size.x * 1.5, 0),
		size,
		anchor
	},
	[3]: {
		offset: new ScreenPoint(size.x * 2.5, 0),
		size,
		anchor
	},
};