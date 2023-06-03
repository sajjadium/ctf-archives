import {QuestMeta} from "./quest_data";
import {ScriptManager} from "../script/script_manager";
import {ScriptBlob} from "../script/blob";
import {Player} from "../game/player";
import {ScriptHolder} from "../script/script_holder";
import {EvalCtx, PlayerEvalCtx} from "../script/eval_ctx";
import {QuestManager} from "./quest_manager";
import {AndTask} from "../script/tasks";

export type QuestItemSaveData = {
    id: string,
    completed: boolean,
    logicScriptId?: number,
    holder: any
}

export class QuestInfo {
    readonly meta: QuestMeta;
    readonly holder: QuestScriptHolder;
    completed: boolean = false;
    private logicScriptId?: number;

    constructor(meta: QuestMeta, manager: QuestManager, scriptManager: ScriptManager, blob: ScriptBlob, player: Player) {
        this.meta = meta;
        this.holder = new QuestScriptHolder(scriptManager, () => {
            return new QuestEvalCtx(blob, player, manager, this);
        });
    }

    save(): QuestItemSaveData {
        return {
            id: this.meta.id,
            holder: this.holder.save(),
            logicScriptId: this.logicScriptId,
            completed: this.completed
        }
    }

    load(data: QuestItemSaveData) {
        this.completed = data.completed;
        this.logicScriptId = data.logicScriptId;
        this.holder.load(data.holder);
    }

    get taskInfo(): [string, boolean][] {
        if (this.logicScriptId === undefined)
            return [];
        const task = this.holder.scripts[this.logicScriptId].task;
        if (task instanceof AndTask) {
            return task.subtasks.map((x, i) => x
                ? [x.description ||'<description missing>', false]
                : [task.completedSubtasks[i]?.description || '<completed>', true]);
        }
        return task ? [[task.description || '<description missing>', false]] : [];
    }

    runLogic() {
        this.logicScriptId = this.holder.addScript(`quest.${this.meta.id}.logic`).evalId!;
    }
}

class QuestScriptHolder extends ScriptHolder {
    onRemoveScript(ctx: EvalCtx) {
        const quest = (ctx as QuestEvalCtx).quest;
        const questManager = (ctx as QuestEvalCtx).questManager;
        questManager.completeQuest(quest.meta.id);
    }
}

class QuestEvalCtx extends PlayerEvalCtx {
    quest: QuestInfo;
    questManager: QuestManager;

    constructor(blob: ScriptBlob, player: Player, questManager: QuestManager, quest: QuestInfo) {
        super(blob, player);
        this.quest = quest;
        this.questManager = questManager;
    }

    protected getContextVar(name: string): any {
        return super.getContextVar(name);
    }
}
