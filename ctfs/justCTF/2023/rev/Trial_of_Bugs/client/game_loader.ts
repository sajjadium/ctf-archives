import {ScriptBlob, ScriptBlobJsGlobal} from "../share/script/blob";
import {TilesetData} from "../share/map/map_data";
import {DownloadGroup} from "./download_group";
import {ScriptComponentMetaFile} from "../share/script/component_meta_data";
import {GameConfig} from "../share/game/game_data";
import {QuestMetaFile} from "../share/quest/quest_data";


export class GameLoader {
    config: GameConfig|null = null;
    scriptBlob: ScriptBlob|null = null;
    protected scriptBlobJsCode?: ScriptBlobJsGlobal;
    scriptComponentMeta?: ScriptComponentMetaFile;
    questMeta?: QuestMetaFile;
    tilesets: {[name: string]: TilesetData}|null = null;

    loadDownload: DownloadGroup|null = null;

    loadAssets(cb: () => void) {
        this.loadDownload = new DownloadGroup(cb);

        this.loadDownload.loadJsonAsset('config.json', (data) => {
            this.config = data;
        });
        this.loadDownload.loadJsonAsset('scriptblob.json', (data) => {
            this.scriptBlob = ScriptBlob.fromJson(data);
            this.scriptBlob.jsCode = this.scriptBlobJsCode;
        });
        this.loadDownload.loadJsAsset('scriptblob.min.js', () => {
            this.scriptBlobJsCode = (window as any).scriptblob_js;
            delete (window as any).scriptblob_js;
            if (this.scriptBlob)
                this.scriptBlob.jsCode = this.scriptBlobJsCode;
        });
        this.loadDownload.loadJsonAsset('scriptcomponents.json', (data) => {
            this.scriptComponentMeta = data;
        });
        this.loadDownload.loadJsonAsset('quests.json', (data) => {
            this.questMeta = data;
        });
        this.loadDownload.loadJsonAsset('tilesets.json', (data) => {
            this.tilesets = data;
        });

        this.loadDownload.finalize();
    }

}
