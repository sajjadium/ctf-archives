import {RendererBase} from "./renderer_base";
import {registerNamedComponent} from "../../../share/entity/component";
import {StaticBuffer} from "../webgl/buffer";
import {quad} from "../geometry_utils";
import {Sprite} from "../../../share/entity/sprite";
import {mat4, vec4} from "gl-matrix";
import {SpritesheetData} from "../../../share/map/spritesheet_data";
import {transient} from "../../../share/util/transient";

const ONES: [number, number, number, number] = [1, 1, 1, 1];

export class SpriteRenderer extends RendererBase {
    static typeName = "renderer:sprite";

    @transient private sprite!: Sprite;
    @transient private vertexBuffer: StaticBuffer|null = null;
    @transient private texCoordBuffer: StaticBuffer|null = null;
    @transient private lastSpriteRect: number[]|null = null;
    @transient protected colorMul?: vec4;

    postLoad() {
        this.vertexBuffer = new StaticBuffer(this.gl, quad(0, 0, 1, 1), 2);
        this.sprite = this.entity.getComponent(Sprite);
    }

    private createTexCoordBuffer(spritesheet: SpritesheetData, rect: number[]) {
        this.texCoordBuffer = new StaticBuffer(this.gl, quad(
            rect[0] / spritesheet.width, rect[1] / spritesheet.height,
            rect[2] / spritesheet.width, rect[3] / spritesheet.height
        ), 2);
        this.lastSpriteRect = [...rect];
    }

    private updateTexCoordBuffer(spritesheet: SpritesheetData, rect: number[]) {
        this.texCoordBuffer!.update(quad(
            rect[0] / spritesheet.width, rect[1] / spritesheet.height,
            rect[2] / spritesheet.width, rect[3] / spritesheet.height
        ));
        this.lastSpriteRect = [...rect];
    }

    private destroyTexCoordBuffer() {
        this.texCoordBuffer?.destroy();
    }

    destroy() {
        this.vertexBuffer?.destroy();
        this.texCoordBuffer?.destroy();
    }

    render() {
        const {gl, transformCtx, programCollection, spritesheetLoader} = this.renderer;

        const spritesheet = this.sprite.spritesheetData;
        const texture = spritesheetLoader.spritesheetTextures[spritesheet?.name || ''];
        if (!spritesheet || !texture || !this.sprite.sprite || !spritesheet.sprites[this.sprite.sprite]) {
            this.destroyTexCoordBuffer();
            return;
        }

        const rect = spritesheet.sprites[this.sprite.sprite];

        if (this.texCoordBuffer === null)
            this.createTexCoordBuffer(spritesheet, rect);

        const lastRect = this.lastSpriteRect!;
        // if (lastRect[0] !== rect[0] || lastRect[1] !== rect[1] || lastRect[2] !== rect[2] || lastRect[3] !== rect[3])
            this.updateTexCoordBuffer(spritesheet, rect);

        transformCtx.scale(this.entity.transform!.w, this.entity.transform!.h);

        const matrix: mat4 = transformCtx.matrix;
        programCollection.simple.bind({
            a_position: this.vertexBuffer!,
            a_texCoord: this.texCoordBuffer!,
            u_colorMul: this.colorMul || ONES,

            u_projMatrix: matrix,
            u_sampler: texture
        });
        gl.drawArrays(gl.TRIANGLES, 0, 6);
    }

    get renderLayer(): number {
        return this.sprite.layer !== undefined ? this.sprite.layer : 1;
    }
}

registerNamedComponent(SpriteRenderer);
