import {Component, registerNamedComponent} from "../entity/component";
import {ColliderComponent} from "../collision/collider_component";
import {PlayerMovementComponent} from "./player_movement_component";
import {Player} from "./player";
import {EVENT_PLAYER_ENTER_AREA} from "../script/event_ids";

export class PlayerEnterAreaComponent extends Component {
    static typeName = 'player_enter_area';
    areaName: string = '';

    onEnterCollision(target: ColliderComponent) {
        if (target.entity.tryGetComponent(PlayerMovementComponent)) {
            this.world.getSingleton(Player).eventSystem.emit(EVENT_PLAYER_ENTER_AREA, {worldName: this.world.name, areaName: this.areaName});
        }
    }
}
registerNamedComponent(PlayerEnterAreaComponent);
