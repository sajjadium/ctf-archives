export function createPointLike<T extends string>(name: T) {
	class Point {
		public readonly x: number;
		public readonly y: number;

		constructor(x: number, y: number) {
			this.x = x;
			this.y = y;
		}

		public static readonly Origin = new Point(0, 0);

		public static fromPostgres(point: string): Point {
			const [x, y] = point.split(",").map(Number);
			return new Point(x, y);
		}

		public static fromJson(point: Point.AsJson): Point {
			return new Point(point.x, point.y);
		}

		public toPostgres(): string {
			return `${this.x},${this.y}`;
		}

		public toJson() {
			return {
				x: this.x,
				y: this.y,
			};
		}

		public add(point: Point): Point {
			return new Point(this.x + point.x, this.y + point.y);
		}

		public subtract(point: Point): Point {
			return new Point(this.x - point.x, this.y - point.y);
		}

		public magnitude(): number {
			return Math.sqrt(this.x * this.x + this.y * this.y);
		}

		public distanceTo(point: Point): number {
			return this.subtract(point).magnitude();
		}

		public rotateClockwise(): Point {
			return new Point(-this.y, this.x);
		}

		public rotateCounterClockwise(): Point {
			return new Point(this.y, -this.x);
		}

		public toInts(): Point {
			return new Point(Math.round(this.x), Math.round(this.y));
		}

		public scale(factor: number): Point {
			return new Point(this.x * factor, this.y * factor);
		}

		public clone(): Point {
			return new Point(this.x, this.y);
		}

		public equals(point: Point): boolean {
			return this.x === point.x && this.y === point.y;
		}
	}

	Object.defineProperty(Point, "name", { value: name });
	return Point;
}

export namespace Point {
	export interface AsJson {
		x: number;
		y: number;
	}
}
