import { Color, PlayerVisualState } from "@amongst/game-common";
import { Point } from "@amongst/geometry";

export class Player {
	public id: string;
	public name: string;
	public color: Color;
	public location?: Point;
	public visualState?: PlayerVisualState;
	public dead?: boolean;
	public hoaxer?: boolean;

	public constructor(
		id: string,
		name: string,
		color: Color
	) {
		this.id = id;
		this.name = name;
		this.color = color;
	}
}
