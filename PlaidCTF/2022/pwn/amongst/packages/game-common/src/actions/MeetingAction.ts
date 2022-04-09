import { M, marshal, Marshaller } from "@zensors/sheriff";

export class MeetingAction {
	public readonly vote?: string;

	public constructor(args: MeetingAction.ConstructorArgs) {
		this.vote = args.vote;
	}

	public static fromJson(json: MeetingAction.AsJson) {
		return new MeetingAction({
			vote: json.vote,
		});
	}

	public static fromUnknown(json: unknown): MeetingAction {
		marshal(json, MeetingAction.Marshaller);
		return MeetingAction.fromJson(json);
	}

	public toJson(): MeetingAction.AsJson {
		return {
			vote: this.vote,
		};
	}
}

export namespace MeetingAction {
	export interface ConstructorArgs {
		vote?: string;
	}

	export interface AsJson {
		vote?: string;
	}

	export const Marshaller: Marshaller<AsJson> = M.obj({
		vote: M.opt(M.str),
	});
}
