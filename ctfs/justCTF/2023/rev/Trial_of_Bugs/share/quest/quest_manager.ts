import {ScriptManager} from "../script/script_manager";
import {Player} from "../game/player";
import {ScriptBlob} from "../script/blob";
import {QuestMetaFile} from "./quest_data";
import {QuestInfo, QuestItemSaveData} from "./quest_info";
import {ObservableField} from "../util/observable_field";

export type QuestSaveData = {
    quests: QuestItemSaveData[]
}

export class QuestManager {
    private readonly scriptManager: ScriptManager;
    private readonly metaData: QuestMetaFile;
    private readonly blob: ScriptBlob;
    private readonly player: Player;
    private readonly quests: {[questName: string]: QuestInfo} = {};
    readonly activeQuests = new ObservableField<QuestInfo[]>([]);

    constructor(metaData: QuestMetaFile, blob: ScriptBlob, scriptManager: ScriptManager, player: Player) {
        this.scriptManager = scriptManager;
        this.metaData = metaData;
        this.blob = blob;
        this.player = player;
    }

    save(): QuestSaveData {
        return {quests: Object.values(this.quests).map(x => x.save())};
    }

    load(data: QuestSaveData) {
        for (const quest of data.quests) {
            if (!(quest.id in this.metaData.quests)) {
                console.error('Invalid quest in save data: ' + quest.id);
                continue;
            }
            this.quests[quest.id] = new QuestInfo(this.metaData.quests[quest.id], this, this.scriptManager, this.blob, this.player);
            this.quests[quest.id].load(quest);
        }
        this.updateActiveQuests();
    }

    private ensureQuest(questId: string): QuestInfo|null {
        if (!(questId in this.metaData.quests)) {
            console.error('Invalid quest for add quest: ' + questId);
            return null;
        }

        this.quests[questId] = new QuestInfo(this.metaData.quests[questId], this, this.scriptManager, this.blob, this.player);
        return this.quests[questId];
    }

    autoAddQuests() {
        for (const candidateData of Object.values(this.metaData.quests)) {
            if (candidateData.requires.every(x => this.quests[x]?.completed))
                this.addQuest(candidateData.id);
        }
    }

    addQuest(questId: string) {
        if (questId in this.quests)
            return;
        console.log('Adding quest: ' + questId);
        const quest = this.ensureQuest(questId);
        quest?.runLogic();
        this.updateActiveQuests();
    }

    completeQuest(questId: string) {
        const quest = this.ensureQuest(questId);
        if (quest && !quest.completed) {
            quest.completed = true;
            this.updateActiveQuests();
            for (const candidate of quest.meta.mightUnlock) {
                const candidateData = this.metaData.quests[candidate];
                if (candidateData.requires.every(x => this.quests[x]?.completed))
                    this.addQuest(candidate);
            }
        }
    }

    updateActiveQuests() {
        this.activeQuests.set(Object.values(this.quests).filter(x => !x.completed));
    }
}
