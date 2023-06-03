import {registerNamedComponent} from "../entity/component";
import {CollisionItem} from "./collision_data";
import {ColliderComponent} from "./collider_component";

export class ShapeColliderComponent extends ColliderComponent {
    static typeName = 'shape_collider';

    shape: CollisionItem[] = [];

    protected getCollisionItems(): CollisionItem[] | null {
        return this.shape;
    }
}
registerNamedComponent(ShapeColliderComponent);
