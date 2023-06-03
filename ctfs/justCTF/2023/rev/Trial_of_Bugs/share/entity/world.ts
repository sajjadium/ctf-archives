import {Component, ComponentRegistry} from "./component";
import {Entity} from "./entity";

export class World {
    name: string;
    componentRegistry: ComponentRegistry;
    entities: {[entId: number]: Entity} = {};
    singletons: {[name: string]: any} = {};
    defaultComponents: (new () => Component)[] = [];
    private nextEntityId: number = 1;

    constructor(name: string, componentRegistry: ComponentRegistry) {
        this.name = name;
        this.componentRegistry = componentRegistry;
    }

    save(): any {
        const ret: any = {};
        for (const entId in this.entities)
            ret[entId] = this.entities[entId].save();
        return ret;
    }

    newEntity() {
        const id = this.nextEntityId++;
        const ret = new Entity(this, id);
        for (const component of this.defaultComponents)
            ret.addComponent(component);
        this.entities[id] = ret;
        return ret;
    }

    getEntity(entId: number): Entity|undefined {
        return this.entities[entId];
    }

    addSingleton(singleton: any) {
        this.singletons[singleton.constructor.name] = singleton;
    }

    getSingleton<T>(singleton: new (...args: any[]) => T): T {
        return this.singletons[singleton.name] as T;
    }
}
