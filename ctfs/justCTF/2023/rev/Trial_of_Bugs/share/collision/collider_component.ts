import {Component} from "../entity/component";
import {CollisionItem} from "./collision_data";
import {transient} from "../util/transient";
import {Body, Response} from "detect-collisions";
import {CollisionSystem} from "./collision_system";
import {createBody} from "./utils";

export abstract class ColliderComponent extends Component {
    isStatic: boolean = true;
    isTrigger: boolean = false;
    isTileTrigger: boolean = false;
    isPlayerOnlyTrigger: boolean = false;
    isSolid: boolean = true;

    @transient private system!: CollisionSystem;
    @transient bodies?: Body[];
    @transient private lastCollisionItems?: CollisionItem[];
    @transient private lastIsStatic?: boolean;
    @transient private lastIsTrigger?: boolean;
    @transient private lastX?: number;
    @transient private lastY?: number;
    @transient private lastW?: number;
    @transient private lastH?: number;
    @transient bodyWasUpdated: boolean = false;
    @transient collidingWith = new Set<ColliderComponent>();
    @transient collidingWithPrev = new Set<ColliderComponent>();
    @transient scaleX?: number;
    @transient scaleY?: number;

    postLoad() {
        this.system = this.world.singletons.CollisionSystem as CollisionSystem;
    }

    destroy() {
        this.destroyBodies();
    }

    private destroyBodies() {
        if (this.bodies) {
            const system = this.system.system;
            for (const body of this.bodies)
                system.remove(body);
            delete this.bodies;
            delete this.lastCollisionItems;
        }
    }

    protected abstract getCollisionItems(): CollisionItem[] | null;

    protected recalculateScale(): void {
    }

    protected doUpdateBodies() {
        const items = this.getCollisionItems();
        if (!items) {
            this.destroyBodies();
            return;
        }
        if (items === this.lastCollisionItems &&
            this.isStatic === this.lastIsStatic &&
            this.isTrigger === this.lastIsTrigger &&
            this.entity.transform!.w === this.lastW &&
            this.entity.transform!.h === this.lastH)
            return;

        this.destroyBodies();

        const system = this.system.system;
        this.lastCollisionItems = items;
        this.lastIsStatic = this.isStatic;
        this.lastIsTrigger = this.isTrigger;
        this.lastW = this.entity.transform!.w;
        this.lastH = this.entity.transform!.h;

        this.recalculateScale();

        const {x, y} = this.entity.transform!;
        this.bodies = items.map(item => createBody(system, item, x, y, this));
        for (const body of this.bodies)
            (body as any).component = this;
        this.lastX = x;
        this.lastY = y;
    }

    private doUpdateBodyPositions() {
        if (!this.bodies || !this.lastCollisionItems)
            return;
        const {x, y} = this.entity.transform!;
        if (this.lastX === x && this.lastY === y)
            return;
        const n = this.bodies.length;
        const scaleX = this.scaleX || 1;
        const scaleY = this.scaleY || 1;
        for (let i = 0; i < n; i++) {
            this.bodies[i].pos.x = scaleX * (this.lastCollisionItems[i].x || 0) + x;
            this.bodies[i].pos.y = scaleY * (this.lastCollisionItems[i].y || 0) + y;
        }
        this.lastX = x;
        this.lastY = y;
    }

    beforeCollisionUpdate() {
        this.doUpdateBodies();

        if (this.bodies)
            this.updateBodyImmediate();

        if (this.collidingWith.size > 0 || this.collidingWithPrev.size > 0) {
            this.collidingWithPrev = this.collidingWith;
            this.collidingWith = new Set<ColliderComponent>();
        }
    }

    afterCollisionUpdate() {
        for (const collider of this.collidingWithPrev) {
            if (!this.collidingWith.has(collider)) {
                for (const component of this.entity.getAllComponents())
                    (component as any).onExitCollision?.(collider);
            }
        }
    }

    onCollision(otherCollider: ColliderComponent|undefined, response: Response) {
        if (otherCollider) {
            this.collidingWith.add(otherCollider);
            if (!this.collidingWithPrev.has(otherCollider)) {
                for (const component of this.entity.getAllComponents())
                    (component as any).onEnterCollision?.(otherCollider, response);
            }
        }
        if (!this.isStatic && this.isSolid && (!otherCollider || otherCollider.isSolid)) {
            this.entity!.transform!.x -= response.overlapV.x;
            this.entity!.transform!.y -= response.overlapV.y;
            this.updateBodyImmediate();
        }
    }

    updateBodyImmediate() {
        if (this.bodies) {
            this.doUpdateBodyPositions();

            const system = this.system.system;
            for (const body of this.bodies)
                system.updateBody(body);
            this.bodyWasUpdated = true;
        }
    }
}
