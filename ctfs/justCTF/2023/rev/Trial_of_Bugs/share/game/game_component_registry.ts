import {ScriptComponentRegistry} from "../script/script_component_registry";
import {Component} from "../entity/component";
import {transient} from "../util/transient";

export class GameComponentRegistry extends ScriptComponentRegistry {
    create(componentName: string): Component | null {
        const ret = super.create(componentName);
        if (ret)
            return ret;

        // Server doesn't have the renderer types, so stub them.
        if (componentName.startsWith('renderer:'))
            return new StubComponent(componentName);

        return null;
    }
}

class StubComponent extends Component {
    @transient typeName: string;

    constructor(typeName: string) {
        super();
        this.typeName = typeName;
    }
}
