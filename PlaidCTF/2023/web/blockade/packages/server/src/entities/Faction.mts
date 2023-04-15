import type { Relation } from "typeorm";
import { Column, Entity, OneToMany, PrimaryGeneratedColumn } from "typeorm";

import { Ship } from "./Ship.mjs";

@Entity({ orderBy: { id: "ASC" }})
export class Faction {
	@PrimaryGeneratedColumn()
	public id: number;

	@Column()
	public name: string;

	@Column()
	public score: number;

	@OneToMany(() => Ship, (ship) => ship.faction)
	public ships: Relation<Ship>[];
}
