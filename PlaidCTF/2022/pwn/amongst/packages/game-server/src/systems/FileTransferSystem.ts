import crc from "crc-32";
import { readFileSync } from "fs";
import { URL } from "url";

import { FileTransferAction, FileTransferRateLimit, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Player } from "../Player.js";
import { System } from "./System.js";

const FileContents = readFileSync(new URL("../../assets/sus", import.meta.url));
const FileChecksum = crc.buf(FileContents, 0).toString();

export class FileTransferSystem extends System<SystemKind.FileTransfer> {
	private downloadPosition: number;
	private downloadComplete: boolean;
	private uploadBuffer: Buffer;
	private uploadComplete: boolean;
	private player: Player;
	private downloadDevice: string;
	private uploadDevice: string;

	public constructor(id: number, player: Player, downloadDevice: string, uploadDevice: string) {
		super(SystemKind.FileTransfer, id);
		this.player = player;
		this.downloadDevice = downloadDevice;
		this.uploadDevice = uploadDevice;
		this.downloadPosition = 0;
		this.downloadComplete = false;
		this.uploadBuffer = Buffer.alloc(0);
		this.uploadComplete = false;
	}

	public getStateForPlayer(player: Player): SystemState | undefined {
		if (player.id !== this.player.id) {
			return undefined;
		}

		return this.getStateForTargetPlayer();
	}

	public accept(_game: Game, player: Player, device?: string): boolean {
		if (player.id !== this.player.id) {
			return false;
		}

		if (!this.downloadComplete) {
			return device === this.downloadDevice;
		}

		if (!this.uploadComplete) {
			return device === this.uploadDevice;
		}

		return false;
	}

	public attach(_game: Game, _player: Player) {
		this.downloadPosition = 0;
		this.uploadBuffer = Buffer.alloc(0);
	}

	public tick(
		game: Game,
		player: Player,
		actionJson?: unknown
	) {
		if (!this.downloadComplete) {
			if (this.downloadPosition < FileContents.length) {
				player.pushUpdate(
					new GameUpdate.FileDownloadPacket({
						id: this.id,
						position: this.downloadPosition,
						totalSize: FileContents.length,
						data: (
							FileContents
								.slice(this.downloadPosition, this.downloadPosition + FileTransferRateLimit)
								.toString("base64")
						)
					})
				);

				this.downloadPosition += FileTransferRateLimit;
			}

			if (actionJson === undefined) {
				return;
			}

			const action = FileTransferAction.fromUnknown(actionJson);

			switch (action.action) {
				case "exit": {
					player.setSystem(game, game.level.movementSystem);
					break;
				}

				case "checksum": {
					player.setSystem(game, game.level.movementSystem);

					if (this.downloadPosition < FileContents.length) {
						throw new Error("File download not complete");
					}

					if (action.body !== FileChecksum) {
						throw new Error("File checksum mismatch");
					}

					this.downloadComplete = true;

					player.pushUpdate(
						new GameUpdate.SystemStateUpdate({
							state: this.getStateForTargetPlayer()
						})
					);

					break;
				}

				default: {
					player.setSystem(game, game.level.movementSystem);
					throw new Error("Invalid action");
				}
			}
		} else {
			if (actionJson === undefined) {
				return;
			}

			const action = FileTransferAction.fromUnknown(actionJson);

			switch (action.action) {
				case "exit": {
					player.setSystem(game, game.level.movementSystem);
					break;
				}

				case "upload": {
					if (action.body === undefined) {
						throw new Error("Missing body");
					}

					const content = Buffer.from(action.body, "base64");

					if (content.length > FileTransferRateLimit) {
						player.setSystem(game, game.level.movementSystem);
						throw new Error("Packet too large");
					}

					this.uploadBuffer = Buffer.concat([this.uploadBuffer, content]);

					if (this.uploadBuffer.length > 2 * FileContents.length) {
						throw new Error("Too much content uploaded");
					}

					break;
				}

				case "done": {
					if (this.uploadBuffer.length !== FileContents.length) {
						throw new Error("Uploaded file size mismatch");
					}

					const uploadedContentChecksum = crc.buf(this.uploadBuffer, 0).toString();

					player.setSystem(game, game.level.movementSystem);

					if (uploadedContentChecksum !== FileChecksum) {
						throw new Error("Invalid checksum");
					}

					this.uploadComplete = true;

					player.pushUpdate(
						new GameUpdate.SystemStateUpdate({
							state: this.getStateForTargetPlayer()
						})
					);

					break;
				}

				default: {
					player.setSystem(game, game.level.movementSystem);
					throw new Error("Invalid action");
				}
			}
		}
	}

	public afterTick(_game: Game) {
		// nothing to do
	}

	public detach(_game: Game, _player: Player) {
		// nothing to do
	}

	public blockVictory(): boolean {
		return !this.uploadComplete;
	}

	private getStateForTargetPlayer(): SystemState {
		return {
			kind: this.kind,
			id: this.id,
			devices: (
				!this.downloadComplete ? [this.downloadDevice] :
				!this.uploadComplete ? [this.uploadDevice] :
				[]
			),
			downloadComplete: this.downloadComplete,
			uploadComplete: this.uploadComplete
		};
	}
}
