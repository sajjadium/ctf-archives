import {registerNamedComponent} from "../../../share/entity/component";
import {SpriteRenderer} from "./sprite_renderer";
import {PlayerDeathComponent} from "../../../share/game/player_death_component";
import {mat4, vec3} from "gl-matrix";
import {MapEntityLoader} from "../../../share/map/map_entity_loader";
import {DEATH_TILE_ID} from "../../../share/game/player_movement_component";

class PlayerRenderer extends SpriteRenderer {
    static typeName = "renderer:player";

    render() {
        const {gl, transformCtx, programCollection, spritesheetLoader} = this.renderer;

        const loader = this.world.getSingleton(MapEntityLoader);
        const tileHeight = loader.tileset.tileHeight;

        const dying = this.entity.getComponent(PlayerDeathComponent).dying;
        if (dying !== -1) {
            const px = this.entity.transform!.centerX;
            const py = this.entity.transform!.y + this.entity.transform!.h * 0.9;

            const ret: [number, number, number] = [0, 0, 0];
            ret[1] = this.entity.transform!.h * 0.9 - py % tileHeight + tileHeight;
            if (loader.getTileAt(px, ret[1] + this.entity.transform!.y) === DEATH_TILE_ID)
                ret[1] += tileHeight;
            vec3.transformMat4(ret, ret, transformCtx.matrix);
            const clipY = (ret[1] + 1) / 2 * gl.canvas.height;

            gl.enable(gl.SCISSOR_TEST);
            gl.scissor(0, clipY, gl.canvas.width, gl.canvas.width - clipY);

            transformCtx.translate(0, dying * 100);
            this.colorMul = [1, 1, 1, 1 - dying];
            super.render();
            delete this.colorMul;

            gl.scissor(0, 0, gl.canvas.width, gl.canvas.height);
            gl.disable(gl.SCISSOR_TEST);
            // gl.scissor(0, 0, 0, 0);
        } else {
            super.render();
        }
    }

    get renderLayer(): number {
        return 3;
    }
}

registerNamedComponent(PlayerRenderer);
