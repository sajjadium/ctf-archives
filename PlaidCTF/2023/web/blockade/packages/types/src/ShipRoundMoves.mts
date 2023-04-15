import { Move } from "./Move.mjs";
import { z } from "zod";

export type ShipRoundMoves = [Move, Move, Move, Move];

export namespace ShipRoundMoves {
	export const Schema = z.tuple([Move.Schema, Move.Schema, Move.Schema, Move.Schema]);
}
