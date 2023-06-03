import {World} from "../entity/world";
import {ColliderComponent} from "./collider_component";
import {SpriteColliderComponent} from "./sprite_collider_component";
import {ShapeColliderComponent} from "./shape_collider_component";
import {Body, System} from "detect-collisions";
import {MapEntityLoader} from "../map/map_entity_loader";
import {MapChunkComponent} from "../map/map_chunk_component";
import {createBody} from "./utils";

export class CollisionSystem {
    readonly world: World;
    readonly system: System;
    private tileBodies: {[key: string]: Body[]} = {};

    constructor(world: World) {
        this.world = world;
        this.system = new System();
    }

    update() {
        const newTiles = new Map<string, [number, number]>();
        const {tileWidth, tileHeight} = this.world.getSingleton(MapEntityLoader).tileset;

        const colliders = [];
        for (const entity of Object.values(this.world.entities)) {
            const collider = entity.tryGetComponent(SpriteColliderComponent) ||
                entity.tryGetComponent(ShapeColliderComponent);
            if (collider)
                colliders.push(collider);
        }

        for (const collider of colliders) {
            if (!collider.bodies || !collider.isTileTrigger)
                continue;
            const entity = collider.entity;
            const tileX1 = Math.floor(entity.transform!.x / tileWidth);
            const tileX2 = Math.ceil((entity.transform!.x + entity.transform!.w) / tileWidth);
            const tileY1 = Math.floor(entity.transform!.y / tileWidth);
            const tileY2 = Math.ceil((entity.transform!.y + entity.transform!.h) / tileHeight);
            for (let x = tileX1; x < tileX2; x++) {
                for (let y = tileY1; y < tileY2; y++)
                    if (!newTiles.has(`${x}.${y}`))
                        newTiles.set(`${x}.${y}`, [x, y]);
            }
        }
        this.updateTiles(newTiles);

        for (const collider of colliders) {
            collider.beforeCollisionUpdate();
        }

        const excludeCollisions = new Set<any>();
        for (const collider of colliders) {
            if (!collider.bodies || !collider.isTrigger)
                continue;

            excludeCollisions.clear();
            collider.bodyWasUpdated = true;
            while (collider.bodyWasUpdated) {
                collider.bodyWasUpdated = false;

                for (const body of collider.bodies) {
                    this.system.checkOne(body, (response) => {
                        if (excludeCollisions.has(response.b))
                            return;
                        excludeCollisions.add(response.b);

                        const componentB = (response.b as any).component as ColliderComponent;
                        collider.onCollision(componentB, response);
                        if (componentB.isPlayerOnlyTrigger && !componentB.isTrigger)
                            componentB.onCollision(collider, response);
                        if (collider.bodyWasUpdated)
                            return true;
                    });
                    if (collider.bodyWasUpdated)
                        break;
                }
            }
        }

        for (const collider of colliders) {
            collider.afterCollisionUpdate();
        }
    }

    private updateTiles(newTiles: Map<string, [number, number]>) {
        const loader = this.world.getSingleton(MapEntityLoader);
        const {chunkWidth, chunkHeight} = loader.mapMeta;
        const {tileWidth, tileHeight} = this.world.getSingleton(MapEntityLoader).tileset;
        const collisionItems = loader.tileset.tileCollisionItems;
        let lastChunkX = NaN, lastChunkY = NaN;
        let chunk: MapChunkComponent|undefined = undefined;
        if (newTiles.size > 16)
            console.log(newTiles.size);
        for (const [posStr, tile] of newTiles.entries()) {
            if (this.tileBodies[posStr])
                continue;

            const chunkX = Math.floor(tile[0] / chunkWidth);
            const chunkY = Math.floor(tile[1] / chunkHeight);
            if (chunkX !== lastChunkX || chunkY !== lastChunkY)
                chunk = loader.mapChunks.get(`${chunkX}.${chunkY}`);
            if (chunk) {
                const tileId = chunk.data[(tile[1] % chunkHeight) * chunkWidth + (tile[0] % chunkWidth)];
                if (collisionItems[tileId]) {
                    const x = tile[0] * tileWidth, y = tile[1] * tileHeight;
                    this.tileBodies[posStr] = collisionItems[tileId].map(item => createBody(this.system, item, x, y, {isStatic: true}));
                }
            }
        }
        for (const posStr of Object.keys(this.tileBodies)) {
            if (!newTiles.has(posStr)) {
                for (const body of this.tileBodies[posStr])
                    this.system.remove(body);
                delete this.tileBodies[posStr];
            }
        }
    }

}
