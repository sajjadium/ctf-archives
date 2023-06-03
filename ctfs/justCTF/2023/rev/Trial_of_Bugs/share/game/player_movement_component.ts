import {Component, registerNamedComponent} from "../entity/component";
import {InputManager} from "../input/input_manager";
import {GameKey} from "../input/game_keys";
import {MapEntityLoader} from "../map/map_entity_loader";
import {PlayerDeathComponent} from "./player_death_component";
import {Player} from "./player";
import {transient} from "../util/transient";
import {Sprite} from "../entity/sprite";

export const DEATH_TILE_ID = 16;

export class PlayerMovementComponent extends Component {
    static typeName = 'player_movement';

    @transient accel: number = 0;
    @transient walkAngle: number|null = null;
    @transient spriteBaseName = 'walk_down';
    @transient spriteTime = 0;

    updatePhysics(delta: number) {
        if (this.entity.getComponent(PlayerDeathComponent).dying !== -1)
            return;

        const dialogue = this.world.getSingleton(Player).dialogue;

        const input = this.world.getSingleton(InputManager);
        let dx = 0, dy = 0;
        if (input.primary.pressed[GameKey.MoveUp])
            dy -= 1;
        if (input.primary.pressed[GameKey.MoveDown])
            dy += 1;
        if (input.primary.pressed[GameKey.MoveLeft])
            dx -= 1;
        if (input.primary.pressed[GameKey.MoveRight])
            dx += 1;
        if (dialogue.dialogueInfo.get() !== null || dialogue.choiceInfo.get() !== null)
            dx = dy = 0;
        let dd = Math.sqrt(dx * dx + dy * dy);
        if (dd != 0) {
            dx /= dd;
            dy /= dd;
        }
        const angle = dx != 0 || dy != 0 ? Math.atan2(dy, dx) : null;
        if (angle === null) {
            this.accel = 0;
        } else if (this.walkAngle !== null) {
            const angleDiff = Math.min(Math.abs(angle - this.walkAngle), 2 * Math.PI - Math.abs(angle - this.walkAngle));
            if (angleDiff >= Math.PI * 0.9)
                this.accel = 0;
        }

        this.accel = Math.min(this.accel + 1, 4);
        this.walkAngle = angle;

        const newX = Math.round(this.entity.transform!.x + this.accel * dx);
        const newY = Math.round(this.entity.transform!.y + this.accel * dy);
        const w = this.entity.transform!.w;
        const h = this.entity.transform!.h;

        const sprite = this.entity.getComponent(Sprite);
        let spriteBaseName = this.spriteBaseName;
        if (dy > 0)
            spriteBaseName = 'walk_down';
        else if (dy < 0)
            spriteBaseName = 'walk_up';
        if (dx > 0)
            spriteBaseName = 'walk_right';
        else if (dx < 0)
            spriteBaseName = 'walk_left';
        if (dx === 0 && dy === 0) {
            spriteBaseName = {
                'walk_left': 'stand_left',
                'walk_right': 'stand_right',
                'walk_up': 'stand_up',
                'walk_down': 'stand_down'
            }[this.spriteBaseName] || spriteBaseName;
        }
        if (spriteBaseName !== this.spriteBaseName) {
            this.spriteBaseName = spriteBaseName;
            this.spriteTime = 0;
        }
        let spriteInfo = {
            'walk_left': {frames: 4, frameSwitch: 0.1},
            'walk_right': {frames: 4, frameSwitch: 0.1},
            'walk_up': {frames: 4, frameSwitch: 0.1},
            'walk_down': {frames: 4, frameSwitch: 0.1},
        }[spriteBaseName];
        if (spriteInfo)
            sprite.sprite = spriteBaseName + '_' + (Math.floor(this.spriteTime / spriteInfo.frameSwitch) % spriteInfo.frames);
        else
            sprite.sprite = spriteBaseName;
        this.spriteTime += delta;

        const loader = this.world.getSingleton(MapEntityLoader);
        if (!loader.hasChunkAt(newX, newY) ||
            !loader.hasChunkAt(newX + w, newY) ||
            !loader.hasChunkAt(newX, newY + h) ||
            !loader.hasChunkAt(newX + w, newY + h))
            return;

        this.entity.transform!.x = newX;
        this.entity.transform!.y = newY;

        const tile = loader.getTileAt(this.entity.transform!.centerX, this.entity.transform!.y + this.entity.transform!.h * 0.9);
        if (tile === DEATH_TILE_ID)
            this.entity.getComponent(PlayerDeathComponent).stepOnDeathTile();
    }

    teleportToPoint(pointName: string) {
        const loader = this.world.getSingleton(MapEntityLoader);
        loader.manager.requestEnterByPoint(this.world.name, loader.mapMeta.name, pointName);
    }
}
registerNamedComponent(PlayerMovementComponent);
