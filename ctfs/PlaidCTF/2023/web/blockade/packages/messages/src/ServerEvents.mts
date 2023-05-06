import { BoardInfo, GameState, RoundOutcome, ShipRoundMoves } from "@puzzled/types";

export interface ServerEvents {
	board: (board: BoardInfo.AsJson) => void;
	round: (outcome: RoundOutcome.AsJson) => void;
	state: (state: GameState.AsJson) => void;
	movesUpdated: (args: MovesUpdatedArgs) => void;
	flag: (flag: string) => void;
}

export interface MovesUpdatedArgs {
	id: number;
	moves: ShipRoundMoves;
}
