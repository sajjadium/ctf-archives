import { MoveOutcome } from "./MoveOutcome.mjs";
import { List, Map } from "immutable";

export interface TurnOutcome {
	shipMoves: Map<number, MoveOutcome>;
	sunk: List<number>;
}

export namespace TurnOutcome {
	export interface AsJson {
		shipMoves: {
			id: number;
			moveOutcome: MoveOutcome.AsJson;
		}[];
		sunk: number[];
	}

	export function fromJson(json: AsJson): TurnOutcome {
		return {
			shipMoves: Map<number, MoveOutcome>(
				json.shipMoves.map((shipMove) => [
					shipMove.id,
					MoveOutcome.fromJson(shipMove.moveOutcome)
				])
			),
			sunk: List<number>(json.sunk)
		};
	}

	export function toJson(turnOutcome: TurnOutcome): AsJson {
		return {
			shipMoves: turnOutcome.shipMoves
				.toArray()
				.map(([id, moveOutcome]) => ({
					id,
					moveOutcome: MoveOutcome.toJson(moveOutcome)
				})),
			sunk: turnOutcome.sunk.toArray()
		};
	}
}
