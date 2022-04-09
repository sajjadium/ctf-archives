import { Map } from "immutable";

import { HoldPurpose, MeetingAction, SystemKind, SystemState } from "@amongst/game-common";

import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

export class MeetingSystem extends System<SystemKind.Meeting> {
	private active: boolean;
	private votes: Map<string, string | undefined>;
	private calledBy: string;
	private trigger: { kind: "emergency" } | { kind: "body"; body: string };

	public constructor(id: number) {
		super(SystemKind.Meeting, id);
		this.active = false;
		this.votes = Map();
		this.calledBy = "";
		this.trigger = { kind: "emergency" };
	}

	public initMeeting(game: Game, calledBy: string, trigger: { kind: "emergency" } | { kind: "body"; body: string }) {
		this.active = true;
		this.votes = Map();
		this.calledBy = calledBy;
		this.trigger = trigger;

		game.level.holdSystem.init(game, game.tick + 60, new HoldPurpose.MeetingStart());

		game.players.forEach((player) => {
			player.setSystem(game, game.level.holdSystem);
			player.location = game.level.map.spawnPoints.get(player.color) ?? player.location;
			player.desync();
		});

		game.bodies.clear();
	}

	public getStateForPlayer(_player: Player): SystemState | undefined {
		return {
			kind: this.kind,
			id: this.id,
			devices: [],
			calledBy: this.calledBy,
			trigger: this.trigger,
			votesSubmitted: [...this.votes.keys()]
		};
	}

	public accept(_game: Game, _player: Player, _device?: string): boolean {
		return true;
	}

	public attach(_game: Game, _player: Player) {
		// nothing to do
	}

	public tick(game: Game, player: Player, actionJson?: unknown) {
		if (player.dead || actionJson === undefined || this.votes.has(player.id)) {
			return;
		}

		const action = MeetingAction.fromUnknown(actionJson);

		if (action.vote !== undefined && !game.players.has(action.vote)) {
			// What are you trying to pull here?
			player.desync();
			return;
		}

		this.votes = this.votes.set(player.id, action.vote);
	}

	public afterTick(game: Game): void {
		if (!this.active) {
			return;
		}

		for (const player of game.players.values()) {
			if (!player.dead && !this.votes.has(player.id)) {
				return; // not all votes have been submitted
			}
		}

		const voteCounts = this.votes.valueSeq().countBy((vote) => vote);
		const maxCount = voteCounts.max();
		const selected = voteCounts.filter((count) => count === maxCount).keySeq().toList();
		let outcome: HoldPurpose.VoteComplete.Outcome;

		if (selected.size === 1) {
			const selectedPlayerId = selected.get(0);

			if (selectedPlayerId !== undefined) {
				const selectedPlayer = game.players.get(selectedPlayerId);

				if (selectedPlayer !== undefined) {
					selectedPlayer.dead = true;

					outcome = {
						kind: "ejected",
						player: selectedPlayer.id,
						hoaxer: selectedPlayer.hoaxer
					};
				} else {
					// ???
					outcome = {
						kind: "ejected",
						player: selectedPlayerId,
						hoaxer: false
					};
				}
			} else {
				outcome = { kind: "skipped" };
			}
		} else {
			outcome = { kind: "tie" };
		}

		game.level.holdSystem.init(game, game.tick + 100, new HoldPurpose.VoteComplete(outcome));

		game.players.forEach((player) => {
			player.setSystem(game, game.level.holdSystem);
			player.desync();
		});

		this.active = false;
	}

	public detach(_game: Game, _player: Player): void {
		// nothing to do
	}
}
