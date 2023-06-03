import {Component, registerNamedComponent} from "../entity/component";
import {Player} from "./player";
import {SpriteColliderComponent} from "../collision/sprite_collider_component";
import {Sprite} from "../entity/sprite";

export class BarrierComponent extends Component {
    static typeName = 'barrier';
    gameFlagName: string = '';
    isInverse: boolean = false;
    minY: number = 0;
    maxY: number = 0;


    update(delta: number) {
        const flag = !!this.world.getSingleton(Player).globalData.get(this.gameFlagName);
        const targetY = flag !== this.isInverse ? this.minY : this.maxY;
        const currY = this.entity.transform!.y;
        if (targetY !== currY) {
            const moveAmount = Math.min(20, Math.abs(targetY - currY));
            this.entity.transform!.y += Math.sign(targetY - currY) * moveAmount;
        }
        this.entity.getComponent(SpriteColliderComponent).isSolid = this.entity.transform!.y !== this.minY;
        this.entity.getComponent(Sprite).layer = this.entity.transform!.y !== this.minY || this.isInverse ? (this.isInverse ? 1 : 2) : 3;
    }
}
registerNamedComponent(BarrierComponent);
