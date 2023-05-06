import { List } from "immutable";
import { TurnOutcome } from "./TurnOutcome.mjs";

export type RoundOutcome = List<TurnOutcome>;

export namespace RoundOutcome {
	export type AsJson = TurnOutcome.AsJson[];

	export function fromJson(json: AsJson): RoundOutcome {
		return List(json.map(TurnOutcome.fromJson));
	}

	export function toJson(roundOutcome: RoundOutcome): AsJson {
		return roundOutcome.toArray().map(TurnOutcome.toJson);
	}
}
