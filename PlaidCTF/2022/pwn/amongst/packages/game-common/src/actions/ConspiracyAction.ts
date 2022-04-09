import { M, marshal, Marshaller } from "@zensors/sheriff";

export class ConspiracyAction {
	public readonly action: "exit";

	public constructor(args: ConspiracyAction.ConstructorArgs) {
		this.action = args.action;
	}

	public static fromJson(json: ConspiracyAction.AsJson) {
		return new ConspiracyAction({
			action: json.action
		});
	}

	public static fromUnknown(json: unknown): ConspiracyAction {
		marshal(json, ConspiracyAction.Marshaller);
		return ConspiracyAction.fromJson(json);
	}

	public toJson(): ConspiracyAction.AsJson {
		return {
			action: this.action
		};
	}
}

export namespace ConspiracyAction {
	export interface ConstructorArgs {
		action: "exit";
	}

	export interface AsJson {
		action: "exit";
	}

	export const Marshaller: Marshaller<AsJson> = M.obj({
		action: M.lit("exit")
	});
}
