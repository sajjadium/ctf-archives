import { Point as GamePoint } from "@puzzled/types";

import { HalfHeading } from "@/types/HalfHeading.js";

export interface ShipProps {
	className?: string;
	id: number;
	name: string;
	faction: number;
	location: GamePoint;
	heading: HalfHeading;
	sunk: boolean;
}
