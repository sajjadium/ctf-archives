import {DialogueModel} from "./dialogue_model";
import {ScriptManager, ScriptManagerSaveData} from "../script/script_manager";
import {DisconnectInfo, NetInterface} from "../net/net_interface";
import {GameData} from "./game_data";
import {MapManager} from "../map/map_manager";
import {InputManager} from "../input/input_manager";
import {GamePersistentStorage} from "./game_persistent_storage";
import {GamePersistenceManager} from "./game_persistence_manager";
import {Debug} from "./debug";
import {GameComponentRegistry} from "./game_component_registry";
import {EventSystem} from "../event/event_system";
import {QuestManager, QuestSaveData} from "../quest/quest_manager";
import {GameGlobalKVManager, GameGlobalKVSaveData} from "./game_global_kv_manager";
import {FlagRevealManager} from "./flag_reveal_manager";

import "./test_sprite_switch_component";
import "./player_enter_area_component";
import "./player_respawn_area_component";
import "./player_no_death_area_component";
import "./player_tp_area_component";
import "./gate_part_component";
import "./barrier_component";
import "./card_component";
import "./auto_sprite_layer_component";
import "../entity/particles";

export type PlayerSaveData = {
    currentWorldName: string,
    currentMapName: string,
    currentX: number,
    currentY: number,
    scriptManager: ScriptManagerSaveData,
    quest: QuestSaveData,
    globalData: GameGlobalKVSaveData
}

export class Player {
    gameData: GameData;
    net: NetInterface;
    eventSystem: EventSystem;
    map: MapManager;
    input: InputManager;
    scriptManager: ScriptManager;
    quest: QuestManager;
    dialogue: DialogueModel;
    persistence?: GamePersistenceManager;
    globalData: GameGlobalKVManager;
    flagReveal: FlagRevealManager;
    debug?: Debug;

    constructor(data: GameData, net: NetInterface, storage?: GamePersistentStorage|null) {
        this.gameData = data;
        this.net = net;
        this.eventSystem = new EventSystem();
        this.map = new MapManager(this.net, new GameComponentRegistry(this.gameData.scriptBlob, this.gameData.componentMeta), data.tilesets);
        this.persistence = storage !== undefined ? new GamePersistenceManager(storage, this.map, () => this.save()) : undefined;
        this.map.persistence = this.persistence;
        this.map.baseSpritesheets = data.config.baseSpritesheets;
        if (data.mapData)
            this.map.mapFullData = data.mapData;
        if (data.spritesheets)
            this.map.spritesheetData.spritesheets = data.spritesheets;
        this.map.playerSingleton = this;
        this.map.eventSystemSingleton = this.eventSystem;
        this.input = new InputManager(net);
        this.map.inputManagerSingleton = this.input;
        this.scriptManager = new ScriptManager(net);
        this.map.scriptManagerSingleton = this.scriptManager;
        this.quest = new QuestManager(data.quest, data.scriptBlob, this.scriptManager, this);
        this.dialogue = new DialogueModel(net, this.eventSystem);
        this.globalData = new GameGlobalKVManager(this.eventSystem);
        this.flagReveal = new FlagRevealManager(this.net, this.globalData);
        if (data.config.enableDebug)
            this.debug = new Debug(this);
    }

    private save(): PlayerSaveData|null {
        const saveWorld = this.map.targetWorld || this.map.currentWorld;
        if (saveWorld === this.map.invalidWorld)
            return null;

        if (this.net.rpc.hasPendingSharedExecutions) {
            console.error('Cannot save as there are pending shared executions');
            return null;
        }

        const transform = saveWorld.teleportTmpEntity?.transform || saveWorld.player.transform!;
        return {
            currentWorldName: saveWorld.world.name,
            currentMapName: saveWorld.loader.mapMeta.name,
            currentX: transform.centerX,
            currentY: transform.centerY,

            scriptManager: this.scriptManager.save(),
            quest: this.quest.save(),
            globalData: this.globalData.save()
        }
    }

    onEnterGame(playerData: PlayerSaveData|null) {
        this.net.rpc.enterSharedBlock();

        if (playerData?.globalData)
            this.globalData.load(playerData.globalData);

        if (playerData?.scriptManager)
            this.scriptManager.load(playerData.scriptManager);

        if (playerData?.quest)
            this.quest.load(playerData.quest);
        this.quest.autoAddQuests();

        this.net.rpc.exitSharedBlock();

        if (!this.net.client) {
            if (playerData)
                this.map.enter(playerData.currentWorldName, this.map.mapFullData![playerData.currentMapName].meta, {x: playerData.currentX, y: playerData.currentY});
            else
                this.map.enter('main', this.map.mapFullData!['main_map'].meta, this.map.mapFullData!['main_map'].points['spawn']);
        }
    }

}
