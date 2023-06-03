import {Component, registerNamedComponent} from "../entity/component";
import {ColliderComponent} from "../collision/collider_component";
import {PlayerDeathComponent} from "./player_death_component";
import {MapEntityLoader} from "../map/map_entity_loader";

export class PlayerTpAreaComponent extends Component {
    static typeName = 'player_tp_area';

    pointName: string = '';

    onEnterCollision(target: ColliderComponent) {
        const component = target.entity.tryGetComponent(PlayerDeathComponent);
        if (component) {
            const loader = this.world.getSingleton(MapEntityLoader);
            loader.manager.requestEnterByPoint(this.world.name, loader.mapMeta.name, this.pointName);
        }
    }
}
registerNamedComponent(PlayerTpAreaComponent);
