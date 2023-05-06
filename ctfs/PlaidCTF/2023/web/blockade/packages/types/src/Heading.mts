import { Point } from "./Point.mjs";

export enum Heading {
	North = "North",
	East = "East",
	South = "South",
	West = "West",
}

export namespace Heading {
	export function leftOf(heading: Heading): Heading {
		switch (heading) {
			case Heading.North: return Heading.West;
			case Heading.East: return Heading.North;
			case Heading.South: return Heading.East;
			case Heading.West: return Heading.South;
			default: throw new Error(`Invalid heading: ${heading}`);
		}
	}

	export function rightOf(heading: Heading): Heading {
		switch (heading) {
			case Heading.North: return Heading.East;
			case Heading.East: return Heading.South;
			case Heading.South: return Heading.West;
			case Heading.West: return Heading.North;
			default: throw new Error(`Invalid heading: ${heading}`);
		}
	}

	export function oppositeOf(heading: Heading): Heading {
		switch (heading) {
			case Heading.North: return Heading.South;
			case Heading.East: return Heading.West;
			case Heading.South: return Heading.North;
			case Heading.West: return Heading.East;
			default: throw new Error(`Invalid heading: ${heading}`);
		}
	}

	export function toPoint(heading: Heading): Point {
		switch (heading) {
			case Heading.North: return new Point(0, -1);
			case Heading.East: return new Point(1, 0);
			case Heading.South: return new Point(0, 1);
			case Heading.West: return new Point(-1, 0);
			default: throw new Error(`Invalid heading: ${heading}`);
		}
	}

	export function isLatitudinal(heading: Heading): boolean {
		switch (heading) {
			case Heading.North: return true;
			case Heading.East: return false;
			case Heading.South: return true;
			case Heading.West: return false;
			default: throw new Error(`Invalid heading: ${heading}`);
		}
	}

	export function isLongitudinal(heading: Heading): boolean {
		switch (heading) {
			case Heading.North: return false;
			case Heading.East: return true;
			case Heading.South: return false;
			case Heading.West: return true;
			default: throw new Error(`Invalid heading: ${heading}`);
		}
	}
}
