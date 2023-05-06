import { HoldPurpose, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

export class HoldSystem extends System<SystemKind.Hold> {
	private until: number;
	public purpose: HoldPurpose;

	public constructor(id: number) {
		super(SystemKind.Hold, id);
		this.until = 0;
		this.purpose = new HoldPurpose.GameStart(0);
	}

	public init(game: Game, until: number, purpose: HoldPurpose) {
		this.until = until;
		this.purpose = purpose;

		game.players.forEach((player) => {
			player.pushUpdate(
				new GameUpdate.SystemStateUpdate({
					state: this.getState()
				})
			);
		});
	}

	public getStateForPlayer(_player: Player): SystemState | undefined {
		return this.getState();
	}

	public accept(_game: Game, _player: Player, _device?: string): boolean {
		return false;
	}

	public attach(_game: Game, _player: Player) {
		// nothing to do
	}

	public tick(
		_game: Game,
		_player: Player,
		_actionJson?: unknown
	) {
		// nothing to do
	}

	public afterTick(game: Game) {
		if (game.tick === this.until) {
			switch (this.purpose.kind) {
				case HoldPurpose.Kind.GameStart:
				case HoldPurpose.Kind.VoteComplete: {
					game.players.forEach((player) => {
						// This should be handleable client-side, so we don't need to desync
						player.setSystem(game, game.level.movementSystem);
					});
					break;
				}

				case HoldPurpose.Kind.MeetingStart: {
					game.players.forEach((player) => {
						// Force a desync because we haven't informed the player of what the meeting is about yet
						player.setSystem(game, game.level.meetingSystem);
						player.desync();
					});
					break;
				}

				case HoldPurpose.Kind.GameEnd: {
					// Game is over, kill it
					game.disconnect();
					break;
				}
			}
		}
	}

	public detach(_game: Game, _player: Player) {
		// nothing to do
	}

	private getState(): SystemState {
		return {
			kind: this.kind,
			id: this.id,
			devices: [],
			until: this.until,
			purpose: this.purpose.toJson()
		};
	}
}
