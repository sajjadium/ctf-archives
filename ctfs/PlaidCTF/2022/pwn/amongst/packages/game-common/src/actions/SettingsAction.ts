import { M, marshal, Marshaller } from "@zensors/sheriff";

import { Color } from "../Color.js";

export class SettingsAction {
	public readonly exit?: boolean;
	public readonly color?: Color;
	public readonly name?: string;

	public constructor(args: SettingsAction.ConstructorArgs) {
		this.exit = args.exit;
		this.color = args.color;
		this.name = args.name;
	}

	public static fromJson(json: SettingsAction.AsJson) {
		return new SettingsAction({
			exit: json.exit,
			color: json.color,
			name: json.name,
		});
	}

	public static fromUnknown(json: unknown): SettingsAction {
		marshal(json, SettingsAction.Marshaller);
		return SettingsAction.fromJson(json);
	}

	public toJson(): SettingsAction.AsJson {
		return {
			exit: this.exit,
			color: this.color,
			name: this.name,
		};
	}
}

export namespace SettingsAction {
	export interface ConstructorArgs {
		exit?: boolean;
		color?: Color;
		name?: string;
	}

	export interface AsJson {
		exit?: boolean;
		color?: Color;
		name?: string;
	}

	export const Marshaller: Marshaller<AsJson> = M.obj({
		exit: M.opt(M.bool),
		color: M.opt(Color.Marshaller),
		name: M.opt(M.str),
	});
}
