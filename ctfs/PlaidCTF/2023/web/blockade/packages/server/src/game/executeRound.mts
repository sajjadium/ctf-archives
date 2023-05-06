import { List, Map } from "immutable";

import { FactionRoundMoves, RoundOutcome, TurnOutcome } from "@puzzled/types";

import { dataSource } from "../dataSource.mjs";
import { Ship } from "../entities/Ship.mjs";
import { executeTurn } from "./executeTurn.mjs";

export async function executeRound(
	moves: Map<number, FactionRoundMoves>,
	factionOrder: number[]
): Promise<RoundOutcome> {
	let turnOutcomes = List<TurnOutcome>();

	for (let i = 0; i < 4; i++) {
		for (const factionId of factionOrder) {
			const factionTurnMoves = moves.get(factionId) ?? Map();

			turnOutcomes = turnOutcomes.push(await executeTurn(factionId, factionTurnMoves.map((moves) => moves[i])));
		}
	}

	const allShips = await dataSource.getRepository(Ship).findBy({ sunk: false });

	for (const ship of allShips) {
		ship.damage = Math.max(ship.damage - ship.typeInfo.carpentryRate, 0);

		for (let i = 0; i < ship.typeInfo.sailRate; i++) {
			const weights = [
				ship.forwardTokens < 4 ? 2 : 0,
				ship.leftTokens < 4 ? 1 : 0,
				ship.rightTokens < 4 ? 1 : 0
			];

			const totalWeight = weights.reduce((a, b) => a + b, 0);

			if (totalWeight === 0) {
				break;
			}

			const random = Math.random() * totalWeight;

			if (random < weights[0]) {
				ship.forwardTokens++;
			} else if (random < weights[0] + weights[1]) {
				ship.leftTokens++;
			} else {
				ship.rightTokens++;
			}
		}

		const cannonsToAdd = Math.max(
			Math.min(
				ship.typeInfo.cannons - ship.loadedCannons,
				ship.typeInfo.cannonRate,
				ship.cannonballs
			),
			0
		);

		ship.loadedCannons += cannonsToAdd;
		ship.cannonballs -= cannonsToAdd;
	}

	await dataSource.getRepository(Ship).save(allShips);
	return turnOutcomes;
}
