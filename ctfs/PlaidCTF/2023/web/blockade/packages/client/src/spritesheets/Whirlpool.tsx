import whirlpoolSpritesheetUrl from "@assets/whirlpools.png";

import { ScreenPoint } from "@/types/ScreenPoint.js";

const size = new ScreenPoint(180, 136);
const anchor = new ScreenPoint(90, 68);

export const WhirlpoolSpritesheet = {
	url: whirlpoolSpritesheetUrl,
	size: new ScreenPoint(size.x * 2, size.y)
};

export const WhirlpoolFrames = {
	clockwise: {
		offset: new ScreenPoint(0, 0),
		size,
		anchor
	},
	counterclockwise: {
		offset: new ScreenPoint(size.x, 0),
		size,
		anchor
	}
};