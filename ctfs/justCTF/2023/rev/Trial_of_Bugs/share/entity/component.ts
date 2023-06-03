import {Entity} from "./entity";
import {stripTransientProperties, transient} from "../util/transient";

export class Component {
    static typeName?: string;
    typeName?: string;

    @transient entity!: Entity;

    load(props: any) {
        Object.assign(this, props);
    }

    save() {
        return stripTransientProperties(this);
    }

    getDependencies?(): string[];

    destroy() {
    }

    get world() {
        return this.entity.world;
    }

    postLoad() {
        //
    }

    update?(delta: number): void;

    updatePhysics?(delta: number): void;
}

export type NamedComponentType = (new () => Component) & {
    typeName: string;
}

export class ComponentRegistry {
    create(componentName: string): Component|null {
        if (globalRegistry[componentName])
            return new globalRegistry[componentName]();
        return null;
    }
}

const globalRegistry: {[name: string]: new () => Component} = {};
export function registerComponent(name: string, constructor: new () => Component) {
    globalRegistry[name] = constructor;
}

export function registerNamedComponent(constructor: NamedComponentType) {
    globalRegistry[constructor.typeName] = constructor;
}
