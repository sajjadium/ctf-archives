import pg from "pg";

import { ProvideCredentialsAction, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

interface Credentials {
	id: number;
	username: string;
	password: string;
}

const CredentialOptions = [
	{ id: 1, username: "zuck", password: "hunter2" },
	{ id: 2, username: "randall", password: "correcthorsebatterystaple" },
	{ id: 3, username: "richard", password: "cowabunga" },
];

const pool = new pg.Pool({
	connectionString:
		process.env.PROVIDE_CREDENTIALS_CONNECTION_STRING ?? "postgresql://amongst:amongst@localhost:5432/postgres"
});
pool.connect();

export class ProvideCredentialsSystem extends System<SystemKind.ProvideCredentials> {
	private device: string;
	private player: Player;
	private credentials: Credentials;
	private complete: boolean;

	public constructor(id: number, device: string, player: Player) {
		super(SystemKind.ProvideCredentials, id);
		this.device = device;
		this.player = player;
		this.credentials = CredentialOptions[Math.floor(Math.random() * CredentialOptions.length)];
		this.complete = false;
	}

	public accept(game: Game, player: Player, device?: string): boolean {
		return device === this.device && player === this.player;
	}

	public attach(_game: Game, _player: Player) {
		// nothing to do
	}

	public getStateForPlayer(player: Player): SystemState | undefined {
		if (player !== this.player) {
			return undefined;
		}

		return this.getStateForValidPlayer();
	}

	public tick(game: Game, player: Player, actionJson?: unknown) {
		if (actionJson === undefined) {
			return;
		}

		const action = ProvideCredentialsAction.fromUnknown(actionJson);

		if (action.exit) {
			player.setSystem(game, game.level.movementSystem);
			return;
		}

		let username = action.username;
		let password = action.password;

		// No sql injection
		username = username.replace("'", "''");
		password = password.replace("'", "''");

		// Max length of username and password is 32
		username = username.substring(0, 32);
		password = password.substring(0, 32);

		pool.query<{ id: number; username: string }>(
			`SELECT id, username FROM users WHERE username = '${username}' AND password = '${password}'`
		)
			.then((result) => {
				if (this.complete) {
					throw new Error("Invalid state");
				}

				if (result.rowCount !== 1) {
					throw new Error("Invalid credentials");
				}

				if (result.rows[0].id !== this.credentials.id) {
					throw new Error("Invalid credentials");
				}

				this.complete = true;
				this.updatePlayers();
				player.pushUpdate(
					new GameUpdate.ProvideCredentialsResponse({
						success: true,
						message: `Successfully logged in as ${result.rows[0].username}`
					})
				);
			})
			.catch(() => {
				player.pushUpdate(
					new GameUpdate.ProvideCredentialsResponse({
						success: false,
						message: "Invalid credentials"
					})
				);
			});
	}

	public afterTick(_game: Game): void {
		// nothing to do
	}

	public detach(_game: Game, _player: Player) {
		// nothing to do
	}

	public blockVictory(): boolean {
		return !this.complete;
	}

	private updatePlayers() {
		this.player.pushUpdate(
			new GameUpdate.SystemStateUpdate({
				state: this.getStateForValidPlayer()
			})
		);
	}

	private getStateForValidPlayer(): SystemState {
		return {
			kind: this.kind,
			id: this.id,
			devices: !this.complete ? [this.device] : [],
			credentials: {
				username: this.credentials.username,
				password: this.credentials.password
			},
			complete: this.complete
		};
	}
}
