import { Column, Entity, PrimaryColumn } from "typeorm";

import { ShipType } from "@puzzled/types";

@Entity()
export class ShipTypeInfo {
	@PrimaryColumn({ type: "text" })
	public type: ShipType;

	@Column()
	public hull: number;

	@Column()
	public ramDamage: number;

	@Column()
	public cannonDamage: number;

	@Column()
	public rockDamage: number;

	@Column({ type: "float" })
	public influenceRadius: number;

	@Column()
	public cannons: number;

	@Column()
	public carpentryRate: number;

	@Column()
	public sailRate: number;

	@Column()
	public cannonRate: number;
}
