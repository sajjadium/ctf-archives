import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";

import { Heading, Point } from "@puzzled/types";

import { PointTransformer } from "./helpers/PointTransformer.mjs";

@Entity({ orderBy: { id: "ASC" }})
export class Gust {
	@PrimaryGeneratedColumn()
	public id: number;

	@Column({
		type: "point",
		transformer: new PointTransformer()
	})
	public location: Point;

	@Column({
		type: "enum",
		enum: Heading
	})
	public heading: Heading;
}
