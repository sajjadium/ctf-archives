import {Component, registerNamedComponent} from "../entity/component";
import {PlayerEntityLocator} from "./entity_locators";
import {transient} from "../util/transient";
import {Transform} from "../entity/transform";
import {CameraLockComponent} from "./camera_lock_component";

export class CameraComponent extends Component {
    static typeName = 'camera';

    @transient target?: Transform;

    update() {
        const transform = this.entity.transform!;
        const playerTransform = this.target || this.world.getSingleton(PlayerEntityLocator).entity.transform!;

        transform.x = playerTransform.centerX - transform.w / 2;
        transform.y = playerTransform.centerY - transform.h / 2;

        const targetX = playerTransform.centerX, targetY = playerTransform.centerY;

        for (const entity of Object.values(this.world.entities)) {
            for (const component of entity.getAllComponents()) {
                if (component instanceof CameraLockComponent) {
                    const lockTransform = component.entity.transform!;
                    if (lockTransform.containsPoints(targetX, targetY)) {
                        transform.x = Math.max(Math.min(transform.x, lockTransform.x + lockTransform.w - transform.w), lockTransform.x);
                        transform.y = Math.max(Math.min(transform.y, lockTransform.y + lockTransform.h - transform.h), lockTransform.y);
                    }
                }
            }
        }
    }

}
registerNamedComponent(CameraComponent);
