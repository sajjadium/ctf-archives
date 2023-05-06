import crc from "crc-32";

import { FileTransferAction, FileTransferRateLimit, SystemKind, SystemState } from "@amongst/game-common";
import { GameUpdate } from "@amongst/messages";

import { Game } from "../Game.js";
import { Self } from "../Self.js";
import { BasicController } from "./BasicController.js";
import { MovementController } from "./MovementController.js";

export class FileTransferController extends BasicController<FileTransferAction> {
	public static downloadMap = new Map<number, string>();
	public readonly kind = SystemKind.FileTransfer;
	public state: SystemState.FileTransfer;
	public downloadPosition: number;
	public downloadTotal: number;
	public uploadPosition: number;
	public uploadTotal: number;

	public constructor(state: SystemState.FileTransfer) {
		super();
		this.state = state;
		this.downloadPosition = 0;
		this.downloadTotal = 1;
		this.uploadPosition = 0;
		this.uploadTotal = 0;
	}

	public attach(game: Game, self: Self) {
		super.attach(game, self);
		this.downloadPosition = 0;
		this.downloadTotal = 1;
		this.uploadPosition = 0;
		this.uploadTotal = FileTransferController.downloadMap.get(this.state.id)?.length ?? 0;
	}

	public receive(game: Game, self: Self, packet: GameUpdate.FileDownloadPacket) {
		if (packet.position === 0) {
			FileTransferController.downloadMap.set(this.state.id, "");
		}

		const data = (FileTransferController.downloadMap.get(this.state.id) ?? "") + atob(packet.data);
		FileTransferController.downloadMap.set(this.state.id, data);
		this.downloadPosition = data.length;
		this.downloadTotal = packet.totalSize;

		if (data.length === packet.totalSize) {
			this.queue.push(
				new FileTransferAction({
					action: "checksum",
					body: crc.bstr(data, 0).toString()
				})
			);
			self.setController(game, new MovementController());
		}
	}

	public exit(game: Game, self: Self): void {
		this.queue.push(new FileTransferAction({ action: "exit" }));
		self.setController(game, new MovementController());
	}

	public detach(game: Game, self: Self): void {
		super.detach(game, self);
	}

	protected beforeTick(game: Game, self: Self) {
		if (this.state.downloadComplete && !this.state.uploadComplete) {
			const data = FileTransferController.downloadMap.get(this.state.id) ?? "";

			if (this.uploadPosition < data.length) {
				this.queue.push(
					new FileTransferAction({
						action: "upload",
						body: btoa(data.slice(this.uploadPosition, this.uploadPosition + FileTransferRateLimit))
					})
				);
				this.uploadPosition += FileTransferRateLimit;
			} else {
				this.queue.push(
					new FileTransferAction({
						action: "done"
					})
				);
				self.setController(game, new MovementController());
			}
		}
	}
}

(window as any).FileTransferController = FileTransferController; // you're welcome
