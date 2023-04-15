import React from "react";

import { SloopFrames, SloopHaloSpritesheet, SloopSpritesheet } from "@/spritesheets/Sloop.js";
import { ScreenPoint } from "@/types/ScreenPoint.js";

import { Ship } from "./Ship.js";
import { ShipProps } from "./ShipProps.js";

export const Sloop = (props: ShipProps) => (
	<Ship
		{...props}
		influence={0.8}
		shipSpritesheet={SloopSpritesheet}
		shipFrames={SloopFrames}
		haloSpritesheet={SloopHaloSpritesheet}
		haloFrames={SloopFrames}
		nameOffset={new ScreenPoint(0, -45)}
	/>
);
