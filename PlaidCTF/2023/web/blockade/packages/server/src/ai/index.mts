import { Map } from "immutable";

import { FactionRoundMoves, GameState } from "@puzzled/types";

import { Faction } from "../entities/Faction.mjs";

export class AI {
	constructor(private faction: Faction) {}

	public getMoves(state: GameState): FactionRoundMoves {
		return Map(
			state.ships
				.filter((ship) => ship.faction === this.faction.id)
				.map((ship) => [
					ship.id,
					[
						{ fire: { left: true, right: true } },
						{ fire: { left: true, right: true } },
						{ fire: { left: true, right: true } },
						{ fire: { left: true, right: true } }
					]
				])
		);
	}
}
