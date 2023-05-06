import { Point } from "./Point.js";
import { SpatiallyHashable } from "./SpatialHashMap.js";

export class Box implements SpatiallyHashable {
	public constructor(
		public readonly topLeft: Point,
		public readonly bottomRight: Point,
	) {}

	public static fromJson(json: Box.AsJson) {
		return new Box(
			Point.fromJson(json[0]),
			Point.fromJson(json[1]),
		);
	}

	public static fromPoints(...points: Point[]): Box {
		const minX = Math.min(...points.map((p) => p.x));
		const minY = Math.min(...points.map((p) => p.y));
		const maxX = Math.max(...points.map((p) => p.x));
		const maxY = Math.max(...points.map((p) => p.y));

		return new Box(
			new Point(minX, minY),
			new Point(maxX, maxY),
		);
	}

	public intersects(other: Box): boolean {
		return (
			this.topLeft.x <= other.bottomRight.x &&
			this.topLeft.y <= other.bottomRight.y &&
			this.bottomRight.x >= other.topLeft.x &&
			this.bottomRight.y >= other.topLeft.y
		);
	}

	public union(other: Box): Box {
		return new Box(
			new Point(
				Math.min(this.topLeft.x, other.topLeft.x),
				Math.min(this.topLeft.y, other.topLeft.y),
			),
			new Point(
				Math.max(this.bottomRight.x, other.bottomRight.x),
				Math.max(this.bottomRight.y, other.bottomRight.y),
			),
		);
	}

	public scale(s: number) {
		return new Box(
			this.topLeft.scale(s),
			this.bottomRight.scale(s),
		);
	}

	public getBoundingBox(): Box {
		return this;
	}

	public getCenter(): Point {
		return this.topLeft.add(this.bottomRight).scale(0.5);
	}

	public constrain(point: Point): Point {
		return new Point(
			Math.max(this.topLeft.x, Math.min(this.bottomRight.x, point.x)),
			Math.max(this.topLeft.y, Math.min(this.bottomRight.y, point.y)),
		);
	}
}

export namespace Box {
	export type AsJson = [Point.AsJson, Point.AsJson];
}
