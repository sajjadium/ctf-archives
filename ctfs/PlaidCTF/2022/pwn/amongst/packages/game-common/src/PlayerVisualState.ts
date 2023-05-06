import { Direction } from "./Direction.js";

export type PlayerVisualState =
	| PlayerVisualState.Idle
	| PlayerVisualState.Moving
	;

export namespace PlayerVisualState {
	export enum Kind {
		Idle = "Idle",
		Moving = "Moving",
	}

	export interface Idle {
		kind: Kind.Idle;
		direction: Direction;
	}

	export interface Moving {
		kind: Kind.Moving;
		direction: Direction;
		frame: number;
	}
}
