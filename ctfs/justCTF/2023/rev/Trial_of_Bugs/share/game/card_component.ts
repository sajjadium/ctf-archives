import {Component, registerNamedComponent} from "../entity/component";
import {ColliderComponent} from "../collision/collider_component";
import {PlayerMovementComponent} from "./player_movement_component";
import {Player} from "./player";

export class CardComponent extends Component {
    static typeName = 'card';

    canDrop: boolean = false;
    collectOnCollide: boolean = true;
    collectedPosX: number = 0;
    collectedPosY: number = 0;
    shownHint: boolean = false;

    onEnterCollision(target: ColliderComponent) {
        const component = target.entity.tryGetComponent(PlayerMovementComponent);
        if (component) {
            if (this.collectOnCollide) {
                this.entity.transform!.x = this.collectedPosX;
                this.entity.transform!.y = this.collectedPosY;
                this.canDrop = true;

                if (!this.shownHint) {
                    this.entity.world.getSingleton(Player).dialogue.showDialogue(-1, 'Hint', 'You can drop this card anywhere in this room by pressing the Interact button');
                    this.shownHint = true;
                }
            } else {
                this.collectOnCollide = true;
            }
        }
    }
}
registerNamedComponent(CardComponent);
