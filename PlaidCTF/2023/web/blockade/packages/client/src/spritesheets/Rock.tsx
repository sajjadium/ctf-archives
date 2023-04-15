import rockSpritesheetUrl from "@assets/rocks.png";

import { ScreenPoint } from "@/types/ScreenPoint.js";

const size = new ScreenPoint(90, 68);
const anchor = new ScreenPoint(45, 34);

export const RockSpritesheet = {
	url: rockSpritesheetUrl,
	size: new ScreenPoint(size.x, size.y)
};

export const RockFrame = {
	offset: new ScreenPoint(0, 0),
	size,
	anchor
};
