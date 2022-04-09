import { Box, Point, SpatiallyHashable } from "@amongst/geometry";

import { PlayerHeight, PlayerWidth } from "./constants.js";

export class Wall implements SpatiallyHashable {
	public constructor(
		public readonly start: Point,
		public readonly end: Point,
		public readonly transparent: boolean = false
	) {}

	public static fromJson(json: Wall.AsJson): Wall {
		return new Wall(
			Point.fromJson(json.start),
			Point.fromJson(json.end),
			json.transparent
		);
	}

	public getBoundingBox() {
		return Box.fromPoints(this.start, this.end);
	}

	public pushPlayer(point: Point): Point {
		// Compute the required displacement as if the player is a unit circle at the origin
		const start = this.start.sub(point).scale(2 / PlayerWidth, 2 / PlayerHeight);
		const end = this.end.sub(point).scale(2 / PlayerWidth, 2 / PlayerHeight);
		const lengthVector = end.sub(start);
		const lengthUnitVector = lengthVector.unit();
		const depthUnitVector = new Point(lengthUnitVector.y, -lengthUnitVector.x);
		const playerDepth = -depthUnitVector.dot(start);

		if (playerDepth < -1 || playerDepth > 1) {
			// Circle doesn't intersect the line
			return point;
		}

		const projectionDist = -lengthUnitVector.dot(start) / lengthVector.mag();

		if (projectionDist < 0 || projectionDist > 1) {
			// Circle intersects the line but not the segment
			return point;
		}

		const amountToPush = -1 - playerDepth;
		const pushVector = depthUnitVector.scale(amountToPush).scale(PlayerWidth / 2, PlayerHeight / 2);
		return point.add(pushVector);
	}
}

export namespace Wall {
	export interface AsJson {
		start: Point.AsJson;
		end: Point.AsJson;
		transparent?: boolean;
	}
}
