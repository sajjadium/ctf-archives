import { M, marshal, Marshaller } from "@zensors/sheriff";

export class SatelliteAction {
	public readonly action: "exit";

	public constructor(args: SatelliteAction.ConstructorArgs) {
		this.action = args.action;
	}

	public static fromJson(json: SatelliteAction.AsJson) {
		return new SatelliteAction({
			action: json.action
		});
	}

	public static fromUnknown(json: unknown): SatelliteAction {
		marshal(json, SatelliteAction.Marshaller);
		return SatelliteAction.fromJson(json);
	}

	public toJson(): SatelliteAction.AsJson {
		return {
			action: this.action
		};
	}
}

export namespace SatelliteAction {
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
