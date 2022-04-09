import { Color } from "@amongst/game-common";
import { Point } from "@amongst/geometry";

export class Body {
	public constructor(
		public readonly id: string,
		public readonly color: Color,
		public readonly location: Point
	) {}
}
