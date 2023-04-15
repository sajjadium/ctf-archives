import gustSpritesheetUrl from "@assets/gusts.png";

import { Heading } from "@puzzled/types";

import { ScreenPoint } from "@/types/ScreenPoint.js";

const size = new ScreenPoint(90, 68);
const anchor = new ScreenPoint(45, 34);

export const GustSpritesheet = {
	url: gustSpritesheetUrl,
	size: new ScreenPoint(size.x * 2, size.y * 2)
};

export const GustFrames = {
	[Heading.East]: {
		offset: new ScreenPoint(0, 0),
		size,
		anchor
	},
	[Heading.North]: {
		offset: new ScreenPoint(size.x, 0),
		size,
		anchor
	},
	[Heading.West]: {
		offset: new ScreenPoint(0, size.y),
		size,
		anchor
	},
	[Heading.South]: {
		offset: new ScreenPoint(size.x, size.y),
		size,
		anchor
	}
};