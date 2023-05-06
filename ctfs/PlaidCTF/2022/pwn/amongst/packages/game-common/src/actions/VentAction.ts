import { M, marshal, Marshaller } from "@zensors/sheriff";

export class VentAction {
	public readonly target: string;
	public readonly exit?: boolean;

	public constructor(args: VentAction.ConstructorArgs) {
		this.target = args.target;
		this.exit = args.exit;
	}

	public static fromJson(json: VentAction.AsJson) {
		return new VentAction({
			target: json.target,
			exit: json.exit,
		});
	}

	public static fromUnknown(json: unknown): VentAction {
		marshal(json, VentAction.Marshaller);
		return VentAction.fromJson(json);
	}

	public toJson(): VentAction.AsJson {
		return {
			target: this.target,
			exit: this.exit,
		};
	}
}

export namespace VentAction {
	export interface ConstructorArgs {
		target: string;
		exit?: boolean;
	}

	export interface AsJson {
		target: string;
		exit?: boolean;
	}

	export const Marshaller: Marshaller<AsJson> = M.obj({
		target: M.str,
		exit: M.opt(M.bool),
	});
}
