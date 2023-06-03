import {bothExecute, RpcSingleton} from "../net/rpc";
import {
    EMPTY_TILESET,
    INVALID_MAP,
    MapFullData,
    MapMetaData,
    TilesetData
} from "./map_data";
import {NetInterface} from "../net/net_interface";
import {MapEntityLoader} from "./map_entity_loader";
import {World} from "../entity/world";
import {ComponentRegistry} from "../entity/component";
import {Transform} from "../entity/transform";
import {MapViewZoneComponent} from "./map_view_zone_component";
import {Entity} from "../entity/entity";
import {CameraComponent} from "./camera_component";
import {CameraEntityLocator, PlayerEntityLocator} from "./entity_locators";
import {SpritesheetDataManager} from "./spritesheet_data";
import {PlayerMovementComponent} from "../game/player_movement_component";
import {Sprite} from "../entity/sprite";
import {PlayerInteractionComponent} from "../game/player_interaction_component";
import {GamePersistenceManager} from "../game/game_persistence_manager";
import {SpriteColliderComponent} from "../collision/sprite_collider_component";
import {CollisionSystem} from "../collision/collision_system";
import {PlayerDeathComponent} from "../game/player_death_component";

export const TICK_RATE = 60;
export const TICK_IN_FUTURE_LEEWAY = 10;
export const MAX_TICKS_BEHIND = TICK_RATE * 3;
export const CLIENT_MAX_TICKS_PER_RENDER = 3;

type WorldInfo = {
    world: World,
    loader: MapEntityLoader,
    player: Entity,
    camera: CameraComponent,
    teleportTmpEntity?: Entity,
    teleportTmpViewZone?: Entity
};

export class MapManager extends RpcSingleton {
    mapFullData: {[map: string]: MapFullData};
    tilesets: {[name: string]: TilesetData};
    persistence?: GamePersistenceManager;

    componentRegistry: ComponentRegistry;
    worlds: {[name: string]: WorldInfo} = {};
    clientLoadedTilesets = new Set<string>();
    clientLoadedSpritesheets = new Set<string>();

    targetWorldName: string|null = null;
    currentWorldName: string = INVALID_MAP.name;
    rendererSingleton: any = null;
    inputManagerSingleton: any = null;
    scriptManagerSingleton: any = null;
    eventSystemSingleton: any = null;
    playerSingleton: any = null;

    spritesheetData = new SpritesheetDataManager();
    baseSpritesheets: string[] = [];

    private peerStartTime: Date = new Date();
    private peerTickCount: number = 0;
    enforceTickRate: boolean = true;

    private finishEnterSent: boolean = false;

    constructor(net: NetInterface, componentRegistry: ComponentRegistry, tilesets: {[name: string]: TilesetData}) {
        super(net);
        this.componentRegistry = componentRegistry;
        this.tilesets = tilesets;
        this.mapFullData = {};
        this.targetWorldName = null;
        this.createDefaultWorld();
    }

    private createDefaultWorld() {
        const world = new World(INVALID_MAP.name, this.componentRegistry);
        world.defaultComponents.push(Transform);

        const loader = new MapEntityLoader(this, world, INVALID_MAP, EMPTY_TILESET);
        world.addSingleton(loader);

        const player = world.newEntity();

        const camera = world.newEntity();
        const cameraComponent = camera.addComponent(CameraComponent);
        camera.addComponent(MapViewZoneComponent);
        world.addSingleton(new PlayerEntityLocator(player));

        this.worlds[INVALID_MAP.name] = {world, loader, player, camera: cameraComponent};
    }

    get currentWorld() {
        return this.worlds[this.currentWorldName];
    }

    get targetWorld() {
        if (this.targetWorldName !== null)
            return this.worlds[this.targetWorldName];
        return null;
    }

    get invalidWorld() {
        return this.worlds[INVALID_MAP.name];
    }

    requestEnterByPoint(worldName: string, mapName: string, pointName: string) {
        this.net.rpc.runServerOnly(() => {
            this.enter(worldName, this.mapFullData[mapName].meta, this.mapFullData[mapName].points[pointName]);
        });
    }

    @bothExecute({clientSync: true})
    enter(worldName: string, mapMeta: MapMetaData, position: {x: number, y: number}) {
        const VIEW_W = 1920;
        const VIEW_H = 1080;
        const PLAYER_W = 50; // TODO:
        const PLAYER_H = 78;

        if (worldName === this.currentWorldName) {
            const world = this.currentWorld.world;

            this.currentWorld.teleportTmpEntity?.delete();
            this.currentWorld.teleportTmpViewZone?.delete();

            const tmpEntity = world.newEntity();
            tmpEntity.transform!.w = PLAYER_W;
            tmpEntity.transform!.h = PLAYER_H;
            tmpEntity.transform!.x = position.x - tmpEntity.transform!.w / 2;
            tmpEntity.transform!.y = position.y - tmpEntity.transform!.h / 2;

            const tmpViewZone = world.newEntity();
            tmpViewZone.transform!.w = VIEW_W;
            tmpViewZone.transform!.h = VIEW_H;
            const cameraComponent = tmpViewZone.addComponent(CameraComponent);
            cameraComponent.target = tmpEntity.transform;
            cameraComponent.update();
            tmpViewZone.addComponent(MapViewZoneComponent).register();

            this.targetWorldName = worldName;
            this.finishEnterSent = false;
            this.currentWorld.teleportTmpEntity = tmpEntity;
            this.currentWorld.teleportTmpViewZone = tmpViewZone;

            return;
        }

        const world = new World(worldName, this.componentRegistry);
        world.addSingleton(this.spritesheetData);

        world.defaultComponents.push(Transform);

        const loader = new MapEntityLoader(this, world, mapMeta, this.tilesets[mapMeta.tileset], this.mapFullData[mapMeta.name]);
        world.addSingleton(loader);

        world.addSingleton(new CollisionSystem(world))

        if (this.rendererSingleton !== null)
            world.addSingleton(this.rendererSingleton);
        if (this.inputManagerSingleton !== null)
            world.addSingleton(this.inputManagerSingleton);
        if (this.scriptManagerSingleton !== null)
            world.addSingleton(this.scriptManagerSingleton);
        if (this.eventSystemSingleton !== null)
            world.addSingleton(this.eventSystemSingleton);
        if (this.playerSingleton !== null)
            world.addSingleton(this.playerSingleton);

        const player = world.newEntity();
        player.transform!.name = "Player";
        player.transform!.w = PLAYER_W;
        player.transform!.h = PLAYER_H;
        player.transform!.x = position.x - player.transform!.w / 2;
        player.transform!.y = position.y - player.transform!.h / 2;
        player.addComponent(PlayerMovementComponent);
        player.addComponent(PlayerDeathComponent);
        player.addComponent(PlayerInteractionComponent);
        const playerSprite = player.addComponent(Sprite);
        playerSprite.spritesheet = 'player';
        playerSprite.sprite = 'stand_down';
        const playerCollider = player.addComponent(SpriteColliderComponent);
        playerCollider.isStatic = false;
        playerCollider.isTrigger = true;
        playerCollider.isTileTrigger = true;
        playerCollider.postLoad();
        player.load({'renderer:player': {}});
        world.addSingleton(new PlayerEntityLocator(player));

        const camera = world.newEntity();
        camera.transform!.w = VIEW_W;
        camera.transform!.h = VIEW_H;
        const cameraComponent = camera.addComponent(CameraComponent);
        cameraComponent.update();
        camera.addComponent(MapViewZoneComponent).register();
        world.addSingleton(new CameraEntityLocator(camera));

        this.worlds[worldName] = {world, loader, player, camera: cameraComponent};
        this.targetWorldName = worldName;
        this.finishEnterSent = false;

        if (!this.net.client)
            loader.requestLoadGlobalEntities();
    }

    @bothExecute({clientSync: true, clientInvokable: true})
    clientTilesetLoaded(tilesetName: string) {
        this.clientLoadedTilesets.add(tilesetName);
    }

    @bothExecute({clientSync: true, clientInvokable: true})
    clientSpritesheetLoaded(spritesheetName: string) {
        this.clientLoadedSpritesheets.add(spritesheetName);
    }

    @bothExecute({clientSync: true})
    finishEnter(worldName: string) {
        if (this.targetWorldName !== worldName)
            return;

        const targetWorldInfo = this.worlds[this.targetWorldName];
        if (targetWorldInfo.teleportTmpEntity) {
            const playerT = targetWorldInfo.player.transform!;
            const targetT = targetWorldInfo.teleportTmpEntity.transform!;
            playerT!.x = targetT!.centerX - playerT.w / 2;
            playerT!.y = targetT!.centerY - playerT.h / 2;
            targetWorldInfo.camera.update();
            targetWorldInfo.teleportTmpViewZone!.delete();
            targetWorldInfo.teleportTmpEntity!.delete();
            delete targetWorldInfo.teleportTmpViewZone;
            delete targetWorldInfo.teleportTmpEntity;
        }
        this.currentWorldName = this.targetWorldName;

        for (const component of targetWorldInfo.player.getAllComponents()) {
            if ((component as any).onPlayerEnter)
                (component as any).onPlayerEnter();
        }
    }

    @bothExecute({clientSync: true})
    loadGlobalEntities(worldName: string, entities: {[id: number]: any}) {
        this.worlds[worldName].loader.onLoadGlobalEntities(entities);
    }

    @bothExecute({clientSync: true})
    loadChunk(worldName: string, x: number, y: number, entities: {[id: number]: any}) {
        this.worlds[worldName].loader.onLoadChunk(x, y, entities);
    }

    @bothExecute({clientSync: true, clientInvokable: true})
    tick() {
        this.net.rpc.runServerOnly(() => {
            this.peerTickCount++;

            const expectedTickInterval = 1000 / TICK_RATE;
            const expectedTickNumber = (new Date().getTime() - this.peerStartTime.getTime()) / expectedTickInterval;
            const maxTickNumber = expectedTickNumber + TICK_IN_FUTURE_LEEWAY;
            if (this.peerTickCount > maxTickNumber && this.enforceTickRate) {
                throw new Error("Client time travelled! [peerTickCount=" + this.peerTickCount + ", maxTickNumber=" + maxTickNumber + "]");
            }

            const minTickNumber =　maxTickNumber - MAX_TICKS_BEHIND;
            if (minTickNumber > this.peerTickCount)
                this.peerTickCount = minTickNumber;
        });

        this.currentWorld.loader.requestChunks();

        // TODO: optimize
        for (const entity of Object.values(this.currentWorld.world.entities)) {
            for (const component of entity.getAllComponents()) {
                if (component.updatePhysics)
                    component.updatePhysics(1.0 / 60);
            }
        }
        this.currentWorld.world.getSingleton(CollisionSystem)?.update();
        for (const entity of Object.values(this.currentWorld.world.entities)) {
            for (const component of entity.getAllComponents()) {
                if (component.update)
                    component.update(1.0 / 60);
            }
        }

        if (this.targetWorldName !== null) {
            const targetWorldInfo = this.worlds[this.targetWorldName];
            targetWorldInfo.loader.requestChunks();

            this.net.rpc.runServerOnly(() => {
                if (targetWorldInfo.loader.canSpawn() &&
                    this.baseSpritesheets.every(x => this.clientLoadedSpritesheets.has(x)) &&
                    this.clientLoadedTilesets.has(targetWorldInfo.loader.mapMeta.tileset) &&
                    targetWorldInfo.loader.mapMeta.spritesheets.every(x => this.clientLoadedSpritesheets.has(x)) &&
                    !this.finishEnterSent) {
                    this.finishEnterSent = true;
                    this.finishEnter(targetWorldInfo.world.name);
                }
            });
        }
    }

    requestValidateState() {
        this.validateState(JSON.stringify(this.currentWorld.world.save()));
    }

    @bothExecute({clientSync: true, clientInvokable: true})
    private validateState(clientState: string) {
        this.net.rpc.runServerOnly(() => {
            const serverState = JSON.stringify(this.currentWorld.world.save());
            if (clientState !== serverState) {
                console.error('State mismatch!\nServer state: ' + serverState + '\nClient state: ' + clientState);
            }
        });
    }
}
