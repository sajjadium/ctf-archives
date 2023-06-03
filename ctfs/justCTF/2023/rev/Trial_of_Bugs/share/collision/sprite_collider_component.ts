import {registerNamedComponent} from "../entity/component";
import {CollisionItem} from "./collision_data";
import {transient} from "../util/transient";
import {Sprite} from "../entity/sprite";
import {ColliderComponent} from "./collider_component";

export class SpriteColliderComponent extends ColliderComponent {
    static typeName = 'sprite_collider';

    @transient private sprite!: Sprite;

    getDependencies(): string[] {
        return ['sprite'];
    }

    postLoad() {
        super.postLoad();
        this.sprite = this.entity.getComponent(Sprite);
    }

    protected getCollisionItems(): CollisionItem[] | null {
        const {spritesheetData, sprite} = this.sprite;
        if (!spritesheetData || !sprite || !spritesheetData.spriteCollisionItems[sprite])
            return null;
        return spritesheetData.spriteCollisionItems[sprite];
    }

    protected recalculateScale() {
        const {spritesheetData, sprite} = this.sprite;
        if (!spritesheetData || !sprite || !spritesheetData.spriteCollisionItems[sprite])
            return 1;
        this.scaleX = this.entity.transform!.w / (spritesheetData.sprites[sprite][2] - spritesheetData.sprites[sprite][0]);
        this.scaleY = this.entity.transform!.h / (spritesheetData.sprites[sprite][3] - spritesheetData.sprites[sprite][1]);
    }
}
registerNamedComponent(SpriteColliderComponent);
