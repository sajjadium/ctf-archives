import * as Imm from "immutable";

import { Box, Point, Polygon, SpatialHashMap } from "@amongst/geometry";

import { Color } from "./Color.js";
import { PlayerWidth, VisibilityRadius } from "./constants.js";
import { Device } from "./Device.js";
import { MapGraphics } from "./MapGraphics.js";
import { Wall } from "./Wall.js";

export class LevelMap {
	public readonly id: string;
	public readonly walls: Wall[];
	public readonly devices: Map<string, Device>;
	public readonly spawnPoints: Imm.Map<Color, Point>;
	public readonly bounds: Box;
	public readonly graphics: MapGraphics;
	private wallMap: SpatialHashMap<Wall>;
	private deviceMap: SpatialHashMap<Device>;

	private constructor(
		id: string,
		walls: Wall[],
		devices: Map<string, Device>,
		spawnPoints: Imm.Map<Color, Point>,
		bounds: Box,
		graphics: MapGraphics
	) {
		this.id = id;
		this.walls = walls;
		this.wallMap = new SpatialHashMap(walls);
		this.devices = devices;
		this.deviceMap = new SpatialHashMap([...devices.values()]);
		this.spawnPoints = spawnPoints;
		this.bounds = bounds;
		this.graphics = graphics;
	}

	public static fromJson(json: LevelMap.AsJson): LevelMap {
		return new LevelMap(
			json.id,
			json.walls.map(Wall.fromJson),
			new Map(json.devices.map(Device.fromJson).map((device) => [device.id, device])),
			Imm.Map(
				Object.entries(json.spawnPoints)
					.map(([color, pointJson]) => [color as Color, Point.fromJson(pointJson)])
			),
			Box.fromJson(json.bounds),
			MapGraphics.fromJson(json.graphics)
		);
	}

	public applyWalls(point: Point): Point {
		const playerSize = new Point(PlayerWidth, PlayerWidth);
		const testBox = new Box(point.sub(playerSize.scale(0.5)), point.add(playerSize.scale(0.5)));
		const walls = this.wallMap.getPossibleCollisions(testBox);

		for (const wall of walls) {
			point = wall.pushPlayer(point);
		}

		return point;
	}

	public applyBounds(point: Point): Point {
		return this.bounds.constrain(point);
	}

	public getDeviceAtPoint(point: Point): Device | undefined {
		const devices = this.deviceMap.getPossibleCollisions(new Box(point, point));

		for (const device of devices) {
			if (device.hitArea.contains(point)) {
				return device;
			}
		}

		return undefined;
	}

	public hasWallBetween(from: Point, to: Point, omitTransparent = false): boolean {
		let possibleWalls = this.wallMap.getPossibleCollisions(Box.fromPoints(from, to));

		if (omitTransparent) {
			possibleWalls = possibleWalls.filter((wall) => !wall.transparent);
		}

		const intersection = this.findClosestIntersection(from, to.sub(from).ang(), possibleWalls);

		if (intersection === undefined) {
			return false;
		}

		const [intersectionPoint, _wall] = intersection;
		return from.dist2(to) > from.dist2(intersectionPoint);
	}

	public getVisiblityPolygon(point: Point): Polygon {
		const visibilityOffset = new Point(VisibilityRadius, VisibilityRadius);
		const walls = (
			this.wallMap
				.getPossibleCollisions(new Box(point.sub(visibilityOffset), point.add(visibilityOffset)))
				.filter((wall) => !wall.transparent)
		);

		let points: [number, Point, Wall | undefined][] = [];

		for (const wall of walls) {
			for (const p of [wall.start, wall.end]) {
				const q = p.sub(point);

				if (q.isOrigin()) {
					continue;
				}

				const angle = q.ang();

				for (const a of [angle - 0.001, angle, angle + 0.001]) {
					const na = this.normAngle(a);
					const intersection = this.findClosestIntersection(point, na, walls);

					if (intersection !== undefined) {
						points.push([na, intersection[0], intersection[1]]);
					}
				}
			}
		}

		for (let i = 0; i < 8; i++) {
			const a = i * Math.PI / 4;
			const intersection = this.findClosestIntersection(point, a, walls);

			if (intersection === undefined) {
				points.push([
					a,
					point.add(new Point(Math.cos(a), Math.sin(a)).scale(2 * VisibilityRadius)),
					undefined
				]);
			} else {
				points.push([a, intersection[0], intersection[1]]);
			}
		}

		points.sort((a, b) => a[0] - b[0]);

		let finalPoints: Point[] = [];

		for (let i = 0; i < points.length; i++) {
			const [_a, pt, wall] = points[i];

			if (
				wall === undefined
				|| points[(i + 1) % points.length][2] !== wall
				|| points[(i + points.length - 1) % points.length][2] !== wall
			) {
				finalPoints.push(pt);
			}
		}

		return new Polygon(finalPoints);
	}

	private normAngle(x: number) {
		const twopi = 2 * Math.PI;
		return ((x % twopi) + twopi) % twopi;
	}

	private findClosestIntersection(point: Point, angle: number, walls: Wall[]): [Point, Wall] | undefined {
		let minT = Infinity;
		let minWall;
		const p = point;
		const r = new Point(Math.cos(angle), Math.sin(angle));

		for (const wall of walls) {
			const q = wall.start;
			const s = wall.end.sub(wall.start);
			const cross = r.cross(s);

			if (cross < 0) {
				// You can't see the back of a wall
				continue;
			}

			const pToQ = q.sub(p);
			const t = pToQ.cross(s) / cross;
			const u = pToQ.cross(r) / cross;

			if (0 <= t && t < minT && -1e-8 <= u && u <= 1 + 1e-8) {
				minT = t;
				minWall = wall;
			}
		}

		if (minWall === undefined) {
			return undefined;
		}

		return [p.add(r.scale(minT)), minWall];
	}
}

export namespace LevelMap {
	export interface AsJson {
		id: string;
		walls: Wall.AsJson[];
		devices: Device.AsJson[];
		spawnPoints: { [k in Color]: Point.AsJson };
		bounds: Box.AsJson;
		graphics: MapGraphics.AsJson;
	}
}
