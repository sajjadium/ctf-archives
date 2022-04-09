import { M, marshal, Marshaller } from "@zensors/sheriff";

import { Point } from "@amongst/geometry";

export class MoveAction {
	public readonly delta: Point;
	public readonly bonusAction?: MoveAction.BonusAction;

	public constructor(args: MoveAction.ConstructorArgs) {
		this.delta = args.delta;
		this.bonusAction = args.bonusAction;
	}

	public static fromJson(json: MoveAction.AsJson) {
		return new MoveAction({
			delta: Point.fromJson(json.delta),
			bonusAction: json.bonusAction === undefined ? undefined : MoveAction.BonusAction.fromJson(json.bonusAction),
		});
	}

	public static fromUnknown(json: unknown): MoveAction {
		marshal(json, MoveAction.Marshaller);
		return MoveAction.fromJson(json);
	}

	public toJson(): MoveAction.AsJson {
		return {
			delta: this.delta.toJson(),
			bonusAction: this.bonusAction?.toJson()
		};
	}
}

export namespace MoveAction {
	export interface ConstructorArgs {
		delta: Point;
		bonusAction?: BonusAction;
	}

	export interface AsJson {
		delta: Point.AsJson;
		bonusAction?: BonusAction.AsJson;
	}

	export type BonusAction =
		| BonusAction.Kill
		| BonusAction.Interact
		| BonusAction.Report
		;

	export namespace BonusAction {
		export enum Kind {
			Kill = "Kill",
			Interact = "Interact",
			Report = "Report",
		}

		export class Kill {
			public readonly kind = Kind.Kill;
			public readonly target: string;
			public readonly at: Point;

			public constructor(args: Kill.ConstructorArgs) {
				this.target = args.target;
				this.at = args.at;
			}

			public static fromJson(json: Kill.AsJson) {
				return new Kill({
					target: json.target,
					at: Point.fromJson(json.at),
				});
			}

			public toJson(): Kill.AsJson {
				return {
					kind: Kind.Kill,
					target: this.target,
					at: this.at.toJson(),
				};
			}
		}

		export namespace Kill {
			export interface ConstructorArgs {
				target: string;
				at: Point;
			}

			export interface AsJson {
				kind: Kind.Kill;
				target: string;
				at: Point.AsJson;
			}

			export const Marshaller: Marshaller<AsJson> = M.obj({
				kind: M.lit(Kind.Kill),
				target: M.str,
				at: Point.Marshaller,
			});
		}

		export class Interact {
			public readonly kind = Kind.Interact;
			public readonly system: number;
			public readonly device: string;

			public constructor(args: Interact.ConstructorArgs) {
				this.system = args.system;
				this.device = args.device;
			}

			public static fromJson(json: Interact.AsJson) {
				return new Interact({
					system: json.system,
					device: json.device,
				});
			}

			public toJson(): Interact.AsJson {
				return {
					kind: Kind.Interact,
					system: this.system,
					device: this.device,
				};
			}
		}

		export namespace Interact {
			export interface ConstructorArgs {
				system: number;
				device: string;
			}

			export interface AsJson {
				kind: Kind.Interact;
				system: number;
				device: string;
			}

			export const Marshaller: Marshaller<AsJson> = M.obj({
				kind: M.lit(Kind.Interact),
				system: M.num,
				device: M.str,
			});
		}

		export class Report {
			public readonly kind = Kind.Report;
			public readonly body: string;

			public constructor(args: Report.ConstructorArgs) {
				this.body = args.body;
			}

			public static fromJson(json: Report.AsJson) {
				return new Report({
					body: json.body,
				});
			}

			public toJson(): Report.AsJson {
				return {
					kind: Kind.Report,
					body: this.body,
				};
			}
		}

		export namespace Report {
			export interface ConstructorArgs {
				body: string;
			}

			export interface AsJson {
				kind: Kind.Report;
				body: string;
			}

			export const Marshaller: Marshaller<AsJson> = M.obj({
				kind: M.lit(Kind.Report),
				body: M.str,
			});
		}

		export type AsJson =
			| Kill.AsJson
			| Interact.AsJson
			| Report.AsJson
			;

		export const Marshaller: Marshaller<AsJson> = M.union(
			Kill.Marshaller,
			Interact.Marshaller,
			Report.Marshaller,
		);

		export function fromJson(json: AsJson): BonusAction {
			switch (json.kind) {
				case Kind.Kill: return Kill.fromJson(json);
				case Kind.Interact: return Interact.fromJson(json);
				case Kind.Report: return Report.fromJson(json);
			}
		}
	}

	export const Marshaller: Marshaller<AsJson> = M.obj({
		delta: Point.Marshaller,
		bonusAction: M.opt(BonusAction.Marshaller),
	});
}
