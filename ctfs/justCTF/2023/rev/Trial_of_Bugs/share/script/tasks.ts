import {registerTask, ScriptTask} from "./task";
import {EVENT_GLOBAL_KV_UPDATE, EVENT_PLAYER_ENTER_AREA, EVENT_SCRIPT} from "./event_ids";
import {WrapperTask} from "./wrapper_task";
import {PlayerEvalCtx} from "./eval_ctx";

export class AndTask extends WrapperTask {
    static typeName = 'and';

    onSubtaskEnded(index: number) {
        super.onSubtaskEnded(index);
        if (this.subtasks.every(x => x === null)) {
            this.end();
        }
    }
}
registerTask(AndTask);

class ScriptEventTask extends ScriptTask {
    static typeName = 'script_event';

    filter!: any;

    onResume() {
        this.registerEventHandler(EVENT_SCRIPT, this.filter, () => this.end());
    }
}
registerTask(ScriptEventTask);


class GameGlobalTask extends ScriptTask {
    static typeName = 'game_global';

    key!: string;
    value!: any;

    onResume() {
        if ((this.ctx as PlayerEvalCtx).player.globalData.get(this.key) === this.value) {
            this.end();
            return;
        }

        this.registerEventHandler(EVENT_GLOBAL_KV_UPDATE, {key: this.key, value: this.value}, () => this.end());
    }
}
registerTask(GameGlobalTask);


class GameGlobalSetTask extends ScriptTask {
    static typeName = 'game_global_set';

    key!: string;

    onResume() {
        if ((this.ctx as PlayerEvalCtx).player.globalData.get(this.key) !== undefined) {
            this.end();
            return;
        }

        this.registerEventHandler(EVENT_GLOBAL_KV_UPDATE, {key: this.key}, (ev) => {
            if (ev.data.value !== undefined)
                this.end();
        });
    }
}
registerTask(GameGlobalSetTask);


class PlayerEnterAreaTask extends ScriptTask {
    static typeName = 'player_enter_area';

    worldName!: string;
    areaName!: string;

    onResume() {
        const {worldName, areaName} = this;
        this.registerEventHandler(EVENT_PLAYER_ENTER_AREA, {worldName, areaName}, () => this.end());
    }
}
registerTask(PlayerEnterAreaTask);


export const tasks = {
    and: (...tasks: ScriptTask[]) => {
        const ret = new AndTask();
        ret.setSubtasks(tasks);
        return ret;
    },
    scriptEvent: (filter: any, description?: string) => {
        const ret = new ScriptEventTask();
        ret.filter = filter;
        ret.description = description;
        return ret;
    },
    gameGlobal: (key: string, value: any, description?: string) => {
        const ret = new GameGlobalTask();
        ret.key = key;
        ret.value = value;
        ret.description = description;
        return ret;
    },
    gameGlobalSet: (key: string, description?: string) => {
        const ret = new GameGlobalSetTask();
        ret.key = key;
        ret.description = description;
        return ret;
    },
    enterArea: (worldName: string, areaName: string, description?: string) => {
        const task = new PlayerEnterAreaTask();
        task.worldName = worldName;
        task.areaName = areaName;
        task.description = description;
        return task;
    }
};
