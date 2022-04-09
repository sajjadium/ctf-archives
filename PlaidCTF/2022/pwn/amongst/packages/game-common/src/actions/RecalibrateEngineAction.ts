import { M, marshal, Marshaller } from "@zensors/sheriff";

export class RecalibrateEngineAction {
	public readonly button: number;

	public constructor(args: RecalibrateEngineAction.ConstructorArgs) {
		this.button = args.button;
	}

	public static fromJson(json: RecalibrateEngineAction.AsJson) {
		return new RecalibrateEngineAction({
			button: json.button,
		});
	}

	public static fromUnknown(json: unknown): RecalibrateEngineAction {
		marshal(json, RecalibrateEngineAction.Marshaller);
		return RecalibrateEngineAction.fromJson(json);
	}

	public toJson(): RecalibrateEngineAction.AsJson {
		return {
			button: this.button,
		};
	}
}

export namespace RecalibrateEngineAction {
	export interface ConstructorArgs {
		button: number;
	}

	export interface AsJson {
		button: number;
	}

	export const Marshaller: Marshaller<AsJson> = M.obj({
		button: M.num,
	});
}
