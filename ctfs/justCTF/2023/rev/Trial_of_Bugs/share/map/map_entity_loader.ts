import {World} from "../entity/world";
import {MapManager} from "./map_manager";
import {MapChunkData, MapFullData, MapMetaData, TilesetData} from "./map_data";
import {Entity} from "../entity/entity";
import {MapChunkComponent} from "./map_chunk_component";
import {Transform} from "../entity/transform";
import "../entity/sprite";
import {PersistentChunkData, PersistentChunkDataMetaWrapper} from "../game/game_persistent_storage";
import {PersistFlag} from "./persist_flag";

type MapViewArea = {
    x: number,
    y: number,
    w: number,
    h: number
}

export const MAP_EPSILON = 0.001;

export class MapEntityLoader {

    readonly manager: MapManager;
    readonly world: World;
    readonly mapMeta: MapMetaData;
    readonly mapFullData?: MapFullData;
    readonly tileset: TilesetData;
    private readonly requestedChunks = new Set<string>();
    private readonly loadedChunks = new Set<string>();
    readonly viewAreas = new Set<MapViewArea>();
    private loadInternalEntityNextId: number = -1000000;
    private globalEntitiesLoaded: boolean = false;
    mapChunks = new Map<string, MapChunkComponent>();

    constructor(manager: MapManager, world: World, mapMeta: MapMetaData, tileset: TilesetData, mapFullData?: MapFullData) {
        this.manager = manager;
        this.world = world;
        this.mapMeta = mapMeta;
        this.tileset = tileset;
        this.mapFullData = mapFullData;
    }

    requestLoadGlobalEntities() {
        const entities: {[id: number]: any} = {};

        // TODO: persist the entities
        for (const entityId of this.mapFullData!.globalEntities)
            entities[entityId] = this.mapFullData!.entities[entityId];

        this.manager.loadGlobalEntities(this.world.name, entities);
    }

    requestChunks() {
        const {tileWidth, tileHeight} = this.tileset;
        const {chunkWidth, chunkHeight} = this.mapMeta;
        const chunkWidthPx = chunkWidth * tileWidth, chunkHeightPx = chunkHeight * tileHeight;
        const chunksToLoad = new Set<string>();
        for (const viewArea of this.viewAreas) {
            const startX = Math.floor(viewArea.x / chunkWidthPx);
            const startY = Math.floor(viewArea.y / chunkHeightPx);
            const endX = Math.ceil((viewArea.x + viewArea.w) / chunkWidthPx);
            const endY = Math.ceil((viewArea.y + viewArea.h) / chunkHeightPx);
            for (let i = startX; i < endX; i++) {
                for (let j = startY; j < endY; j++)
                    chunksToLoad.add(`${i}.${j}`);
            }
        }

        // Only server can load chunks as client does not have this data, but both parties must agree on unload at the
        // same time.
        this.manager.net.rpc.runServerOnly(() => {
            if (this.mapFullData) {
                for (const chunk of chunksToLoad) {
                    if (chunk in this.mapFullData.chunks && !this.requestedChunks.has(chunk)) {
                        this.requestedChunks.add(chunk);

                        const chunkData = this.mapFullData.chunks[chunk];
                        if (this.manager.persistence) {
                            this.manager.persistence.loadChunk(this.world.name, chunkData.x, chunkData.y,
                                (persistentData) => this.requestLoadChunk(chunkData, persistentData));
                        } else {
                            this.requestLoadChunk(chunkData, null);
                        }
                    }
                }
            }
        });

        for (const chunk of this.loadedChunks) {
            if (!chunksToLoad.has(chunk)) {
                const [x, y] = chunk.split('.');
                this.unloadChunk(parseInt(x), parseInt(y));
            }
        }
    }

    canSpawn() {
        return this.requestedChunks.size === this.loadedChunks.size && this.globalEntitiesLoaded;
    }

    private requestLoadChunk(chunk: MapChunkData, persistentData: PersistentChunkData|null) {
        const entities: {[id: number]: any} = {};

        for (const [layerName, data] of Object.entries(chunk.tiles)) {
            const chunkTWidth = this.mapMeta.chunkWidth * this.tileset.tileWidth;
            const chunkTHeight = this.mapMeta.chunkHeight * this.tileset.tileHeight;

            entities[this.loadInternalEntityNextId--] = {
                [Transform.typeName]: {
                    name: "Tiles (" + layerName + " " + chunk.x + " " + chunk.y + ")",
                    x: chunk.x * chunkTWidth,
                    y: chunk.y * chunkTHeight,
                    w: chunkTWidth,
                    h: chunkTHeight
                },
                [MapChunkComponent.typeName]: {
                    data
                },
                'renderer:map_chunk': {}
            };
        }

        if (persistentData) {
            Object.assign(entities, persistentData.entities);
        }

        if (chunk.entities) {
            for (const entityId of chunk.entities) {
                if (!(entityId in entities))
                    entities[entityId] = this.mapFullData!.entities[entityId];
            }
        }

        for (const [entityId, entityData] of Object.entries(entities)) {
            if (entityData === null)
                delete (entities as any)[entityId];
        }

        this.manager.loadChunk(this.world.name, chunk.x, chunk.y, entities);
    }

    onLoadGlobalEntities(entities: {[id: number]: any}) {
        for (const [entityId, entityData] of Object.entries(entities)) {
            const entity = new Entity(this.world, parseInt(entityId));
            this.world.entities[entity.id] = entity;
            entity.load(entityData);
        }
        this.globalEntitiesLoaded = true;
    }

    onLoadChunk(x: number, y: number, entities: {[id: number]: any}) {
        if (this.manager.net.client)
            console.log('Loaded chunk: ' + x + ' ' + y);
        this.loadedChunks.add(`${x}.${y}`);

        for (const [entityId, entityData] of Object.entries(entities)) {
            if (this.world.entities[parseInt(entityId)])
                continue;

            const entity = new Entity(this.world, parseInt(entityId));
            this.world.entities[entity.id] = entity;
            entity.load(entityData);

            const chunk = entity.tryGetComponent(MapChunkComponent);
            if (chunk)
                this.mapChunks.set(`${x}.${y}`, chunk);
        }
    }

    private findEntitiesInChunk(x: number, y: number) {
        const chunkTWidth = this.mapMeta.chunkWidth * this.tileset.tileWidth;
        const chunkTHeight = this.mapMeta.chunkHeight * this.tileset.tileHeight;

        const chunkLeft = x * chunkTWidth, chunkRight = chunkLeft + chunkTWidth;
        const chunkTop = y * chunkTHeight, chunkBottom = chunkTop + chunkTHeight;

        // Find entities within the given chunk
        const chunkEntities: Entity[] = [];
        for (const entity of Object.values(this.world.entities)) {
            if (entity.transform!.x + entity.transform!.w > chunkLeft &&
                entity.transform!.y + entity.transform!.h > chunkTop &&
                entity.transform!.x < chunkRight &&
                entity.transform!.y < chunkBottom) {
                if (entity.tryGetComponent(PersistFlag)) {
                    if (entity!.transform!.centerX < chunkLeft || entity!.transform!.centerY < chunkTop ||
                        entity!.transform!.centerX >= chunkRight || entity!.transform!.centerY >= chunkBottom)
                        continue;
                }

                chunkEntities.push(entity);
            }
        }

        return chunkEntities;
    }

    private getChunkSaveData(x: number, y: number, entities: Entity[]): PersistentChunkData {
        const saveData: {[id: number]: any} = {};

        for (const entity of entities) {
            if (entity.tryGetComponent(PersistFlag))
                saveData[entity.id] = entity.save();
        }

        const mapEntities = this.mapFullData?.chunks[`${x}.${y}`]?.entities;
        if (mapEntities) {
            for (const entityId of mapEntities) {
                if (!this.mapFullData!.entities[entityId].hasOwnProperty('persist_flag'))
                    continue;
                if (!(entityId in saveData))
                    saveData[entityId] = null;
            }
        }

        return {entities: saveData};
    }

    private unloadChunk(x: number, y: number) {
        if (this.manager.net.client)
            console.log('Unloading chunk: ' + x + ' ' + y);

        const {tileWidth, tileHeight} = this.tileset;
        const {chunkWidth, chunkHeight} = this.mapMeta;
        const chunkWidthPx = chunkWidth * tileWidth, chunkHeightPx = chunkHeight * tileHeight;
        const chunkEntities = this.findEntitiesInChunk(x, y);

        this.manager.net.rpc.runServerOnly(() => {
            const saveData = this.getChunkSaveData(x, y, chunkEntities);
            this.manager.persistence?.saveChunk(this.world.name, x, y, saveData);
        });

        this.loadedChunks.delete(`${x}.${y}`);

        const deleteEntities = [];
        for (const entity of chunkEntities) {
            if (entity.tryGetComponent(PersistFlag)) {
                deleteEntities.push(entity);
                continue;
            }

            const transform = entity.transform!;
            const x1 = Math.floor(transform.x / chunkWidthPx), y1 = Math.floor(transform.y / chunkHeightPx);
            const x2 = Math.floor((transform.x + transform.w - MAP_EPSILON) / chunkWidthPx), y2 = Math.floor((transform.y + transform.h - MAP_EPSILON) / chunkHeightPx);
            let doNotDelete = false;
            for (let tx = x1; !doNotDelete && tx <= x2; tx++) {
                for (let ty = y1; ty <= y2; ty++) {
                    if (this.loadedChunks.has(`${tx}.${ty}`)) {
                        doNotDelete = true;
                        break;
                    }
                }
            }
            if (!doNotDelete) {
                deleteEntities.push(entity);
            }
        }
        for (const entity of deleteEntities)
            entity.delete();

        this.mapChunks.delete(`${x}.${y}`);
        this.requestedChunks.delete(`${x}.${y}`);
    }

    getSaveData(result: PersistentChunkDataMetaWrapper[]) {
        for (const chunk of this.loadedChunks) {
            const [xs, ys] = chunk.split('.');
            const x = parseInt(xs), y = parseInt(ys);
            const entities = this.findEntitiesInChunk(x, y);
            const data = this.getChunkSaveData(x, y, entities);
            result.push({worldName: this.world.name, x, y, data});
        }
    }

    getTileAt(x: number, y: number): number {
        x = Math.floor(x / this.tileset.tileWidth);
        y = Math.floor(y / this.tileset.tileWidth);
        const chunkName = Math.floor(x / this.mapMeta.chunkWidth) + '.' + Math.floor(y / this.mapMeta.chunkHeight);
        const chunk = this.mapChunks.get(chunkName);
        if (!chunk)
            return -1;
        return chunk.data[(y % this.mapMeta.chunkHeight) * this.mapMeta.chunkWidth + (x % this.mapMeta.chunkWidth)];
    }

    hasChunkAt(x: number, y: number): boolean {
        x = Math.floor(x / this.tileset.tileWidth);
        y = Math.floor(y / this.tileset.tileWidth);
        const chunkName = Math.floor(x / this.mapMeta.chunkWidth) + '.' + Math.floor(y / this.mapMeta.chunkHeight);
        return this.loadedChunks.has(chunkName);
    }
}
