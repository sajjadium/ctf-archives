import { Heading } from "./Heading.mjs";
import { Point } from "./Point.mjs";

export interface MoveOutcome {
	controlledMove: MovementPhaseResult;
	uncontrolledMove: MovementPhaseResult;
	fire: FirePhaseResult;
}

export namespace MoveOutcome {
	export interface AsJson {
		controlledMove: MovementPhaseResult.AsJson;
		uncontrolledMove: MovementPhaseResult.AsJson;
		fire: FirePhaseResult.AsJson;
	}

	export function fromJson(json: AsJson): MoveOutcome {
		return {
			controlledMove: MovementPhaseResult.fromJson(json.controlledMove),
			uncontrolledMove: MovementPhaseResult.fromJson(json.uncontrolledMove),
			fire: FirePhaseResult.fromJson(json.fire)
		};
	}

	export function toJson(moveOutcome: MoveOutcome): AsJson {
		return {
			controlledMove: MovementPhaseResult.toJson(moveOutcome.controlledMove),
			uncontrolledMove: MovementPhaseResult.toJson(moveOutcome.uncontrolledMove),
			fire: FirePhaseResult.toJson(moveOutcome.fire)
		};
	}
}

export interface MovementPhaseResult {
	intent: {
		location: Point;
		heading: Heading;
	};
	result: {
		location: Point;
		heading: Heading;
	};
}

export namespace MovementPhaseResult {
	export interface AsJson {
		intent: {
			location: Point.AsJson;
			heading: Heading;
		};
		result: {
			location: Point.AsJson;
			heading: Heading;
		};
	}

	export function fromJson(json: AsJson): MovementPhaseResult {
		return {
			intent: {
				location: Point.fromJson(json.intent.location),
				heading: json.intent.heading
			},
			result: {
				location: Point.fromJson(json.result.location),
				heading: json.result.heading
			}
		};
	}

	export function toJson(movementPhaseResult: MovementPhaseResult): AsJson {
		return {
			intent: {
				location: movementPhaseResult.intent.location.toJson(),
				heading: movementPhaseResult.intent.heading
			},
			result: {
				location: movementPhaseResult.result.location.toJson(),
				heading: movementPhaseResult.result.heading
			}
		};
	}
}

export interface FirePhaseResult {
	left?: FireResult;
	right?: FireResult;
}

export namespace FirePhaseResult {
	export interface AsJson {
		left?: FireResult.AsJson;
		right?: FireResult.AsJson;
	}

	export function fromJson(json: AsJson): FirePhaseResult {
		return {
			left: json.left ? FireResult.fromJson(json.left) : undefined,
			right: json.right ? FireResult.fromJson(json.right) : undefined
		};
	}

	export function toJson(firePhaseResult: FirePhaseResult): AsJson {
		return {
			left: firePhaseResult.left ? FireResult.toJson(firePhaseResult.left) : undefined,
			right: firePhaseResult.right ? FireResult.toJson(firePhaseResult.right) : undefined
		};
	}
}

export type FireResult = { kind: "miss" } | { kind: "hit", location: Point };

export namespace FireResult {
	export type AsJson = { kind: "miss" } | { kind: "hit", location: Point.AsJson };

	export function fromJson(json: AsJson): FireResult {
		return json.kind === "miss" ? { kind: "miss" } : { kind: "hit", location: Point.fromJson(json.location) };
	}

	export function toJson(fireResult: FireResult): AsJson {
		return fireResult.kind === "miss" ? { kind: "miss" } : { kind: "hit", location: fireResult.location.toJson() };
	}
}
