import { ValueTransformer } from "typeorm";

import { Point } from "@puzzled/types";

interface TypeormPoint {
	x: number;
	y: number;
}

export class PointTransformer implements ValueTransformer {
	public to(value: unknown) {
		if (value instanceof Point) {
			return value.toPostgres();
		}
		return value; // wtf typeorm
	}

	public from(value: TypeormPoint) {
		return new Point(value.x, value.y);
	}
}
