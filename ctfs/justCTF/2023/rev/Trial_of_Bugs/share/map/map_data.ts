import {CollisionItem} from "../collision/collision_data";

export type MapMetaData = {
    name: string,
    tileset: string,
    spritesheets: string[],
    chunkWidth: number,
    chunkHeight: number
}
export type MapChunkData = {
    x: number,
    y: number,
    tiles: {[layer: string]: number[]},
    entities?: number[]
}

export type MapClientData = {
    meta: MapMetaData,
    chunks: {[pos: string]: MapChunkData},
}
export type MapFullData = MapClientData & {
    points: {[name: string]: {x: number, y: number}},
    entities: {[id: number]: any},
    globalEntities: number[]
}

export type TilesetData = {
    name: string,
    count: number,
    columns: number,
    tileWidth: number,
    tileHeight: number,
    tileCollisionItems: CollisionItem[][]
}

export const EMPTY_TILESET: TilesetData = {
    name: 'empty',
    count: 0,
    columns: 1,
    tileWidth: 1,
    tileHeight: 1,
    tileCollisionItems: []
};

export const INVALID_MAP: MapMetaData = {
    name: 'invalid',
    tileset: EMPTY_TILESET.name,
    spritesheets: [],
    chunkWidth: 100,
    chunkHeight: 100
};
