import { Heading, Point, ShipType } from "@puzzled/types";

import { dataSource } from "../src/dataSource.mjs";
import { Buoy } from "../src/entities/Buoy.mjs";
import { Faction } from "../src/entities/Faction.mjs";
import { Gust } from "../src/entities/Gust.mjs";
import { Rock } from "../src/entities/Rock.mjs";
import { Ship } from "../src/entities/Ship.mjs";
import { Whirlpool } from "../src/entities/Whirlpool.mjs";

export async function createFaction(
	options: {
		name: string,
		score?: number
	}
) {
	const faction = dataSource.getRepository(Faction).create({
		name: options.name,
		score: options.score ?? 0
	});

	return await dataSource.getRepository(Faction).save(faction);
}

export async function createShip(
	options: {
		faction: Faction,
		name?: string,
		location?: Point,
		heading?: Heading,
		type?: ShipType,
		damage?: number,
		forwardTokens?: number,
		leftTokens?: number,
		rightTokens?: number,
		loadedCannons?: number,
		cannonballs?: number,
		sunk?: boolean
	}
) {
	const ship = dataSource.getRepository(Ship).create({
		faction: options.faction,
		location: options.location ?? Point.Origin,
		heading : options.heading ?? Heading.East,
		name: options.name ?? "Test Ship",
		type: options.type ?? ShipType.Brig,
		damage: options.damage ?? 0,
		forwardTokens: options.forwardTokens ?? 1,
		leftTokens: options.leftTokens ?? 1,
		rightTokens: options.rightTokens ?? 1,
		loadedCannons: options.loadedCannons ?? 1,
		cannonballs: options.cannonballs ?? 1,
		sunk: options.sunk ?? false
	});

	await dataSource.getRepository(Ship).save(ship);
	return await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
}

export async function createRock(location: Point) {
	const rock = dataSource.getRepository(Rock).create({
		location
	});

	return await dataSource.getRepository(Rock).save(rock);
}

export async function createGust(location: Point, heading: Heading) {
	const gust = dataSource.getRepository(Gust).create({
		location,
		heading
	});

	return await dataSource.getRepository(Gust).save(gust);
}

export async function createWhirlpool(location: Point, clockwise: boolean) {
	if (location.x - Math.floor(location.x) !== 0.5 || location.y - Math.floor(location.y) !== 0.5) {
		throw new Error("Whirlpool location must be at the corner of four tiles");
	}

	const whirlpool = dataSource.getRepository(Whirlpool).create({
		location,
		clockwise
	});

	return await dataSource.getRepository(Whirlpool).save(whirlpool);
}

export async function createBuoy(location: Point, value = 1) {
	const buoy = dataSource.getRepository(Buoy).create({
		location,
		value
	});

	return await dataSource.getRepository(Buoy).save(buoy);
}
