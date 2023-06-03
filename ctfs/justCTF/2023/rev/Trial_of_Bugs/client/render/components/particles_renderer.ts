import {RendererBase} from "./renderer_base";
import {registerNamedComponent} from "../../../share/entity/component";
import {StaticBuffer} from "../webgl/buffer";
import {quad} from "../geometry_utils";
import {mat4} from "gl-matrix";
import {SpritesheetData} from "../../../share/map/spritesheet_data";
import {transient} from "../../../share/util/transient";
import {Particles} from "../../../share/entity/particles";

const ONES: [number, number, number, number] = [1, 1, 1, 1];
const EMPTY_COLOR = Array(6 * 4).fill(0);

const PARTICLE_COUNT = 100;

type ParticleInfo = {
    x: number,
    y: number,
    sprite: string,
    velX: number
    velY: number
    accelY: number,
    accelX: number,
    mulY: number,
    mulX: number,
    lifetime: number
}

export class ParticlesRenderer extends RendererBase {
    static typeName = "renderer:particles";

    @transient private component!: Particles;
    @transient private particles: ParticleInfo[] = [];
    @transient private vertexBuffer: StaticBuffer|null = null;
    @transient private texCoordBuffer: StaticBuffer|null = null;
    @transient private colorBuffer: StaticBuffer|null = null;
    @transient private lastTime: number = 0;
    @transient private spawnTimeSum: number = 0;
    @transient private nextSpawnTime: number = 0;

    postLoad() {
        this.component = this.entity.getComponent(Particles);
        const particleCount = this.component.particleMaxCount;
        this.vertexBuffer = new StaticBuffer(this.gl, Array(particleCount).fill(quad(0, 0, 0, 0)).flat(), 2, {dynamicDraw: true});
        this.texCoordBuffer = new StaticBuffer(this.gl, Array(particleCount).fill(quad(0, 0, 0, 0)).flat(), 2, {dynamicDraw: true});
        this.colorBuffer = new StaticBuffer(this.gl, Array(6 * particleCount).fill([0, 0, 0, 0]).flat(), 4, {dynamicDraw: true});

        this.lastTime = performance.now();
        this.spawnTimeSum = 0;
        this.nextSpawnTime = Math.random() * (2 * (1000 / this.component.particleSpawnPerSecond));

        this.particles = [];
        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: 0,
                y: 0,
                sprite: '',
                velX: 0,
                velY: 0,
                accelX: 0,
                accelY: 0,
                mulX: 0,
                mulY: 0,
                lifetime: 0
            });
        }
    }

    private updateParticles(spritesheet: SpritesheetData, delta: number) {
        const newVertexBufferData = Array(this.particles.length);
        const newTexCoordBufferData = Array(this.particles.length);
        const newColorBufferData = Array(this.particles.length);

        this.spawnTimeSum += delta;
        let timeSum = this.spawnTimeSum;
        let spawnCount = 0;
        while (this.spawnTimeSum > this.nextSpawnTime) {
            spawnCount++;
            this.spawnTimeSum -= this.nextSpawnTime;
            this.nextSpawnTime = Math.random() * (2 * (1000 / this.component.particleSpawnPerSecond));
        }

        const maxLifetime = this.component.particleLifetime;
        const {particleColorStart, particleColorEnd} = this.component;

        for (let i = 0; i < this.particles.length; i++) {
            const p = this.particles[i];
            p.x += p.velX * delta / 1000;
            p.y += p.velY * delta / 1000;
            p.velX += p.accelX * delta / 1000;
            p.velY += p.accelY * delta / 1000;
            p.velX *= p.mulX;
            p.velY *= p.mulY;
            p.lifetime -= delta;

            if (p.lifetime <= 0 && spawnCount > 0) {
                spawnCount = 0;
                p.x = Math.random() * (this.entity.transform!.w);
                p.y = Math.random() * (this.entity.transform!.h);
                p.velX = this.component.particleMinVelX + Math.random() * (this.component.particleMaxVelX - this.component.particleMinVelX);
                p.velY = this.component.particleMinVelY + Math.random() * (this.component.particleMaxVelY - this.component.particleMinVelY);
                p.accelX = this.component.particleAccelX;
                p.accelY = this.component.particleAccelY;
                p.mulX = this.component.particleMulX;
                p.mulY = this.component.particleMulY;
                p.lifetime = this.component.particleLifetime + Math.random() * timeSum;

                const sprites = this.component.particleSprite.split(',');
                p.sprite = sprites[Math.floor(Math.random() * sprites.length)];
            }

            if (p.lifetime <= 0) {
                newVertexBufferData[i] = quad(0, 0, 0, 0);
                newTexCoordBufferData[i] = quad(0, 0, 0, 0);
                newColorBufferData[i] = EMPTY_COLOR;
                continue;
            }

            const d = (maxLifetime - p.lifetime) / maxLifetime;
            const r = particleColorStart.r + (particleColorEnd.r - particleColorStart.r) * d;
            const g = particleColorStart.g + (particleColorEnd.g - particleColorStart.g) * d;
            const b = particleColorStart.b + (particleColorEnd.b - particleColorStart.b) * d;
            const a = particleColorStart.a + (particleColorEnd.a - particleColorStart.a) * d;

            const rect = spritesheet.sprites[p.sprite];
            newVertexBufferData[i] = quad(p.x, p.y, p.x + (rect[2] - rect[0]), p.y + (rect[3] - rect[1]));
            newTexCoordBufferData[i] = quad(
                rect[0] / spritesheet.width, rect[1] / spritesheet.height,
                rect[2] / spritesheet.width, rect[3] / spritesheet.height
            );
            newColorBufferData[i] = [r, g, b, a, r, g, b, a, r, g, b, a, r, g, b, a, r, g, b, a, r, g, b, a];
        }

        this.vertexBuffer!.update(newVertexBufferData.flat());
        this.texCoordBuffer!.update(newTexCoordBufferData.flat());
        this.colorBuffer!.update(newColorBufferData.flat());
    }

    destroy() {
        this.vertexBuffer?.destroy();
        this.texCoordBuffer?.destroy();
        this.colorBuffer?.destroy();
    }

    render() {
        const {gl, transformCtx, programCollection, spritesheetLoader} = this.renderer;

        const spritesheet = this.component.spritesheetData;
        const texture = spritesheetLoader.spritesheetTextures[spritesheet?.name || ''];
        if (!spritesheet || !texture) {
            return;
        }

        const now = performance.now();
        this.updateParticles(spritesheet, now - this.lastTime);
        this.lastTime = now;

        const matrix: mat4 = transformCtx.matrix;
        programCollection.colored.bind({
            a_position: this.vertexBuffer!,
            a_texCoord: this.texCoordBuffer!,
            a_color: this.colorBuffer!,

            u_projMatrix: matrix,
            u_sampler: texture
        });
        gl.drawArrays(gl.TRIANGLES, 0, 6 * this.particles.length);
    }
}

registerNamedComponent(ParticlesRenderer);
