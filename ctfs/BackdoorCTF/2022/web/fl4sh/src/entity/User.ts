import { Entity, Column, PrimaryGeneratedColumn, Unique, ManyToMany, JoinTable } from "typeorm";

@Entity()
@Unique(['email'])
export class User {

    @PrimaryGeneratedColumn({ name: 'id' })
    id: number;

    @Column({ name: 'name' })
    name: string;

    @Column({ name: 'email' })
    email: string;

    @Column({ name: 'password' })
    password: string;

    @Column({type:"longtext", name: 'images' })
    images: string;

    @Column({ name: 'region' })
    region: string;
}