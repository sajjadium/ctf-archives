import { M, marshal, Marshaller } from "@zensors/sheriff";

export class ResetAction {
	public readonly action: "exit" | "start";

	public constructor(args: ResetAction.ConstructorArgs) {
		this.action = args.action;
	}

	public static fromJson(json: ResetAction.AsJson) {
		return new ResetAction({
			action: json.action,
		});
	}

	public static fromUnknown(json: unknown): ResetAction {
		marshal(json, ResetAction.Marshaller);
		return ResetAction.fromJson(json);
	}

	public toJson(): ResetAction.AsJson {
		return {
			action: this.action,
		};
	}
}

export namespace ResetAction {
	export interface ConstructorArgs {
		action: "exit" | "start";
	}

	export interface AsJson {
		action: "exit" | "start";
	}

	export const Marshaller: Marshaller<AsJson> = M.obj({
		action: M.union(M.lit("exit"), M.lit("start")),
	});
}
