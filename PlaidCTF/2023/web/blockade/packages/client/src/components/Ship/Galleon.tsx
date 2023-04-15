import React from "react";

import { GalleonFrames, GalleonHaloSpritesheet, GalleonSpritesheet } from "@/spritesheets/Galleon.js";
import { ScreenPoint } from "@/types/ScreenPoint.js";

import { Ship } from "./Ship.js";
import { ShipProps } from "./ShipProps.js";

export const Galleon = (props: ShipProps) => (
	<Ship
		{...props}
		influence={3.2}
		shipSpritesheet={GalleonSpritesheet}
		shipFrames={GalleonFrames}
		haloSpritesheet={GalleonHaloSpritesheet}
		haloFrames={GalleonFrames}
		nameOffset={new ScreenPoint(0, -60)}
	/>
);
