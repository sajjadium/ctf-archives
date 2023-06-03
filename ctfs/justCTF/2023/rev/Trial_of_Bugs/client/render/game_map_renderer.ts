import {Player} from "../../share/game/player";
import {createProgramCollection, ProgramCollection} from "./shaders";
import {TilesetResourceManager} from "./tileset_resource_manager";
import {RendererBase} from "./components/renderer_base";
import "./components/index";
import {DrawTransformContext} from "./draw_transform_context";
import {mat4} from "gl-matrix";
import {SpritesheetLoader} from "./spritesheet_loader";
import {TickScheduler} from "../tick_scheduler";
import {CLIENT_MAX_TICKS_PER_RENDER, TICK_RATE} from "../../share/map/map_manager";

export class GameMapRenderer {
    gl: WebGLRenderingContext;
    player: Player;
    private stopped: boolean = false;
    transformCtx = new DrawTransformContext();
    programCollection: ProgramCollection;
    tilesetResourceManager: TilesetResourceManager;
    spritesheetLoader: SpritesheetLoader;
    tickScheduler = new TickScheduler(TICK_RATE * 0.9, TICK_RATE);

    constructor(canvas: WebGLRenderingContext, player: Player) {
        this.gl = canvas;
        this.player = player;
        this.programCollection = createProgramCollection(canvas);
        this.tilesetResourceManager = new TilesetResourceManager(canvas, this.transformCtx, player, this.programCollection);
        this.spritesheetLoader = new SpritesheetLoader(canvas, player);

        player.map.rendererSingleton = this;

        this.tickScheduler.reset();
        requestAnimationFrame(() => this.render());
    }

    stop() {
        if (this.player.map.rendererSingleton === this)
            this.player.map.rendererSingleton = null;
        this.stopped = true;
    }

    private render() {
        if (this.stopped)
            return;

        this.gl.canvas.width = (this.gl.canvas.parentNode as HTMLElement).offsetWidth;
        this.gl.canvas.height = (this.gl.canvas.parentNode as HTMLElement).offsetHeight;

        this.tilesetResourceManager.loadTilesets();
        this.tilesetResourceManager.uploadTilesets();
        this.spritesheetLoader.loadSpritesheets();

        const ticks = Math.min(this.tickScheduler.getTickCount(), CLIENT_MAX_TICKS_PER_RENDER);
        for (let i = ticks; i > 0; --i)
            this.player.map.tick();

        //this.player.map.requestValidateState();
        this.player.quest.updateActiveQuests();

        const gl = this.gl;
        gl.clearColor(0.0, 0.0, 0.0, 1.0);
        gl.clear(gl.COLOR_BUFFER_BIT);
        gl.enable(gl.BLEND);
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
        gl.viewport(0, 0, this.gl.canvas.width, this.gl.canvas.height);

        const worldInfo = this.player.map.currentWorld;
        const cameraTransform = worldInfo.camera.entity.transform;
        if (cameraTransform === undefined) {
            requestAnimationFrame(() => this.render());
            return;
        }

        mat4.ortho(this.transformCtx.matrix, 0, cameraTransform.w, cameraTransform.h, 0, -1, 100);
        this.transformCtx.translate(-cameraTransform.x, -cameraTransform.y);

        // TODO: optimize?
        for (let i = 0; i < 4; i++) {
            for (const entity of Object.values(worldInfo.world.entities)) {
                for (const component of entity.getAllComponents()) {
                    if (component instanceof RendererBase && component.renderLayer === i) {
                        this.transformCtx.push();
                        this.transformCtx.applyFromComponent(entity.transform!);
                        component.render();
                        this.transformCtx.pop();
                    }
                }
            }
        }

        requestAnimationFrame(() => this.render());
    }
}
