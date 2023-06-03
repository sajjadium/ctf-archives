import {CollisionItem} from "../collision/collision_data";

export type SpritesheetData = {
    name: string,
    width: number,
    height: number,
    sprites: {[name: string]: [number, number, number, number]},
    spriteCollisionItems: {[name: string]: CollisionItem[]}
}

export class SpritesheetDataManager {
    spritesheets: {[key: string]: SpritesheetData};

    constructor(spritesheets?: {[key: string]: SpritesheetData}) {
        this.spritesheets = spritesheets || {};
    }
}
