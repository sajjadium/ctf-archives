import { GameState } from "@puzzled/types";

import { dataSource } from "./dataSource.mjs";
import { Faction } from "./entities/Faction.mjs";
import { Ship } from "./entities/Ship.mjs";

export async function getState(round: number, readerFactionId: number): Promise<GameState> {
	const [factions, ships] = await Promise.all([
		dataSource.getRepository(Faction).find({ order: { id: "ASC" }}),
		dataSource.getRepository(Ship).find({ order: { id: "ASC" }})
	]);

	return {
		round,
		factions: factions.map((faction) => ({
			id: faction.id,
			name: faction.name,
			score: faction.score
		})),
		ships: ships.map((ship) => {
			const commonInfo = {
				id: ship.id,
				name: ship.name,
				faction: ship.factionId,
				location: ship.location,
				heading: ship.heading,
				type: ship.type,
				sunk: ship.sunk
			};

			if (ship.factionId !== readerFactionId) {
				return commonInfo;
			}

			return {
				...commonInfo,
				damage: ship.damage,
				forwardTokens: ship.forwardTokens,
				leftTokens: ship.leftTokens,
				rightTokens: ship.rightTokens,
				loadedCannons: ship.loadedCannons,
				cannonballs: ship.cannonballs
			};
		})
	};
}