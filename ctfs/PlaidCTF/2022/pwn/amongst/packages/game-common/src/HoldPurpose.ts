export type HoldPurpose =
	| HoldPurpose.GameStart
	| HoldPurpose.VoteComplete
	| HoldPurpose.MeetingStart
	| HoldPurpose.GameEnd
	;

export namespace HoldPurpose {
	export enum Kind {
		GameStart = "GameStart",
		MeetingStart = "MeetingStart",
		VoteComplete = "VoteComplete",
		GameEnd = "GameEnd",
	}

	export class GameStart {
		public readonly kind = Kind.GameStart;

		public constructor(
			public readonly hoaxers: number
		) {}

		public static fromJson(json: GameStart.AsJson): GameStart {
			return new GameStart(json.hoaxers);
		}

		public toJson(): GameStart.AsJson {
			return {
				kind: this.kind,
				hoaxers: this.hoaxers,
			};
		}
	}

	export namespace GameStart {
		export interface AsJson {
			kind: Kind.GameStart;
			hoaxers: number;
		}
	}

	export class MeetingStart {
		public readonly kind = Kind.MeetingStart;

		public constructor() {}

		public static fromJson(_json: MeetingStart.AsJson): MeetingStart {
			return new MeetingStart();
		}

		public toJson(): MeetingStart.AsJson {
			return {
				kind: this.kind,
			};
		}
	}

	export namespace MeetingStart {
		export interface AsJson {
			kind: Kind.MeetingStart;
		}
	}

	export class VoteComplete {
		public readonly kind = Kind.VoteComplete;

		public constructor(
			public readonly outcome: VoteComplete.Outcome
		) {}

		public static fromJson(json: VoteComplete.AsJson): VoteComplete {
			return new VoteComplete(json.outcome);
		}

		public toJson(): VoteComplete.AsJson {
			return {
				kind: this.kind,
				outcome: this.outcome,
			};
		}
	}

	export namespace VoteComplete {
		export type Outcome =
		| { kind: "skipped" }
		| { kind: "tie" }
		| { kind: "ejected"; player: string; hoaxer: boolean }
		;

		export interface AsJson {
			kind: Kind.VoteComplete;
			outcome: Outcome;
		}
	}

	export class GameEnd {
		public readonly kind = Kind.GameEnd;

		public constructor(
			public readonly shipmatesWin: boolean
		) {}

		public static fromJson(json: GameEnd.AsJson): GameEnd {
			return new GameEnd(json.shipmatesWin);
		}

		public toJson(): GameEnd.AsJson {
			return {
				kind: this.kind,
				shipmatesWin: this.shipmatesWin,
			};
		}
	}

	export namespace GameEnd {
		export interface AsJson {
			kind: Kind.GameEnd;
			shipmatesWin: boolean;
		}
	}

	export type AsJson =
		| GameStart.AsJson
		| MeetingStart.AsJson
		| VoteComplete.AsJson
		| GameEnd.AsJson
		;

	export function fromJson(json: AsJson): HoldPurpose {
		switch (json.kind) {
			case Kind.GameStart: return GameStart.fromJson(json);
			case Kind.MeetingStart: return MeetingStart.fromJson(json);
			case Kind.VoteComplete: return VoteComplete.fromJson(json);
			case Kind.GameEnd: return GameEnd.fromJson(json);
		}
	}
}
