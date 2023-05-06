import { DataSource } from "typeorm";

import { ShipType } from "@puzzled/types";

import { Buoy } from "./entities/Buoy.mjs";
import { Faction } from "./entities/Faction.mjs";
import { Gust } from "./entities/Gust.mjs";
import { Rock } from "./entities/Rock.mjs";
import { Ship } from "./entities/Ship.mjs";
import { ShipTypeInfo } from "./entities/ShipTypeInfo.mjs";
import { Whirlpool } from "./entities/Whirlpool.mjs";

export const dataSource = new DataSource({
	type: "postgres",
	host: process.env.PG_HOST ?? "localhost",
	port: 5432,
	username: "postgres",
	password: "postgres",
	database: "postgres",
	entities: [Buoy, Faction, Gust, Rock, Ship, ShipTypeInfo, Whirlpool],
	subscribers: [],
	migrations: []
});

const sync = dataSource.synchronize.bind(dataSource);
dataSource.synchronize = async () => {
	await sync();

	if (await dataSource.getRepository(ShipTypeInfo).count() === 0) {
		dataSource.getRepository(ShipTypeInfo).insert([
			{
				type: ShipType.Sloop,
				hull: 60,
				ramDamage: 5,
				cannonDamage: 10,
				rockDamage: 5,
				influenceRadius: 0.8,
				cannons: 4,
				carpentryRate: 6,
				sailRate: 5,
				cannonRate: 1
			},
			{
				type: ShipType.Brig,
				hull: 90,
				ramDamage: 10,
				cannonDamage: 15,
				rockDamage: 10,
				influenceRadius: 1.6,
				cannons: 8,
				carpentryRate: 8,
				sailRate: 4,
				cannonRate: 2
			},
			{
				type: ShipType.Galleon,
				hull: 120,
				ramDamage: 20,
				cannonDamage: 20,
				rockDamage: 15,
				influenceRadius: 3.2,
				cannons: 12,
				carpentryRate: 10,
				sailRate: 3,
				cannonRate: 3
			},
			{
				type: ShipType.Frigate,
				hull: 150,
				ramDamage: 20,
				cannonDamage: 20,
				rockDamage: 20,
				influenceRadius: 4.8,
				cannons: 16,
				carpentryRate: 12,
				sailRate: 3,
				cannonRate: 4
			}
		]);
	}
};
