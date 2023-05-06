import { List, Map } from "immutable";

import { Move, MoveOutcome, TurnOutcome } from "@puzzled/types";

import { dataSource } from "../dataSource.mjs";
import { Ship } from "../entities/Ship.mjs";
import { asyncBindMap } from "../utils/asyncBindMap.mjs";
import { executeMove } from "./executeMove.mjs";

export async function executeTurn(factionId: number, moves: Map<number, Move>): Promise<TurnOutcome> {
	let moveOutcomes: Map<number, MoveOutcome>;

	try {
		moveOutcomes = await dataSource.transaction(async (tx) => {
			const ships = await tx.findBy(Ship, { factionId, sunk: false });
			const shipsMap = Map(ships.map((ship) => [ship.id, ship]));
			const shipsWithMoves = shipsMap.map((ship): [Ship, Move] => [ship, moves.get(ship.id) ?? {}]);
			return await asyncBindMap(shipsWithMoves, async ([ship, move]) => (
				executeMove(tx, ship, move)
			));
		});
	} catch (e) {
		// player attempted something invalid, replace all of their moves with empty moves
		moveOutcomes = await dataSource.transaction(async (tx) => {
			const ships = await tx.findBy(Ship, { factionId, sunk: false });
			const shipsMap = Map(ships.map((ship) => [ship.id, ship]));
			return await asyncBindMap(shipsMap, async (ship) => (
				executeMove(tx, ship, {})
			));
		});
	}

	const allShips = await dataSource.getRepository(Ship).findBy({ sunk: false });
	let sunk = List<number>();

	for (const ship of allShips) {
		if (ship.damage >= ship.typeInfo.hull) {
			ship.damage = ship.typeInfo.hull;
			ship.sunk = true;
			sunk = sunk.push(ship.id);
		}
	}

	await dataSource.getRepository(Ship).save(allShips);
	return {
		shipMoves: moveOutcomes,
		sunk
	};
}
