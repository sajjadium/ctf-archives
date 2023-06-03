import {TilesetLoader} from "./tileset_loader";
import {Texture} from "./webgl/texture";
import {StaticBuffer} from "./webgl/buffer";
import {Player} from "../../share/game/player";
import {quad} from "./geometry_utils";
import {mat4} from "gl-matrix";
import {ProgramCollection} from "./shaders";
import {DrawTransformContext} from "./draw_transform_context";

export class TilesetResourceManager {
    private readonly player: Player;
    private readonly gl: WebGLRenderingContext;
    private readonly transformCtx: DrawTransformContext;
    private readonly programCollection: ProgramCollection;

    private tilesetLoader: TilesetLoader;
    private currentTilesetTexture: Texture|null = null;
    private currentTilesetName: string|null = null;

    constructor(gl: WebGLRenderingContext, transformCtx: DrawTransformContext, player: Player, programCollection: ProgramCollection) {
        this.gl = gl;
        this.transformCtx = transformCtx;
        this.player = player;
        this.tilesetLoader = new TilesetLoader(player);
        this.programCollection = programCollection;
    }

    loadTilesets() {
        const targetWorld = this.player.map.targetWorld;
        if (targetWorld !== null)
            this.tilesetLoader.requestLoadTileset(targetWorld.loader.mapMeta.tileset);

        const currentWorld = this.player.map.currentWorld;
        this.tilesetLoader.requestLoadTileset(currentWorld.loader.mapMeta.tileset);
    }

    uploadTilesets() {
        const currentWorld = this.player.map.currentWorld;
        const currentTileset = currentWorld.loader.mapMeta.tileset;
        if (this.currentTilesetName !== currentTileset &&
            currentTileset in this.tilesetLoader.tilesetImages) {
            this.currentTilesetTexture?.destroy();

            const tilesetInfo = this.player.gameData.tilesets[currentTileset];
            const w = tilesetInfo.tileWidth * tilesetInfo.columns;
            const h = tilesetInfo.tileHeight * (tilesetInfo.count / tilesetInfo.columns);
            this.currentTilesetTexture = new Texture(this.gl, this.tilesetLoader.tilesetImages[currentTileset]);
            this.currentTilesetName = currentTileset;
        }
    }

    drawTileset(tilesetName: string, dataTexture: Texture, vertexBuffer: StaticBuffer, texCoordBuffer: StaticBuffer) {
        if (tilesetName !== this.currentTilesetName)
            return;

        const tilesetInfo = this.player.gameData.tilesets[tilesetName];

        const matrix: mat4 = this.transformCtx.matrix;
        this.programCollection.tile.bind({
            a_position: vertexBuffer,
            a_texCoord: texCoordBuffer,

            u_projMatrix: matrix,
            u_sampler: this.currentTilesetTexture!,
            u_mapDataSampler: dataTexture,
            u_tileCount: [tilesetInfo.columns, tilesetInfo.count / tilesetInfo.columns],
            u_tileSize: [tilesetInfo.tileWidth, tilesetInfo.tileHeight]
        });
        this.gl.drawArrays(this.gl.TRIANGLES, 0, 6);
    }
}
