export type PersistentChunkData = {
    entities: {[id: number]: any};
}

export type PersistentChunkDataMetaWrapper = {
    worldName: string;
    x: number;
    y: number;
    data: PersistentChunkData;
}

export type PersistentData = {
    playerData: any;
}

export interface GamePersistentStorage {
    /**
     * Saves the game and commits volatile chunks.
     */
    saveGame(data: PersistentData): Promise<void>;

    /**
     * Saves the chunk to storage. The chunk is marked as volatile until saveGame is called. Any volatile chunks will
     * be deleted when loading a game using loadGame.
     * The chunk will only be available for reading once the callback is called.
     */
    saveChunk(worldName: string, x: number, y: number, data: PersistentChunkData): Promise<void>;

    /**
     * Same as saveChunk, but with a chunk batch.
     */
    saveChunks(entries: PersistentChunkDataMetaWrapper[]): Promise<void>;

    /**
     * Loads a chunk at the specified coordinates. Volatile chunks will also be returned by this function.
     */
    loadChunk(worldName: string, x: number, y: number): Promise<PersistentChunkData|null>;
}
