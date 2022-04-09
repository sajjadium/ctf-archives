import { M, marshal, Marshaller } from "@zensors/sheriff";

export class ProcessSampleAction {
	public readonly action: "exit" | "begin" | "end";

	public constructor(args: ProcessSampleAction.ConstructorArgs) {
		this.action = args.action;
	}

	public static fromJson(json: ProcessSampleAction.AsJson) {
		return new ProcessSampleAction({
			action: json.action
		});
	}

	public static fromUnknown(json: unknown): ProcessSampleAction {
		marshal(json, ProcessSampleAction.Marshaller);
		return ProcessSampleAction.fromJson(json);
	}

	public toJson(): ProcessSampleAction.AsJson {
		return {
			action: this.action
		};
	}
}

export namespace ProcessSampleAction {
	export interface ConstructorArgs {
		action: "exit" | "begin" | "end";
	}

	export interface AsJson {
		action: "exit" | "begin" | "end";
	}

	export const Marshaller: Marshaller<AsJson> = M.obj({
		action: M.union(M.lit("exit"), M.lit("begin"), M.lit("end"))
	});
}
