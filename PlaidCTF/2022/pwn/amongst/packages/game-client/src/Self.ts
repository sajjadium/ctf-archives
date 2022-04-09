import { Socket } from "socket.io-client";

import { Color, PlayerVisualState } from "@amongst/game-common";
import { Point } from "@amongst/geometry";
import { ClientEvent, ServerEvent } from "@amongst/messages";

import { Controller } from "./controllers/index.js";
import { Game } from "./Game.js";
import { Player } from "./Player.js";

export class Self extends Player {
	public socket: Socket<ServerEvent, ClientEvent>;
	public location: Point;
	public visualState: PlayerVisualState;
	public dead: boolean;
	public hoaxer: boolean;
	public emergencyMeetings: number;
	public syncId: number;
	public tick: number;
	public controller: Controller;

	public constructor(
		id: string,
		socket: Socket<ServerEvent, ClientEvent>,
		name: string,
		color: Color,
		location: Point,
		visualState: PlayerVisualState,
		dead: boolean,
		hoaxer: boolean,
		emergencyMeetings: number,
		syncId: number,
		tick: number,
		controller: Controller,
	) {
		super(id, name, color);
		this.socket = socket;
		this.location = location;
		this.visualState = visualState;
		this.dead = dead;
		this.hoaxer = hoaxer;
		this.emergencyMeetings = emergencyMeetings;
		this.syncId = syncId;
		this.tick = tick;
		this.controller = controller;
	}

	public setController(game: Game, controller: Controller) {
		this.controller.detach(game, this);
		this.controller = controller;
		this.controller.attach(game, this);
	}
}
