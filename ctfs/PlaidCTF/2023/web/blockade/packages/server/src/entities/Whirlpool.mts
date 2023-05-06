import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";

import { Point } from "@puzzled/types";

import { PointTransformer } from "./helpers/PointTransformer.mjs";

@Entity({ orderBy: { id: "ASC" }})
export class Whirlpool {
	@PrimaryGeneratedColumn()
	public id: number;

	@Column({
		type: "point",
		transformer: new PointTransformer()
	})
	public location: Point; // location of center, so should be offset by (0.5, 0.5)

	@Column()
	public clockwise: boolean;
}
