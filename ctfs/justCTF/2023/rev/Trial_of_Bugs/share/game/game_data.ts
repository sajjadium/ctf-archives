import {ScriptBlob} from "../script/blob";
import {MapFullData, TilesetData} from "../map/map_data";
import {SpritesheetData} from "../map/spritesheet_data";
import {ScriptComponentMetaFile} from "../script/component_meta_data";
import {QuestMetaFile} from "../quest/quest_data";

export type GameConfig = {
    wsUrl: string|string[],
    baseSpritesheets: string[],
    enableDebug?: boolean,
    serverKey?: string|null
}

export class GameData {

    config: GameConfig;
    scriptBlob: ScriptBlob;
    componentMeta: ScriptComponentMetaFile;
    quest: QuestMetaFile;
    tilesets: {[name: string]: TilesetData};
    mapData: {[map: string]: MapFullData}|undefined = undefined;
    spritesheets: {[name: string]: SpritesheetData}|undefined = undefined;

    constructor(config: GameConfig, scriptBlob: ScriptBlob, componentMeta: ScriptComponentMetaFile,
                quest: QuestMetaFile, tilesets: {[name: string]: TilesetData}) {
        this.config = config;
        this.scriptBlob = scriptBlob;
        this.componentMeta = componentMeta;
        this.quest = quest;
        this.tilesets = tilesets;
    }

}
