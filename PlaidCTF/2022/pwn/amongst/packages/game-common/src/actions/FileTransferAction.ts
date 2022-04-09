import { M, marshal, Marshaller } from "@zensors/sheriff";

export class FileTransferAction {
	public readonly action: "exit" | "checksum" | "upload" | "done";
	public readonly body?: string;

	public constructor(args: FileTransferAction.ConstructorArgs) {
		this.action = args.action;
		this.body = args.body;
	}

	public static fromJson(json: FileTransferAction.AsJson) {
		return new FileTransferAction({
			action: json.action,
			body: json.body,
		});
	}

	public static fromUnknown(json: unknown): FileTransferAction {
		marshal(json, FileTransferAction.Marshaller);
		return FileTransferAction.fromJson(json);
	}

	public toJson(): FileTransferAction.AsJson {
		return {
			action: this.action,
			body: this.body,
		};
	}
}

export namespace FileTransferAction {
	export interface ConstructorArgs {
		action: "exit" | "checksum" | "upload" | "done";
		body?: string;
	}

	export interface AsJson {
		action: "exit" | "checksum" | "upload" | "done";
		body?: string;
	}

	export const Marshaller: Marshaller<AsJson> = M.obj({
		action: M.union(M.lit("exit"), M.lit("checksum"), M.lit("upload"), M.lit("done")),
		body: M.opt(M.str),
	});
}
