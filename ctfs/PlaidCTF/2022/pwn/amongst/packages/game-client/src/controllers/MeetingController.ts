import { SystemKind, SystemState } from "@amongst/game-common";
import { MeetingAction } from "@amongst/game-common";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { BasicController } from "./BasicController.js";

export class MeetingController extends BasicController<MeetingAction> {
	public readonly kind = SystemKind.Meeting;
	public state: SystemState.Meeting;
	public selfVoted: boolean;

	public constructor(state: SystemState.Meeting) {
		super();
		this.state = state;
		this.selfVoted = false;
	}

	public attach(game: Game, self: Self) {
		super.attach(game, self);
		this.selfVoted = false;
	}

	public vote(player: string | undefined) {
		this.queue.push(new MeetingAction({ vote: player }));
		this.selfVoted = true;
	}

	public detach(game: Game, self: Self): void {
		super.detach(game, self);
	}
}
