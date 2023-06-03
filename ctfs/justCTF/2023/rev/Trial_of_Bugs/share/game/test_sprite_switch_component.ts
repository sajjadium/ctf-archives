import {Component, registerNamedComponent} from "../entity/component";
import {Sprite} from "../entity/sprite";

export class TestSpriteSwitchComponent extends Component {
    static typeName = 'test_sprite_switch';

    sprites?: {[index: number]: string}; // TODO: do this at map build step
    spriteNo: number = 0;
    switchInterval: number = 1;
    timeToNextSwitch: number = 0;

    postLoad() {
        this.timeToNextSwitch = this.switchInterval;
    }

    update(delta: number) {
        if (!this.sprites)
            return;

        this.timeToNextSwitch -= delta;
        if (this.timeToNextSwitch > 0)
            return;

        const sprite = this.entity.getComponent(Sprite);
        sprite.sprite = this.sprites[this.spriteNo];
        this.spriteNo = this.spriteNo + 1;
        this.timeToNextSwitch = this.switchInterval;
        if (!this.sprites[this.spriteNo])
            this.spriteNo = 0;
    }
}
registerNamedComponent(TestSpriteSwitchComponent);
