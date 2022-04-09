import { M, Marshaller } from "@zensors/sheriff";

export class Point {
	public constructor(
		public readonly x: number,
		public readonly y: number,
	) {
		if (isNaN(x) || isNaN(y)) {
			throw new Error("Encountered NaN");
		}
	}

	public mag2() {
		return this.x * this.x + this.y * this.y;
	}

	public mag() {
		return Math.sqrt(this.mag2());
	}

	public add(p: Point) {
		return new Point(this.x + p.x, this.y + p.y);
	}

	public sub(p: Point) {
		return new Point(this.x - p.x, this.y - p.y);
	}

	public scale(sx: number, sy?: number) {
		return new Point(this.x * sx, this.y * (sy ?? sx));
	}

	public dist2(p: Point) {
		return this.sub(p).mag2();
	}

	public dist(p: Point) {
		return this.sub(p).mag();
	}

	public dot(p: Point) {
		return this.x * p.x + this.y * p.y;
	}

	public cross(p: Point) {
		return this.x * p.y - this.y * p.x;
	}

	public unit() {
		const mag = this.mag();
		return mag === 0 ? Point.Origin : this.scale(1 / mag);
	}

	public ang() {
		return Math.atan2(this.y, this.x);
	}

	public isOrigin() {
		return this.x === 0 && this.y === 0;
	}

	public equals(p: Point) {
		return this.x === p.x && this.y === p.y;
	}

	public toJson(): Point.AsJson {
		return [this.x, this.y];
	}

	public toSvg(): string {
		return `${this.x},${this.y}`;
	}
}

export namespace Point {
	export type AsJson = [x: number, y: number];
	export const Marshaller: Marshaller<AsJson> = M.tup(M.num, M.num);

	export const fromJson = (json: AsJson) => new Point(json[0], json[1]);
	export const Origin = new Point(0, 0);
}
