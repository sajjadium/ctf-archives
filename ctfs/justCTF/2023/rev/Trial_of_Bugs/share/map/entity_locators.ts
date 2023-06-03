import {Entity} from "../entity/entity";

abstract class EntityLocator {
    entity: Entity;

    constructor(entity: Entity) {
        this.entity = entity;
    }
}


export class PlayerEntityLocator extends EntityLocator {
}
export class CameraEntityLocator extends EntityLocator {
}

