import React from "react";

import { BrigFrames, BrigHaloSpritesheet, BrigSpritesheet } from "@/spritesheets/Brig.js";
import { ScreenPoint } from "@/types/ScreenPoint.js";

import { Ship } from "./Ship.js";
import { ShipProps } from "./ShipProps.js";

export const Brig = (props: ShipProps) => (
	<Ship
		{...props}
		influence={1.6}
		shipSpritesheet={BrigSpritesheet}
		shipFrames={BrigFrames}
		haloSpritesheet={BrigHaloSpritesheet}
		haloFrames={BrigFrames}
		nameOffset={new ScreenPoint(0, -58)}
	/>
);
