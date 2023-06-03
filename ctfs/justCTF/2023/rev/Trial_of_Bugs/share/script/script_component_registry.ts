import {ScriptBlob} from "./blob";
import {Component, ComponentRegistry} from "../entity/component";
import {ScriptComponent} from "./script_component";
import {ScriptComponentMetaFile} from "./component_meta_data";

export class ScriptComponentRegistry extends ComponentRegistry {
    private readonly scriptBlob: ScriptBlob;
    private readonly componentMeta: ScriptComponentMetaFile;

    constructor(scriptBlob: ScriptBlob, componentMeta: ScriptComponentMetaFile) {
        super();
        this.scriptBlob = scriptBlob;
        this.componentMeta = componentMeta;
    }

    create(componentName: string): Component | null {
        if (componentName in this.componentMeta.components)
            return new ScriptComponent(this.scriptBlob, componentName, this.componentMeta.components[componentName]);
        return super.create(componentName);
    }
}
