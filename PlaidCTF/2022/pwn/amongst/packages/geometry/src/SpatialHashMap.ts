import { Box } from "./Box.js";

export interface SpatiallyHashable {
	getBoundingBox(): Box;
}

const CellSize = 20;

/**
 * A basic implementation of a spatial hash map.  The idea is that we can use
 * this to find potential collisions, and then apply more precise collision
 * detection on the short list.
 */
export class SpatialHashMap<T extends SpatiallyHashable> {
	private objects: Map<number, Map<number, Set<{ object: T; box: Box }>>>;

	public constructor(objects: T[]) {
		this.objects = new Map();

		for (const object of objects) {
			const box = object.getBoundingBox();

			for (const [x, y] of this.getCells(box)) {
				if (!this.objects.has(x)) {
					this.objects.set(x, new Map());
				}

				const xMap = this.objects.get(x)!;

				if (!xMap.has(y)) {
					xMap.set(y, new Set());
				}

				const ySet = xMap.get(y)!;
				ySet.add({ object, box });
			}
		}
	}

	public getPossibleCollisions(object: SpatiallyHashable): T[] {
		let ret: Set<{ object: T; box: Box }> = new Set();
		const testBox = object.getBoundingBox();

		for (const [x, y] of this.getCells(testBox)) {
			const set = this.objects.get(x)?.get(y);

			if (set !== undefined) {
				ret = new Set([...ret, ...set]);
			}
		}

		return [...ret].filter(({ box }) => box.intersects(testBox)).map(({ object: obj }) => obj);
	}

	private *getCells(box: Box): Generator<[number, number]> {
		const topLeft = box.topLeft.scale(1 / CellSize);
		const bottomRight = box.bottomRight.scale(1 / CellSize);

		for (let x = Math.floor(topLeft.x); x <= Math.floor(bottomRight.x); x++) {
			for (let y = Math.floor(topLeft.y); y <= Math.floor(bottomRight.y); y++) {
				yield [x, y];
			}
		}
	}
}
