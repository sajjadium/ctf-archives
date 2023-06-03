import {Component, registerNamedComponent} from "../entity/component";
import {ColliderComponent} from "../collision/collider_component";
import {PlayerDeathComponent} from "./player_death_component";

export class PlayerRespawnAreaComponent extends Component {
    static typeName = 'player_respawn_area';

    pointName: string = '';

    onEnterCollision(target: ColliderComponent) {
        const component = target.entity.tryGetComponent(PlayerDeathComponent);
        if (component) {
            component.respawnPoint = this.pointName;
        }
    }
}
registerNamedComponent(PlayerRespawnAreaComponent);
