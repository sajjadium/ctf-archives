import { SystemKind, SystemState } from "@amongst/game-common";

import { Game } from "../Game.js";
import { Player } from "../Player.js";

export abstract class System<K extends SystemKind = SystemKind> {
	public readonly kind: K;
	public readonly id: number;

	public constructor(kind: K, id: number) {
		this.kind = kind;
		this.id = id;
	}

	public blockVictory() {
		return false;
	}

	public abstract getStateForPlayer(player: Player): SystemState | undefined;
	public abstract accept(game: Game, player: Player, device?: string): boolean;
	public abstract attach(game: Game, player: Player, device?: string): void;
	public abstract tick(game: Game, player: Player, action?: unknown): void;
	public abstract afterTick(game: Game): void;
	public abstract detach(game: Game, player: Player): void;
}
