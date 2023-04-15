import { z } from "zod";

import { ShipRoundMoves } from "@puzzled/types";

export interface ClientEvents {
	start: () => void;
	setMoves: (args: SetMovesArgs) => void;
	advanceRound: (args: AdvanceRoundArgs) => void;
}

export interface SetMovesArgs {
	id: number;
	moves: ShipRoundMoves;
}

export namespace SetMovesArgs {
	export const Schema = z.object({
		id: z.number(),
		moves: ShipRoundMoves.Schema
	});
}

export interface AdvanceRoundArgs {
	round: number;
}

export namespace AdvanceRoundArgs {
	export const Schema = z.object({
		round: z.number()
	});
}
