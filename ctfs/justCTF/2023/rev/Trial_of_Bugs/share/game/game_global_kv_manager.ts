import {EventSystem} from "../event/event_system";
import {EVENT_GLOBAL_KV_UPDATE} from "../script/event_ids";

export type GameGlobalKVSaveData = {
    kv: {[key: string]: any};
}

export class GameGlobalKVManager {
    private readonly eventSystem: EventSystem;
    private kv: {[key: string]: any};

    constructor(eventSystem: EventSystem) {
        this.eventSystem = eventSystem;
        this.kv = {};
    }

    get(key: string): any {
        return this.kv[key];
    }

    set(key: string, value: any) {
        const oldValue = this.kv[key];
        this.kv[key] = value;
        this.eventSystem.emit(EVENT_GLOBAL_KV_UPDATE, {key, value, oldValue});
    }

    save(): GameGlobalKVSaveData {
        return {kv: this.kv};
    }

    load(data: GameGlobalKVSaveData) {
        this.kv = data.kv;
    }
}
