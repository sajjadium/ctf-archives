import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";

import { Point } from "@puzzled/types";

import { PointTransformer } from "./helpers/PointTransformer.mjs";

@Entity({ orderBy: { id: "ASC" }})
export class Buoy {
	@PrimaryGeneratedColumn()
	public id: number;

	@Column({ type: "int" })
	public value: number;

	@Column({
		type: "point",
		transformer: new PointTransformer()
	})
	public location: Point;
}
