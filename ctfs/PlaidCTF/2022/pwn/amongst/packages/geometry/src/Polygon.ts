import { M, Marshaller } from "@zensors/sheriff";

import { Box } from "./Box.js";
import { Point } from "./Point.js";

export class Polygon {
	public constructor(
		public readonly points: readonly Point[]
	) {}

	public *edges(): Generator<[Point, Point]> {
		for (let i = 0; i < this.points.length; i++) {
			yield [this.points[i], this.points[(i + 1) % this.points.length]];
		}
	}

	public contains(point: Point) { // TODO: only for convex polygons bc I'm lazy
		for (let [p1, p2] of this.edges()) {
			if (p2.sub(p1).cross(point.sub(p1)) < 0) {
				return false;
			}
		}

		return true;
	}

	public scale(s: number) {
		return new Polygon(this.points.map((p) => p.scale(s)));
	}

	public translate(delta: Point) {
		return new Polygon(this.points.map((p) => p.add(delta)));
	}

	public getBoundingBox() {
		return Box.fromPoints(...this.points);
	}

	public toJson(): Polygon.AsJson {
		return this.points.map((p) => p.toJson());
	}

	public toSvg(): string {
		return this.points.map((p) => p.toSvg()).join(" ");
	}
}

export namespace Polygon {
	export type AsJson = Point.AsJson[];
	export const Marshaller: Marshaller<AsJson> = M.arr(Point.Marshaller);

	export const fromJson = (json: AsJson) => new Polygon(json.map(Point.fromJson));
}
