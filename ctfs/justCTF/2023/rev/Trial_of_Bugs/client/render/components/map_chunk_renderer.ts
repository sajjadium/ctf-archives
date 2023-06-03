import {RendererBase} from "./renderer_base";
import {Texture} from "../webgl/texture";
import {MapChunkComponent} from "../../../share/map/map_chunk_component";
import {MapEntityLoader} from "../../../share/map/map_entity_loader";
import {registerNamedComponent} from "../../../share/entity/component";
import {StaticBuffer} from "../webgl/buffer";
import {quad} from "../geometry_utils";
import {transient} from "../../../share/util/transient";

class MapChunkRenderer extends RendererBase {
    static typeName = "renderer:map_chunk";

    @transient private tilesetName: string|null = null;
    @transient private dataTexture: Texture|null = null;
    @transient private vertexBuffer: StaticBuffer|null = null;
    @transient private texCoordBuffer: StaticBuffer|null = null;

    postLoad() {
        const gl = this.gl;
        const {mapMeta, tileset} = this.world.getSingleton(MapEntityLoader);
        const columns = tileset.columns;

        const chunk = this.entity.getComponent(MapChunkComponent);
        const textureData = new Uint8Array(mapMeta.chunkWidth * mapMeta.chunkHeight * 3);
        const tiles = mapMeta.chunkWidth * mapMeta.chunkHeight;
        for (let i = 0; i < tiles; i++) {
            textureData[3 * i] = chunk.data[i] % columns;
            textureData[3 * i + 1] = Math.floor(chunk.data[i] / columns);
        }

        this.tilesetName = tileset.name;
        this.dataTexture = new Texture(gl, {
            data: textureData,
            width: mapMeta.chunkWidth,
            height: mapMeta.chunkHeight,
            format: gl.RGB
        }, gl.NEAREST);

        this.vertexBuffer = new StaticBuffer(this.gl, quad(0, 0, mapMeta.chunkWidth * tileset.tileWidth, mapMeta.chunkHeight * tileset.tileHeight), 2);
        this.texCoordBuffer = new StaticBuffer(this.gl, quad(0, 0, mapMeta.chunkWidth, mapMeta.chunkHeight), 2);
    }

    destroy() {
        this.dataTexture?.destroy();
        this.vertexBuffer?.destroy();
        this.texCoordBuffer?.destroy();
    }

    render() {
        this.renderer.tilesetResourceManager.drawTileset(this.tilesetName!, this.dataTexture!, this.vertexBuffer!, this.texCoordBuffer!);
    }

    get renderLayer() {
        return 0;
    }
}

registerNamedComponent(MapChunkRenderer);
