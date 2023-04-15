import type { Relation } from "typeorm";
import { Column, Entity, JoinColumn, ManyToOne, PrimaryGeneratedColumn } from "typeorm";

import { Heading, Point, ShipType } from "@puzzled/types";

import { Faction } from "./Faction.mjs";
import { PointTransformer } from "./helpers/PointTransformer.mjs";
import { ShipTypeInfo } from "./ShipTypeInfo.mjs";

@Entity({ orderBy: { id: "ASC" }})
export class Ship {
	@PrimaryGeneratedColumn()
	public id: number;

	@Column()
	public name: string;

	@Column({ type: "text" })
	public type: ShipType;

	@ManyToOne(() => ShipTypeInfo, { nullable: false, eager: true })
	@JoinColumn({ name: "type" })
	public typeInfo: Relation<ShipTypeInfo>;

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

	@ManyToOne(() => Faction, (faction) => faction.ships, { nullable: false, eager: true })
	public faction: Relation<Faction>;

	@Column()
	public factionId: number;

	@Column({ default: 0 })
	public damage: number;

	@Column({ default: 0 })
	public forwardTokens: number;

	@Column({ default: 0 })
	public leftTokens: number;

	@Column({ default: 0 })
	public rightTokens: number;

	@Column({ default: 0 })
	public loadedCannons: number;

	@Column({ default: 0 })
	public cannonballs: number;

	@Column({ default: false })
	public sunk: boolean;
}
