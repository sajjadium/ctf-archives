import { Heading } from "./Heading.mjs";
import { Point } from "./Point.mjs";
import { ShipType } from "./ShipType.mjs";

export interface GameState {
	round: number;
	factions: FactionState[];
	ships: ShipState[];
}

export namespace GameState {
	export interface AsJson {
		round: number;
		factions: FactionState[];
		ships: ShipState.AsJson[];
	}

	export function fromJson(json: AsJson): GameState {
		return {
			round: json.round,
			factions: json.factions,
			ships: json.ships.map(ShipState.fromJson)
		};
	}

	export function toJson(game: GameState): AsJson {
		return {
			round: game.round,
			factions: game.factions,
			ships: game.ships.map(ShipState.toJson)
		};
	}

	export function clone(game: GameState): GameState {
		return {
			round: game.round,
			factions: game.factions.map((faction) => FactionState.clone(faction)),
			ships: game.ships.map((ship) => ShipState.clone(ship))
		};
	}
}

export interface FactionState {
	id: number;
	name: string;
	score: number;
}

export namespace FactionState {
	export function clone(faction: FactionState): FactionState {
		return { ...faction };
	}
}

export interface ShipState {
	id: number;
	name: string;
	faction: number;
	type: ShipType;
	location: Point;
	heading: Heading;
	damage?: number;
	forwardTokens?: number;
	leftTokens?: number;
	rightTokens?: number;
	loadedCannons?: number;
	cannonballs?: number;
	sunk: boolean;
}

export namespace ShipState {
	export interface AsJson extends Omit<ShipState, "location"> {
		location: Point.AsJson;
	}

	export function fromJson(json: AsJson): ShipState {
		return {
			...json,
			location: Point.fromJson(json.location)
		};
	}

	export function toJson(ship: ShipState): AsJson {
		return {
			...ship,
			location: ship.location.toJson()
		};
	}

	export function clone(ship: ShipState): ShipState {
		return {
			...ship,
			location: ship.location.clone()
		};
	}
}
