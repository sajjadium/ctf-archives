import { Heading } from "@puzzled/types";

export enum HalfHeading {
	North = "North",
	Northeast = "Northeast",
	East = "East",
	Southeast = "Southeast",
	South = "South",
	Southwest = "Southwest",
	West = "West",
	Northwest = "Northwest"
}

export namespace HalfHeading {
	export function fromHeading(heading: Heading) {
		switch (heading) {
			case Heading.North: return HalfHeading.North;
			case Heading.East: return HalfHeading.East;
			case Heading.South: return HalfHeading.South;
			case Heading.West: return HalfHeading.West;
			default: throw new Error(`Invalid heading: ${heading}`);
		}
	}

	export function between(a: Heading, b: Heading) {
		if (a === b) {
			return HalfHeading.fromHeading(a);
		}

		if (Heading.oppositeOf(a) === b) {
			throw new Error(`Cannot get half heading between ${a} and ${b}`);
		}

		const latitudinal = Heading.isLatitudinal(a) ? a : b;
		const longitudinal = Heading.isLongitudinal(a) ? a : b;

		if (latitudinal === Heading.North && longitudinal === Heading.East) {
			return HalfHeading.Northeast;
		} else if (latitudinal === Heading.North && longitudinal === Heading.West) {
			return HalfHeading.Northwest;
		} else if (latitudinal === Heading.South && longitudinal === Heading.East) {
			return HalfHeading.Southeast;
		} else if (latitudinal === Heading.South && longitudinal === Heading.West) {
			return HalfHeading.Southwest;
		} else {
			throw new Error(`Cannot get half heading between ${a} and ${b}`);
		}
	}
}
