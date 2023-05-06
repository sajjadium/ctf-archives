import { createPointLike } from "./createPointLike.mjs";

export const Point = createPointLike("GamePoint");
export type Point = InstanceType<typeof Point>;

export namespace Point {
	export interface AsJson {
		x: number;
		y: number;
	}
}
