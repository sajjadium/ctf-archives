import {Component, registerNamedComponent} from "../entity/component";
import {ColliderComponent} from "../collision/collider_component";
import {PlayerDeathComponent} from "./player_death_component";

export class PlayerNoDeathAreaComponent extends Component {
    static typeName = 'player_no_death_area';

    onEnterCollision(target: ColliderComponent) {
        const component = target.entity.tryGetComponent(PlayerDeathComponent);
        if (component) {
            component.noDeathCounter++;
        }
    }

    onExitCollision(target: ColliderComponent) {
        const component = target.entity.tryGetComponent(PlayerDeathComponent);
        if (component) {
            component.noDeathCounter--;
        }
    }
}
registerNamedComponent(PlayerNoDeathAreaComponent);
