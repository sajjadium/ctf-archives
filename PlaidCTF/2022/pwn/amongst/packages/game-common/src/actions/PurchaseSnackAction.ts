import { M, marshal, Marshaller } from "@zensors/sheriff";

export class PurchaseSnackAction {
	public readonly exit: boolean;
	public readonly selection: string;

	public constructor(args: PurchaseSnackAction.ConstructorArgs) {
		this.exit = args.exit;
		this.selection = args.selection;
	}

	public static fromJson(json: PurchaseSnackAction.AsJson) {
		return new PurchaseSnackAction({
			exit: json.exit,
			selection: json.selection,
		});
	}

	public static fromUnknown(json: unknown): PurchaseSnackAction {
		marshal(json, PurchaseSnackAction.Marshaller);
		return PurchaseSnackAction.fromJson(json);
	}

	public toJson(): PurchaseSnackAction.AsJson {
		return {
			exit: this.exit,
			selection: this.selection,
		};
	}
}

export namespace PurchaseSnackAction {
	export interface ConstructorArgs {
		exit: boolean;
		selection: string;
	}

	export interface AsJson {
		exit: boolean;
		selection: string;
	}

	export const Marshaller: Marshaller<AsJson> = M.obj({
		exit: M.bool,
		selection: M.str,
	});
}
