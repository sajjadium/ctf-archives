import { Point } from "@amongst/geometry";

export class MapGraphics {
	public constructor(
		public readonly id: string,
		public readonly origin: Point,
		public readonly scale: number,
		public readonly visibility: number
	) {}

	public static fromJson(json: MapGraphics.AsJson): MapGraphics {
		return new MapGraphics(
			json.id,
			Point.fromJson(json.origin),
			json.scale,
			json.visibility
		);
	}
}

export namespace MapGraphics {
	export interface AsJson {
		id: string;
		origin: Point.AsJson;
		scale: number;
		visibility: number;
	}
}
