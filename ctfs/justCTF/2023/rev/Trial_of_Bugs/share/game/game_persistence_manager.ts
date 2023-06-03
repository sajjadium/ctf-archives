import {GamePersistentStorage, PersistentChunkData, PersistentChunkDataMetaWrapper} from "./game_persistent_storage";
import {Mutex} from "async-mutex";
import {MapManager} from "../map/map_manager";
import {DisconnectSource} from "../net/net_interface";

export class GamePersistenceManager {
    private readonly storage: GamePersistentStorage|null;
    private readonly map: MapManager;
    private readonly pendingChunks: {[id: string]: PersistentChunkData} = {};
    private readonly savePlayerDataCallback: () => any;
    private readonly gameSaveMutex = new Mutex();
    private savingVolatileData: number = 0;
    private saveFailed: boolean = false;

    constructor(storage: GamePersistentStorage|null, map: MapManager, savePlayerDataCallback: () => any) {
        this.storage = storage;
        this.map = map;
        this.savePlayerDataCallback = savePlayerDataCallback;
    }

    private getPendingChunkId(worldName: string, x: number, y: number) {
        return `${worldName}/${x}.${y}`;
    }

    disableSavingDueToError() {
        this.saveFailed = true;
    }

    saveGame(): Promise<void> {
        return this.gameSaveMutex.runExclusive(async () => {
            if (this.storage === null)
                return;

            if (this.saveFailed)
                throw new Error('Save failed');

            try {
                // Before actually saving collect everything we want to save.
                const playerData = this.savePlayerDataCallback();
                if (!playerData)
                    return;

                const saveChunks: PersistentChunkDataMetaWrapper[] = [];
                for (const world of Object.values(this.map.worlds)) {
                    world.loader.getSaveData(saveChunks);
                }

                await this.storage.saveChunks(saveChunks);
                await this.storage.saveGame({
                    playerData
                });
            } catch (e) {
                // Do it here as opposed to in the catch handler so we can be sure the other save handlers won't execute.
                this.saveFailed = true;
                throw e;
            }

            console.log('[' + this.storage.toString() + '] Game saved!');
        }).catch((e) => this.reportError(e));
    }

    saveChunk(worldName: string, x: number, y: number, data: PersistentChunkData) {
        const id = this.getPendingChunkId(worldName, x, y);
        this.pendingChunks[id] = data;

        if (this.storage === null)
            return;
        this.lockMutexForVolatile(async () => {
            await this.storage!.saveChunk(worldName, x, y, data);
            if (this.pendingChunks[id] === data)
                delete this.pendingChunks[id];
        }).catch((e) => this.reportError(e));
    }

    loadChunk(worldName: string, x: number, y: number, callback: (data: PersistentChunkData|null) => void) {
        const id = this.getPendingChunkId(worldName, x, y);
        if (id in this.pendingChunks) {
            callback(this.pendingChunks[id]);
            return;
        }

        if (this.storage === null) {
            callback(null);
            return;
        }
        this.lockMutexForVolatile(async () => {
            const data = await this.storage!.loadChunk(worldName, x, y);
            callback(data);
        }).catch((e) => this.reportError(e));
    }

    private async lockMutexForVolatile(cb: () => Promise<void>) {
        if (this.savingVolatileData === 0)
            await this.gameSaveMutex.acquire();
        this.savingVolatileData += 1;
        try {
            if (this.saveFailed)
                throw new Error('Save failed');
            await cb();
        } catch (e) {
            this.saveFailed = true;
            throw e;
        } finally {
            this.savingVolatileData -= 1;
            if (this.savingVolatileData === 0)
                this.gameSaveMutex.release();
        }
    }

    private reportError(e: Error) {
        console.error(e);
        this.map.net.disconnect({source: DisconnectSource.HANDLE_ERROR, handleError: e});
    }

}
