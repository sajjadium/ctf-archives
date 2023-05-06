import { M, marshal, Marshaller } from "@zensors/sheriff";

export class EmergencyButtonAction {
	public readonly action: "exit" | "press";

	public constructor(args: EmergencyButtonAction.ConstructorArgs) {
		this.action = args.action;
	}

	public static fromJson(json: EmergencyButtonAction.AsJson) {
		return new EmergencyButtonAction({
			action: json.action,
		});
	}

	public static fromUnknown(json: unknown): EmergencyButtonAction {
		marshal(json, EmergencyButtonAction.Marshaller);
		return EmergencyButtonAction.fromJson(json);
	}

	public toJson(): EmergencyButtonAction.AsJson {
		return {
			action: this.action,
		};
	}
}

export namespace EmergencyButtonAction {
	export interface ConstructorArgs {
		action: "exit" | "press";
	}

	export interface AsJson {
		action: "exit" | "press";
	}

	export const Marshaller: Marshaller<AsJson> = M.obj({
		action: M.union(M.lit("exit"), M.lit("press")),
	});
}
