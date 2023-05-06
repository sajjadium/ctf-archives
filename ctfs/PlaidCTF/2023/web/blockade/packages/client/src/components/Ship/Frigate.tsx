import React from "react";

import { FrigateFrames, FrigateHaloSpritesheet, FrigateSpritesheet } from "@/spritesheets/Frigate.js";
import { ScreenPoint } from "@/types/ScreenPoint.js";

import { Ship } from "./Ship.js";
import { ShipProps } from "./ShipProps.js";

export const Frigate = (props: ShipProps) => (
	<Ship
		{...props}
		influence={4.8}
		shipSpritesheet={FrigateSpritesheet}
		shipFrames={FrigateFrames}
		haloSpritesheet={FrigateHaloSpritesheet}
		haloFrames={FrigateFrames}
		nameOffset={new ScreenPoint(0, -80)}
	/>
);
