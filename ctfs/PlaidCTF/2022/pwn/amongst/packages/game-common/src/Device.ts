import { Point, Polygon, SpatiallyHashable } from "@amongst/geometry";

export class Device implements SpatiallyHashable {
	public constructor(
		public readonly id: string,
		public readonly hitArea: Polygon,
		public readonly graphics?: Device.Graphics,
	) {}

	public static fromJson(json: Device.AsJson): Device {
		return new Device(
			json.id,
			Polygon.fromJson(json.hitArea),
			json.graphics !== undefined ? Device.Graphics.fromJson(json.graphics) : undefined
		);
	}

	public getBoundingBox() {
		return this.hitArea.getBoundingBox();
	}
}

export namespace Device {
	export interface AsJson {
		id: string;
		hitArea: Polygon.AsJson;
		graphics?: Graphics.AsJson;
	}

	export class Graphics {
		public constructor(
			public readonly type: string,
			public readonly location: Point,
			public readonly layer?: number,
			public readonly hideInDark?: boolean,
		) {}

		public static fromJson(json: Graphics.AsJson): Graphics {
			return new Graphics(
				json.type,
				Point.fromJson(json.location),
				json.layer !== undefined ? json.layer : undefined,
				json.hideInDark !== undefined ? json.hideInDark : undefined
			);
		}
	}

	export namespace Graphics {
		export interface AsJson {
			type: string;
			location: Point.AsJson;
			layer?: number;
			hideInDark?: boolean;
		}
	}
}
