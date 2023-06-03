import {Component} from "../entity/component";
import {ScriptBlob} from "./blob";
import {PlayerEvalCtx, StaticEvalCtx} from "./eval_ctx";
import {ScriptEvaluator} from "./evaluator";
import {ScriptManager} from "./script_manager";
import {Player} from "../game/player";
import {ScriptComponentMeta} from "./component_meta_data";
import {stripTransientProperties, transient} from "../util/transient";
import {ScriptHolder} from "./script_holder";
import {PlayerEntityLocator} from "../map/entity_locators";

export class ScriptComponent extends Component {
    @transient private readonly scriptBlob: ScriptBlob;
    @transient private readonly dependencies: string[];
    @transient typeName: string;
    @transient private holder?: ScriptHolder;

    constructor(scriptBlob: ScriptBlob, typeName: string, meta: ScriptComponentMeta) {
        super();
        this.scriptBlob = scriptBlob;
        this.typeName = typeName;
        this.dependencies = meta.components;

        const ctx = new StaticEvalCtx(scriptBlob);
        ctx.jsContext.self = this;
        ScriptEvaluator.start(ctx, `component.${typeName}.construct`);
        if (ScriptEvaluator.update(ctx))
            throw new Error('Component constructor evaluation did not complete immediately; this is not allowed.');
    }

    save() {
        const ret = stripTransientProperties(this, true);
        ret['_holder'] = this.holder!.save();
        return ret;
    }

    load(props: any) {
        Object.assign(this, props);

        const player = this.world.getSingleton(Player);
        this.holder = new ScriptHolder(this.world.getSingleton(ScriptManager), () => {
            return new EntityEvalCtx(this.scriptBlob, player, this);
        });
    }

    getDependencies(): string[] {
        return this.dependencies;
    }

    postLoad() {
        if ((this as any)._holder) {
            this.holder!.load((this as any)._holder);
            delete (this as any)._holder;
        }
        this.holder!.addScript(`component.${this.typeName}.init`);
    }

    onInteract() {
        this.holder!.addScript(`component.${this.typeName}.interact`);
    }

    run(scriptName: string) {
        this.holder!.addScript(`component.${this.typeName}.${scriptName}`);
    }
}

class EntityEvalCtx extends PlayerEvalCtx {
    component: ScriptComponent;

    constructor(blob: ScriptBlob, player: Player, component: ScriptComponent) {
        super(blob, player);
        this.component = component;
    }

    protected getContextVar(name: string): any {
        if (name === 'self')
            return this.component;
        if (name === 'playerEntity')
            return this.component.entity.world.getSingleton(PlayerEntityLocator).entity;
        if (name in this.component.entity)
            return this.component.entity[name];
        return super.getContextVar(name);
    }
}
