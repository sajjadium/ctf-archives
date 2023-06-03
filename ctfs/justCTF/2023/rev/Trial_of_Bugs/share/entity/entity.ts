import {World} from "./world";
import {Component} from "./component";
import {Transform} from "./transform";


export class Entity {
    world: World;
    id: number;

    [k: string]: any;
    transform?: Transform;

    constructor(world: World, entityId: number) {
        this.world = world;
        this.id = entityId;
    }

    delete() {
        for (const component of this.getAllComponents())
            component.destroy();
        delete this.world.entities[this.id];
    }

    addComponent<T extends Component>(component: T | (new () => T)): T {
        if (!(component instanceof Component))
            component = new component();
        component.entity = this;
        this[(component.constructor as any).typeName] = component;
        return component;
    }

    removeComponent(component: Component) {
        delete this[(component.constructor as any).typeName];
    }

    getComponent<T>(component: (new () => T) & {typeName: string}): T {
        return this[component.typeName] as T;
    }

    tryGetComponent<T>(component: (new () => T) & {typeName: string}): T|undefined {
        return this[component.typeName] as T|undefined;
    }

    getAllComponents() {
        const ret: Component[] = [];
        for (const name in this) {
            if (this.hasOwnProperty(name) && name !== 'id' && name !== 'world') {
                ret.push(this[name] as Component);
            }
        }
        return ret;
    }

    load(data: any) {
        const components: Component[] = [];
        for (const k in data) {
            const component = this.world.componentRegistry.create(k);
            if (component === null) {
                console.error('Unknown component: ' + k);
                continue;
            }
            component.entity = this;
            this[component.typeName || (component.constructor as any).typeName] = component;
            component.load(data[k]);
            components.push(component);
        }

        for (const component of components) {
            if (component.getDependencies) {
                for (const dep of component.getDependencies()) {
                    if (dep in this)
                        continue;

                    const component = this.world.componentRegistry.create(dep);
                    if (component === null) {
                        console.error('Unknown component: ' + dep);
                        continue;
                    }
                    component.entity = this;
                    this[component.typeName || (component.constructor as any).typeName] = component;
                }
            }
        }

        for (const component of components) {
            component.postLoad();
        }
    }

    save() {
        const ret: any = {};
        for (const name in this) {
            if (this.hasOwnProperty(name) && name !== 'id' && name !== 'world') {
                ret[name] = this[name].save();
            }
        }
        return ret;
    }
}
