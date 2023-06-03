export type QuestMeta = {
    id: string;
    name: string;
    requires: string[];
    mightUnlock: string[];
}

export type QuestMetaFile = {
    quests: {[id: string]: QuestMeta};
}
