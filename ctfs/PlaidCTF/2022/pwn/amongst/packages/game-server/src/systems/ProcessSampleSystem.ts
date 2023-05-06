import { ProcessSampleAction, ProcessSampleTime, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

const CryptoFlag = process.env.CRYPTO_FLAG ?? "PCTF{SAMPLE_FLAG_USE_ENV_PLS__}";

if (!/PCTF\{[A-Z_!\?]{25}\}/.test(CryptoFlag)) {
	throw new Error("Invalid CryptoFlag");
}

const Secret = CryptoFlag.slice(5, -1);
const Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_!?";
const N = Alphabet.length;
const SecretMatrix = Array.from(
	new Array(5),
	(_, i) => Array.from(
		new Array(5),
		(__, j) => Alphabet.indexOf(Secret[i * 5 + j])
	)
);

function generateSampleId() {
	return Array.from(new Array(25), () => Alphabet[Math.floor(Math.random() * N)]).join("");
}

function cipher(input: string) {
	if (input.length !== 25) {
		throw new Error("Invalid input");
	}

	let out = "";

	for (let i = 0; i < 5; i++) {
		const block = input.slice(i * 5, i * 5 + 5).split("").map((c) => Alphabet.indexOf(c));
		const result = (
			SecretMatrix
				.map((row) => row.map((val, j) => val * block[j]).reduce((a, b) => a + b, 0))
				.map((val) => Alphabet[val % N])
				.join("")
		);
		out += result;
	}

	return out;
}

export class ProcessSampleSystem extends System<SystemKind.ProcessSample> {
	private device: string;
	private beginPlayer: Player;
	private endPlayer: Player;
	private timer?: number;
	private taskComplete: boolean;
	private sampleId: string;

	public constructor(id: number, device: string, beginPlayer: Player, endPlayer: Player) {
		super(SystemKind.ProcessSample, id);
		this.device = device;
		this.beginPlayer = beginPlayer;
		this.endPlayer = endPlayer;
		this.timer = undefined;
		this.taskComplete = false;
		this.sampleId = generateSampleId();
	}

	public accept(game: Game, player: Player, device?: string): boolean {
		return (
			device === this.device
			&& (player === this.beginPlayer || player === this.endPlayer)
			&& !this.taskComplete
		);
	}

	public attach(_game: Game, player: Player) {
		if (player === this.beginPlayer) {
			player.pushUpdate(
				new GameUpdate.ProcessSampleDisplayUpdate({
					content: this.sampleId
				})
			);
			return;
		}

		if (player === this.endPlayer && this.timer === 0) {
			this.sendResultMessage();
		}
	}

	public getStateForPlayer(player: Player): SystemState | undefined {
		if (player !== this.beginPlayer && player !== this.endPlayer) {
			return undefined;
		}

		return this.getStateForValidPlayer(player);
	}

	public tick(game: Game, player: Player, actionJson?: unknown) {
		if (actionJson === undefined) {
			return;
		}

		const action = ProcessSampleAction.fromUnknown(actionJson);

		switch (action.action) {
			case "begin": {
				if (player !== this.beginPlayer || this.timer !== undefined) {
					throw new Error("Invalid action");
				}

				this.timer = ProcessSampleTime;
				this.updatePlayers();
				break;
			}

			case "end": {
				if (player !== this.endPlayer || this.timer === undefined || this.timer > 0) {
					throw new Error("Invalid action");
				}

				this.taskComplete = true;
				this.updatePlayers();
				break;
			}

			case "exit": {
				player.setSystem(game, game.level.movementSystem);
				break;
			}
		}
	}

	public afterTick(_game: Game): void {
		if (!this.taskComplete && this.timer !== undefined && this.timer > 0) {
			this.timer--;

			if (this.timer === 0 && this.endPlayer.system === this) {
				this.sendResultMessage();
			}
		}
	}

	public detach(_game: Game, _player: Player) {
		// nothing to do
	}

	public blockVictory(): boolean {
		return !this.taskComplete;
	}

	private updatePlayers() {
		this.beginPlayer.pushUpdate(
			new GameUpdate.SystemStateUpdate({
				state: this.getStateForValidPlayer(this.beginPlayer)
			})
		);

		this.endPlayer.pushUpdate(
			new GameUpdate.SystemStateUpdate({
				state: this.getStateForValidPlayer(this.endPlayer)
			})
		);
	}

	private getStateForValidPlayer(player: Player): SystemState {
		return {
			kind: this.kind,
			id: this.id,
			devices: !this.taskComplete ? [this.device] : [],
			taskComplete: this.taskComplete,
			timerEndsAt: (
				this.timer === undefined ? undefined :
				this.timer + player.game.tick
			),
			role: player === this.beginPlayer ? "begin" : "end"
		};
	}

	private sendResultMessage() {
		this.endPlayer.pushUpdate(
			new GameUpdate.ProcessSampleDisplayUpdate({
				content: cipher(this.sampleId)
			})
		);
	}
}
