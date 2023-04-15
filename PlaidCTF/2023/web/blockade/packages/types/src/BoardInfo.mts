import { Heading } from "./Heading.mjs";
import { Point } from "./Point.mjs";

export interface BoardInfo {
	size: Point;
	rocks: {
		location: Point;
	}[];
	gusts: {
		location: Point;
		heading: Heading;
	}[];
	whirlpools: {
		location: Point;
		clockwise: boolean;
	}[];
	buoys: {
		location: Point;
		value: number;
	}[];
}

export namespace BoardInfo {
	export interface AsJson {
		size: Point.AsJson;
		rocks: {
			location: Point.AsJson;
		}[];
		gusts: {
			location: Point.AsJson;
			heading: Heading;
		}[];
		whirlpools: {
			location: Point.AsJson;
			clockwise: boolean;
		}[];
		buoys: {
			location: Point.AsJson;
			value: number;
		}[];
	}

	export function fromJson(json: AsJson): BoardInfo {
		return {
			size: Point.fromJson(json.size),
			rocks: json.rocks.map((rock) => ({
				location: Point.fromJson(rock.location)
			})),
			gusts: json.gusts.map((gust) => ({
				location: Point.fromJson(gust.location),
				heading: gust.heading
			})),
			whirlpools: json.whirlpools.map((whirlpool) => ({
				location: Point.fromJson(whirlpool.location),
				clockwise: whirlpool.clockwise
			})),
			buoys: json.buoys.map((buoy) => ({
				location: Point.fromJson(buoy.location),
				value: buoy.value
			}))
		};
	}

	export function toJson(board: BoardInfo): AsJson {
		return {
			size: board.size.toJson(),
			rocks: board.rocks.map((rock) => ({
				location: rock.location.toJson()
			})),
			gusts: board.gusts.map((gust) => ({
				location: gust.location.toJson(),
				heading: gust.heading
			})),
			whirlpools: board.whirlpools.map((whirlpool) => ({
				location: whirlpool.location.toJson(),
				clockwise: whirlpool.clockwise
			})),
			buoys: board.buoys.map((buoy) => ({
				location: buoy.location.toJson(),
				value: buoy.value
			}))
		};
	}
}
