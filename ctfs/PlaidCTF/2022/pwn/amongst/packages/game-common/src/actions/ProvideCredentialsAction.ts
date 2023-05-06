import { M, marshal, Marshaller } from "@zensors/sheriff";

export class ProvideCredentialsAction {
	public readonly exit: boolean;
	public readonly username: string;
	public readonly password: string;

	public constructor(args: ProvideCredentialsAction.ConstructorArgs) {
		this.exit = args.exit;
		this.username = args.username;
		this.password = args.password;
	}

	public static fromJson(json: ProvideCredentialsAction.AsJson) {
		return new ProvideCredentialsAction({
			exit: json.exit,
			username: json.username,
			password: json.password,
		});
	}

	public static fromUnknown(json: unknown): ProvideCredentialsAction {
		marshal(json, ProvideCredentialsAction.Marshaller);
		return ProvideCredentialsAction.fromJson(json);
	}

	public toJson(): ProvideCredentialsAction.AsJson {
		return {
			exit: this.exit,
			username: this.username,
			password: this.password,
		};
	}
}

export namespace ProvideCredentialsAction {
	export interface ConstructorArgs {
		exit: boolean;
		username: string;
		password: string;
	}

	export interface AsJson {
		exit: boolean;
		username: string;
		password: string;
	}

	export const Marshaller: Marshaller<AsJson> = M.obj({
		exit: M.bool,
		username: M.str,
		password: M.str,
	});
}
