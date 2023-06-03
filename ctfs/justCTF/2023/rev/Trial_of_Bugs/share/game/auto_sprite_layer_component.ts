import {Component, registerNamedComponent} from "../entity/component";
import {Sprite} from "../entity/sprite";
import {PlayerEntityLocator} from "../map/entity_locators";

export class AutoSpriteLayerComponent extends Component {
    static typeName = 'auto_sprite_layer';
    offsetY: number = 0;


    update(delta: number) {
        const playerTransform = this.world.getSingleton(PlayerEntityLocator).entity.transform!;
        const playerY = playerTransform.y + playerTransform.h * 0.9;
        this.entity.getComponent(Sprite).layer = playerY >= this.entity.transform!.y + this.offsetY ? 1 : 3;
    }
}
registerNamedComponent(AutoSpriteLayerComponent);
