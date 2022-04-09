import { HoldPurpose, SystemKind, SystemState } from "@amongst/game-common";

import { Game } from "../Game";
import { Self } from "../Self";
import { MeetingController, MovementController } from ".";
import { BasicController } from "./BasicController";

export class HoldController extends BasicController<never> {
	public readonly kind = SystemKind.Hold;
	public state: SystemState.Hold;
	public purpose: HoldPurpose;

	public constructor(state: SystemState.Hold) {
		super();
		this.state = state;
		this.purpose = HoldPurpose.fromJson(state.purpose);
	}

	public updateState(state: SystemState.Hold): void {
		this.state = state;
		this.purpose = HoldPurpose.fromJson(state.purpose);
	}

	protected beforeTick(game: Game, self: Self): void {
		if (game.tick >= this.state.until) {
			switch (this.purpose.kind) {
				case HoldPurpose.Kind.GameStart:
				case HoldPurpose.Kind.VoteComplete: {
					self.setController(game, new MovementController());
				}
			}
		}
	}
}
