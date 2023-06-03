export type ScriptComponentMeta = {
    name: string;
    components: string[];
    props: { [key: string]: string };
    defaults: { [key: string]: any };
}

export type ScriptComponentMetaFile = {
    components: {[name: string]: ScriptComponentMeta}
}
